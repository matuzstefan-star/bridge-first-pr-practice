"""Plain-text report for analyzed boards. Only Steffy's own seat is ever named."""
from __future__ import annotations

from .analysis import SUIT_SYMBOL, BoardAnalysis, Summary, side_of
from .lin_tools import DIRNAME

ORDER = ["N", "E", "S", "W"]


def _result(a: BoardAnalysis) -> str:
    c = a.board.contract
    if a.declarer_tricks is None:
        return "result unknown (no card play or claim in the LIN)"
    diff = a.declarer_tricks - (c.level + 6)
    if diff == 0:
        text = f"made exactly ({a.declarer_tricks} tricks)"
    elif diff > 0:
        text = f"made {a.declarer_tricks} tricks (+{diff})"
    else:
        text = f"down {-diff} ({a.declarer_tricks} tricks)"
    return text


def board_report(a: BoardAnalysis, username: str) -> str:
    b = a.board
    title = f"Board {b.number}" if b.number else "Board"
    lines = [f"{title} - dealer {DIRNAME[b.dealer].title()}, vul {b.vulnerability}"]

    if b.contract is None:
        lines.append("Contract: passed out")
    else:
        c = b.contract
        seat = DIRNAME[c.declarer].title()
        if c.declarer == b.steffl_pos:
            seat += f" ({username})"
        lines.append(f"Contract: {c.level}{c.strain_symbol}{'X' * c.doubled} by {seat}")
        lines.append(f"Result:   {_result(a)}")
        if a.declarer_score is not None:
            signed = a.declarer_score if side_of(c.declarer) == "NS" else -a.declarer_score
            lines.append(f"Score:    {'NS' if signed >= 0 else 'EW'} {abs(signed)}")
    lines.append("HCP:      " + " | ".join(f"{p} {a.hcp[p]}" for p in ORDER))
    lines.append("Shapes:   " + " | ".join(f"{p} {a.shapes[p]}" for p in ORDER) + "   (S-H-D-C)")
    if a.side_hcp is not None:
        fit = f", trump fit {a.fit} cards" if a.fit is not None else ""
        lines.append(f"Declaring side: {a.side_hcp} HCP{fit}")
    if a.role:
        lines.append(f"Steffy's role: {a.role}")
    for note in a.notes:
        lines.append(f"Note:     {note}")
    return "\n".join(lines)


def summary_report(s: Summary) -> str:
    lines = ["Summary", f"Boards analyzed: {s.boards} (passed out: {s.passed_out})"]
    if s.with_role:
        lines.append(
            f"Steffy's seat found in {s.with_role} boards: "
            f"declarer {s.as_declarer}, dummy {s.as_dummy}, defender {s.as_defender}"
        )
        if s.avg_hcp is not None:
            lines.append(f"Average HCP held: {s.avg_hcp:.1f}")
        if s.declarer_played:
            lines.append(f"Contracts made as declarer: {s.declarer_made}/{s.declarer_played}")
        if s.scored:
            lines.append(f"Total raw score for Steffy's side: {s.total_score:+d} over {s.scored} boards")
    return "\n".join(lines)


def _card(card: str) -> str:
    return SUIT_SYMBOL[card[0]] + ("10" if card[1] == "T" else card[1])


def play_report(a: BoardAnalysis, username: str) -> str:
    """Trick-by-trick review. Facts from the recorded play only, no double-dummy analysis."""
    b, c = a.board, a.board.contract
    if c is None or not a.tricks:
        return "Play: no card play recorded"

    trump = None if c.strain == "NT" else c.strain
    dec_side = side_of(c.declarer)
    header = [p + (f" ({username})" if p == b.steffl_pos else "") for p in ORDER]
    width = max(6, *(len(h) for h in header))
    lines = [
        f"Play - {c.level}{c.strain_symbol} by {DIRNAME[c.declarer].title()}, "
        f"trump {SUIT_SYMBOL[c.strain]}   (> = leader)",
        "  #  " + " ".join(h.ljust(width) for h in header) + "  Winner  Declaring side",
    ]
    for t in a.tricks:
        cells = [(">" if p == t.leader else " ") + _card(t.cards[p]) for p in ORDER]
        lines.append(
            f"{t.number:>3}  " + " ".join(x.ljust(width) for x in cells)
            + f"  {t.winner + ('*' if t.ruffers and t.winner in t.ruffers else ''):<6}  {t.declarer_won}"
        )
    lines.append("(* = won by a trump on a non-trump lead)")

    facts = []
    first = a.tricks[0]
    facts.append(f"Opening lead: {DIRNAME[first.leader].title()} {_card(first.cards[first.leader])}")

    if trump:
        ruffs = [t for t in a.tricks if t.ruffers]
        if ruffs:
            facts.append("Ruffs: " + "; ".join(
                f"trick {t.number} by " + "/".join(
                    f"{p} ({'declaring side' if side_of(p) == dec_side else 'defenders'})" for p in t.ruffers)
                for t in ruffs))
        trump_leads = [t.number for t in a.tricks if t.cards[t.leader][0] == trump]
        facts.append("Trump led on tricks: " + (", ".join(map(str, trump_leads)) or "none"))
        defenders = [p for p in ORDER if side_of(p) != dec_side]
        held = sum(len(b.hands[p][trump]) for p in defenders)
        played = sum(1 for t in a.tricks for p in defenders if t.cards[p][0] == trump)
        facts.append(f"Defenders' trumps: {held} held, {played} played in {len(a.tricks)} tricks")

    lost = [t for t in a.tricks if side_of(t.winner) != dec_side]
    if lost:
        facts.append("Tricks lost by declarer: " + "; ".join(
            f"{t.number} to {t.winner} ({_card(t.cards[t.winner])})" for t in lost))

    done, total = len(a.tricks), 13
    if done < total:
        remaining = total - done
        got = None if b.result_tricks is None else b.result_tricks - a.tricks[-1].declarer_won
        if got is None:
            facts.append(f"Play stopped after {done} tricks ({remaining} not recorded)")
        else:
            facts.append(
                f"Play stopped after {done} tricks; claim gave declarer {got} of the last {remaining} "
                f"(final {b.result_tricks} tricks)")
    return "\n".join(lines + [""] + [f"- {f}" for f in facts])


def solver_report(a: BoardAnalysis, dd: dict) -> str:
    """Double-dummy comparison of the actual result with what the cards allowed."""
    b, c = a.board, a.board.contract
    table = dd["table"]
    cols = ["C", "D", "H", "S", "NT"]
    lines = ["Double dummy (tricks each declarer can take)",
             "      " + "".join(f"{SUIT_SYMBOL[x]:>4}" for x in cols)]
    for p in ORDER:
        lines.append(f"  {p}   " + "".join(f"{table[p][x]:>4}" for x in cols))
    par = " ".join(dd["par_contracts"])
    lines.append(f"Par: {par}  (N-S {dd['par_score']:+d})")
    if c is not None:
        dd_tricks = table[c.declarer][c.strain]
        need = c.level + 6
        lines.append(f"Contract {c.level}{c.strain_symbol}: needs {need}, double dummy gives {dd_tricks}"
                     + (" - makes" if dd_tricks >= need else f" - down {need - dd_tricks} at best defense"))
        if a.declarer_tricks is not None:
            diff = a.declarer_tricks - dd_tricks
            how = "matched double dummy" if diff == 0 else (
                f"{abs(diff)} trick{'s' if abs(diff) > 1 else ''} {'better' if diff > 0 else 'worse'} than double dummy")
            lines.append(f"Actual result {a.declarer_tricks} tricks: {how}")
    return chr(10).join(lines)
