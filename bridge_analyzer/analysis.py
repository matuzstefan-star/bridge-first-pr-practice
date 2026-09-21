"""
Analysis of parsed BBO boards: hand strength, card-play result, duplicate score.

Builds on lin_tools (parsing only). lin_tools does not read the card play
(pc| tags), so this module reads those straight from the raw LIN text.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .lin_tools import CLOCKWISE, DIRNAME, RANK_ORDER, SUITS, Board

HCP_VALUES = {"A": 4, "K": 3, "Q": 2, "J": 1}
SUIT_SYMBOL = {"S": "♠", "H": "♥", "D": "♦", "C": "♣", "NT": "NT"}


def side_of(pos: str) -> str:
    return "NS" if pos in ("N", "S") else "EW"


def partner_of(pos: str) -> str:
    return CLOCKWISE[(CLOCKWISE.index(pos) + 2) % 4]


def hcp(hand: dict) -> int:
    return sum(HCP_VALUES.get(c, 0) for cards in hand.values() for c in cards)


def shape_text(hand: dict) -> str:
    """Suit lengths in S-H-D-C order, e.g. '4-3-3-3'."""
    return "-".join(str(len(hand[s])) for s in SUITS)


# --- card play -------------------------------------------------------------

def parse_play(lin_text: str) -> list[str]:
    """Cards played in order, from the pc| tags (e.g. 'SA', 'H2', 'DT')."""
    tokens = lin_text.strip().split("|")
    return [v.strip().upper() for t, v in zip(tokens[0::2], tokens[1::2]) if t == "pc"]


def _beats(card: str, best: str, trump: str | None) -> bool:
    if card[0] == best[0]:
        return RANK_ORDER.index(card[1]) < RANK_ORDER.index(best[1])
    # Different suits: `best` is the led suit or a trump, so only a trump beats it.
    return card[0] == trump


@dataclass
class Trick:
    number: int
    leader: str
    cards: dict          # pos -> card, e.g. 'SA'
    winner: str
    ruffers: list        # positions that trumped a non-trump lead
    declarer_won: int    # tricks won by the declaring side so far, including this one


def play_log(plays: list[str], declarer: str, strain: str) -> list[Trick]:
    """Complete tricks from the card play; a trailing partial trick is ignored."""
    trump = None if strain == "NT" else strain
    leader = CLOCKWISE[(CLOCKWISE.index(declarer) + 1) % 4]
    log, won = [], 0
    for i in range(0, len(plays) - len(plays) % 4, 4):
        trick = plays[i : i + 4]
        best = 0
        for j in range(1, 4):
            if _beats(trick[j], trick[best], trump):
                best = j
        cards = {CLOCKWISE[(CLOCKWISE.index(leader) + k) % 4]: c for k, c in enumerate(trick)}
        ruffers = [p for p, c in cards.items() if trump and c[0] == trump and trick[0][0] != trump]
        winner = CLOCKWISE[(CLOCKWISE.index(leader) + best) % 4]
        if side_of(winner) == side_of(declarer):
            won += 1
        log.append(Trick(i // 4 + 1, leader, cards, winner, ruffers, won))
        leader = winner
    return log


def declarer_side_tricks(plays: list[str], declarer: str, strain: str) -> int | None:
    """Tricks won by the declaring side, or None if fewer than 13 tricks were played."""
    log = play_log(plays, declarer, strain)
    return log[-1].declarer_won if len(log) == 13 else None


# --- scoring ---------------------------------------------------------------

def duplicate_score(level: int, strain: str, doubled: int, tricks: int, vul: bool) -> int:
    """Duplicate score from declarer's side (negative when the contract fails)."""
    need = level + 6
    mult = {0: 1, 1: 2, 2: 4}[doubled]

    if tricks < need:
        down = need - tricks
        if doubled == 0:
            pts = (100 if vul else 50) * down
        elif vul:
            pts = 200 + 300 * (down - 1)
        else:
            pts = [100, 300, 500][down - 1] if down <= 3 else 500 + 300 * (down - 3)
        return -pts * (2 if doubled == 2 else 1)

    per = 20 if strain in ("C", "D") else 30
    trick_pts = (per * level + (10 if strain == "NT" else 0)) * mult
    bonus = (500 if vul else 300) if trick_pts >= 100 else 50
    if level == 6:
        bonus += 750 if vul else 500
    elif level == 7:
        bonus += 1500 if vul else 1000
    bonus += {0: 0, 1: 50, 2: 100}[doubled]

    over = tricks - need
    if doubled == 0:
        over_pts = per * over
    else:
        over_pts = (200 if vul else 100) * over * (2 if doubled == 2 else 1)
    return trick_pts + bonus + over_pts


# --- per-board analysis ----------------------------------------------------

@dataclass
class BoardAnalysis:
    board: Board
    hcp: dict                      # pos -> HCP
    shapes: dict                   # pos -> 'S-H-D-C' text
    declarer_tricks: int | None    # None when the result is unknown (e.g. no play in LIN)
    tricks_source: str | None      # 'play' or 'claim'
    declarer_score: int | None     # from declarer's side
    role: str | None               # Steffy's role: declarer / dummy / defender
    side_hcp: int | None = None    # declaring side combined HCP
    fit: int | None = None         # declaring side length in the trump suit
    notes: list = field(default_factory=list)
    tricks: list = field(default_factory=list)  # play_log() result
    note_kind: str | None = None   # key of the HCP yardstick note, if any

    @property
    def steffl_side_score(self) -> int | None:
        """Score from the point of view of Steffy's side."""
        b = self.board
        if self.declarer_score is None or b.steffl_pos is None or b.contract is None:
            return None
        same_side = side_of(b.steffl_pos) == side_of(b.contract.declarer)
        return self.declarer_score if same_side else -self.declarer_score


def _is_vulnerable(board: Board, pos: str) -> bool:
    v = board.vulnerability
    return v == "Both" or v == side_of(pos)


NOTE_TEXT_EN = {
    "slam_light": "slam with only {hcp} combined HCP (slams usually want ~33)",
    "game_light": "game with only {hcp} combined HCP (game usually wants ~25)",
    "part_heavy": "part-score with {hcp} combined HCP (game values)",
}


def _bidding_kind(level: int, strain: str, side_hcp: int) -> str | None:
    """Very rough HCP yardstick (25 game / 33 slam), not a bidding verdict."""
    game_level = {"NT": 3, "H": 4, "S": 4, "C": 5, "D": 5}[strain]
    if level >= 7:
        return None
    if level >= 6:
        return "slam_light" if side_hcp < 30 else None
    if level >= game_level:
        return "game_light" if side_hcp < 24 else None
    return "part_heavy" if side_hcp >= 27 else None


def analyze_board(board: Board, lin_text: str) -> BoardAnalysis:
    points = {pos: hcp(h) for pos, h in board.hands.items()}
    shapes = {pos: shape_text(h) for pos, h in board.hands.items()}
    c = board.contract

    tricks, source, log = None, None, []
    if c is not None:
        log = play_log(parse_play(lin_text), c.declarer, c.strain)
        played = log[-1].declarer_won if len(log) == 13 else None
        if board.result_tricks is not None:  # mc| claim = declarer's total
            tricks, source = board.result_tricks, "claim"
        elif played is not None:
            tricks, source = played, "play"

    score = None
    if c is not None and tricks is not None:
        score = duplicate_score(c.level, c.strain, c.doubled, tricks, _is_vulnerable(board, c.declarer))

    role = None
    if board.steffl_pos is not None and c is not None:
        if board.steffl_pos == c.declarer:
            role = "declarer"
        elif board.steffl_pos == partner_of(c.declarer):
            role = "dummy"
        else:
            role = "defender"

    result = BoardAnalysis(board, points, shapes, tricks, source, score, role, tricks=log)

    if c is not None:
        dummy = partner_of(c.declarer)
        result.side_hcp = points[c.declarer] + points[dummy]
        if c.strain != "NT":
            result.fit = sum(len(board.hands[p][c.strain]) for p in (c.declarer, dummy))
        result.note_kind = _bidding_kind(c.level, c.strain, result.side_hcp)
        if result.note_kind:
            result.notes.append(NOTE_TEXT_EN[result.note_kind].format(hcp=result.side_hcp))
    return result


# --- summary over several boards -------------------------------------------

@dataclass
class Summary:
    boards: int = 0
    passed_out: int = 0
    with_role: int = 0
    as_declarer: int = 0
    as_dummy: int = 0
    as_defender: int = 0
    declarer_made: int = 0
    declarer_played: int = 0
    avg_hcp: float | None = None
    total_score: int = 0
    scored: int = 0


def summarize(analyses: list[BoardAnalysis]) -> Summary:
    s = Summary(boards=len(analyses))
    hcps = []
    for a in analyses:
        b = a.board
        if b.contract is None:
            s.passed_out += 1
        if b.steffl_pos is not None:
            s.with_role += 1
            hcps.append(a.hcp[b.steffl_pos])
        if a.role == "declarer":
            s.as_declarer += 1
            if a.declarer_tricks is not None:
                s.declarer_played += 1
                if a.declarer_tricks >= b.contract.level + 6:
                    s.declarer_made += 1
        elif a.role == "dummy":
            s.as_dummy += 1
        elif a.role == "defender":
            s.as_defender += 1
        sc = a.steffl_side_score
        if sc is not None:
            s.total_score += sc
            s.scored += 1
    if hcps:
        s.avg_hcp = sum(hcps) / len(hcps)
    return s
