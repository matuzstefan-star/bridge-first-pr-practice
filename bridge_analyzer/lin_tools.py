"""
Core parsing library for BBO (Bridge Base Online) LIN hand records.

A LIN string is a sequence of tag|value|tag|value|... pairs. This module
turns that into a Board object with sorted hands, an assigned-to-position
auction, a deduced contract/declarer, and an anonymization helper -- with
no dependency on python-docx, so it can be tested/reused on its own.
"""
from __future__ import annotations

import re
import urllib.request
from dataclasses import dataclass, field
from urllib.parse import urlparse, parse_qs, unquote

RANK_ORDER = "AKQJT98765432"
SUITS = ["S", "H", "D", "C"]
DIRECTIONS = ["S", "W", "N", "E"]  # order LIN lists hands/players in (pn, md)
CLOCKWISE = ["N", "E", "S", "W"]  # bidding rotation order
DIRNAME = {"N": "NORTH", "E": "EAST", "S": "SOUTH", "W": "WEST"}
DEALER_MAP = {"1": "S", "2": "W", "3": "N", "4": "E"}
VUL_MAP = {"o": "None", "n": "NS", "e": "EW", "b": "Both"}


@dataclass
class Contract:
    level: int
    strain: str  # 'S','H','D','C','NT'
    doubled: int  # 0=none, 1=X, 2=XX
    declarer: str  # N/E/S/W

    @property
    def strain_symbol(self) -> str:
        return {"S": "♠", "H": "♥", "D": "♦", "C": "♣", "NT": "NT"}[self.strain]

    def __str__(self) -> str:
        dbl = {0: "", 1: "X", 2: "XX"}[self.doubled]
        return f"{self.level}{self.strain_symbol}{dbl} by {DIRNAME[self.declarer].title()}"


@dataclass
class Board:
    number: str | None
    dealer: str
    vulnerability: str
    players: dict  # position -> raw BBO name (S,W,N,E)
    hands: dict  # position -> {suit: [ranks sorted desc]}
    calls: list  # list of (position, normalized_call_str)
    contract: Contract | None
    result_tricks: int | None
    steffl_pos: str | None  # which position matches the target username, if any

    def label(self, pos: str, username_display: str = "steffl54") -> str:
        """Anonymized seat label: real BBO names are never surfaced except
        for the user's own seat, which is tagged with their username."""
        if pos == self.steffl_pos:
            return f"{DIRNAME[pos]} ({username_display})"
        return DIRNAME[pos]

    @property
    def result_text(self) -> str | None:
        if self.contract is None or self.result_tricks is None:
            return None
        needed = self.contract.level + 6
        diff = self.result_tricks - needed
        if diff == 0:
            return f"made exactly {self.result_tricks}"
        if diff > 0:
            return f"made {self.result_tricks} (+{diff})"
        return f"down {-diff} ({self.result_tricks} tricks)"


def sort_desc(cards: list) -> list:
    return sorted(cards, key=lambda c: RANK_ORDER.index(c))


def _parse_hand_string(s: str) -> dict:
    suits = {suit: [] for suit in SUITS}
    current = None
    for ch in s:
        if ch in SUITS:
            current = ch
        elif current is not None and ch in RANK_ORDER:
            suits[current].append(ch)
    return suits


def _deduce_missing_hand(known_hands: dict) -> dict:
    used = {suit: set() for suit in SUITS}
    for hand in known_hands.values():
        for suit, cards in hand.items():
            used[suit].update(cards)
    return {suit: [c for c in RANK_ORDER if c not in used[suit]] for suit in SUITS}


def parse_hands(md_value: str) -> tuple[str, dict]:
    """Returns (dealer, {pos: {suit: [ranks desc]}}) from an md| tag value."""
    parts = md_value.split(",")
    while len(parts) < 4:
        parts.append("")
    parts = parts[:4]

    dealer = "N"
    first = parts[0]
    if first and first[0].isdigit():
        dealer = DEALER_MAP.get(first[0], "N")
        parts[0] = first[1:]

    hands, missing = {}, []
    for pos, part in zip(DIRECTIONS, parts):
        if part.strip() == "":
            missing.append(pos)
        else:
            hands[pos] = _parse_hand_string(part)

    if len(missing) == 1:
        hands[missing[0]] = _deduce_missing_hand(hands)
    elif len(missing) > 1:
        raise ValueError(
            f"LIN is missing {len(missing)} hands {missing} - can only deduce "
            "a single missing hand by elimination. Ask for the full LIN."
        )

    for pos in hands:
        for suit in SUITS:
            hands[pos][suit] = sort_desc(hands[pos].get(suit, []))
    return dealer, hands


def normalize_call(raw: str) -> str:
    c = raw.strip().rstrip("!").upper()
    if c in ("P", "PASS"):
        return "Pass"
    if c in ("D", "X"):
        return "X"
    if c in ("R", "XX"):
        return "XX"
    m = re.match(r"^(\d)(N|NT|S|H|D|C)$", c)
    if m:
        level, strain = m.groups()
        return f"{level}{'NT' if strain in ('N', 'NT') else strain}"
    return c


def _assign_positions(calls: list, dealer: str) -> list:
    start = CLOCKWISE.index(dealer)
    return [CLOCKWISE[(start + i) % 4] for i in range(len(calls))]


def _determine_contract(calls: list, positions: list) -> Contract | None:
    bid_re = re.compile(r"^(\d)(NT|S|H|D|C)$")
    final_idx = None
    for i, c in enumerate(calls):
        if bid_re.match(c):
            final_idx = i
    if final_idx is None:
        return None  # passed out

    level, strain = bid_re.match(calls[final_idx]).groups()
    level = int(level)
    final_pos = positions[final_idx]
    declarer_side = "NS" if final_pos in ("N", "S") else "EW"

    doubled = 0
    for c in calls[final_idx + 1 :]:
        if c == "X":
            doubled = 1
        elif c == "XX":
            doubled = 2

    declarer = final_pos
    for i, c in enumerate(calls):
        m = bid_re.match(c)
        if m and m.group(2) == strain:
            side = "NS" if positions[i] in ("N", "S") else "EW"
            if side == declarer_side:
                declarer = positions[i]
                break

    return Contract(level=level, strain=strain, doubled=doubled, declarer=declarer)


def parse_lin(text: str, username: str = "steffl54", board_number_override: str | None = None) -> Board:
    text = text.strip()
    tokens = text.split("|")
    pairs = list(zip(tokens[0::2], tokens[1::2]))

    players = {}
    dealer, hands = "N", {}
    vulnerability = "Unknown"
    raw_calls = []
    board_number = board_number_override
    result_tricks = None

    for tag, value in pairs:
        if tag == "pn":
            names = value.split(",")
            for pos, name in zip(DIRECTIONS, names):
                players[pos] = name
        elif tag == "md":
            dealer, hands = parse_hands(value)
        elif tag == "sv":
            vulnerability = VUL_MAP.get(value.strip().lower(), "Unknown")
        elif tag == "mb":
            raw_calls.append(value)
        elif tag == "ah" and board_number is None:
            m = re.search(r"Board\s*(\d+)", value, re.IGNORECASE)
            if m:
                board_number = m.group(1)
        elif tag == "mc":
            try:
                result_tricks = int(value)
            except ValueError:
                pass

    calls_norm = [normalize_call(c) for c in raw_calls]
    positions = _assign_positions(calls_norm, dealer)
    calls = list(zip(positions, calls_norm))
    contract = _determine_contract(calls_norm, positions)

    steffl_pos = None
    target = username.strip().lower()
    for pos, name in players.items():
        if name.strip().lower() == target:
            steffl_pos = pos
            break

    return Board(
        number=board_number,
        dealer=dealer,
        vulnerability=vulnerability,
        players=players,
        hands=hands,
        calls=calls,
        contract=contract,
        result_tricks=result_tricks,
        steffl_pos=steffl_pos,
    )


def auction_grid(board: "Board") -> list[list[str]]:
    """Rows of 4 calls (West, North, East, South columns), blanks before the
    dealer's first turn and after the auction ends. Shared by the docx and
    HTML renderers so the two views never drift apart."""
    columns = ["W", "N", "E", "S"]
    calls = board.calls
    if not calls:
        return []
    start_col = columns.index(calls[0][0])
    grid = [""] * start_col + [c for _, c in calls]
    while len(grid) % 4 != 0:
        grid.append("")
    return [grid[i : i + 4] for i in range(0, len(grid), 4)]


def fetch_lin(source: str) -> str:
    """Fetch raw LIN text from a fetchlin URL, extract it from a handviewer
    URL's lin= query param, or pass raw LIN text straight through."""
    source = source.strip()
    if source.lower().startswith("http"):
        parsed = urlparse(source)
        qs = parse_qs(parsed.query)
        if "lin" in qs:
            return unquote(qs["lin"][0])
        req = urllib.request.Request(source, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8", errors="replace")
        if "pn|" not in body and "md|" not in body:
            raise ValueError(
                "Fetched content doesn't look like LIN data (no pn|/md| tags found). "
                "Try the bridgebase.com/myhands/fetchlin.php?id=...&when_played=... "
                "URL, or paste the raw LIN text directly."
            )
        return body
    return source  # assume it's already raw LIN text
