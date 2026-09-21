"""CLI: python -m bridge_analyzer <source> [<source> ...] [-o report.txt]"""
from __future__ import annotations

import argparse
import sys

from .analysis import analyze_board, summarize
from .lin_tools import fetch_lin, parse_lin
from .report import board_report, play_report, solver_report, summary_report
from .solver import SolverUnavailable, solve


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="bridge_analyzer",
        description="Analyze hands played on Bridge Base Online.",
    )
    ap.add_argument(
        "sources",
        nargs="+",
        help="fetchlin.php URL, handviewer URL with lin=, raw LIN text, or a path to a .lin/.txt file",
    )
    ap.add_argument("--username", default="steffl54", help="BBO username whose seat is labeled (default: steffl54)")
    ap.add_argument("--play", action="store_true", help="add a trick-by-trick review of the card play")
    ap.add_argument("--solve", action="store_true", help="add double-dummy analysis (needs the endplay solver env)")
    ap.add_argument("-o", "--output", help="write the report to this file instead of stdout")
    args = ap.parse_args(argv)

    analyses = []
    for source in args.sources:
        try:
            try:
                with open(source, encoding="utf-8") as f:
                    lin = f.read()
            except OSError:
                lin = fetch_lin(source)
            board = parse_lin(lin, username=args.username)
            analyses.append(analyze_board(board, lin))
        except (ValueError, OSError) as e:
            print(f"Skipped {source[:60]!r}: {e}", file=sys.stderr)

    if not analyses:
        print("No boards could be analyzed.", file=sys.stderr)
        return 1

    parts = []
    for a in analyses:
        parts.append(board_report(a, args.username))
        if args.solve:
            try:
                parts.append(solver_report(a, solve(a.board)))
            except SolverUnavailable as e:
                print(f"Double dummy skipped: {e}", file=sys.stderr)
        if args.play:
            parts.append(play_report(a, args.username))
    if len(analyses) > 1:
        parts.append(summary_report(summarize(analyses)))
    text = "\n\n".join(parts) + "\n"

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Report written to {args.output}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
