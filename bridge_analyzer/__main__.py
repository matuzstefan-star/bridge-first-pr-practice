"""CLI: python -m bridge_analyzer <source|folder> [...] [--solve] [--play] [--docx out.docx] [--archive dir]"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import shutil
import sys
from pathlib import Path

from .analysis import analyze_board, summarize
from .lin_tools import fetch_lin, parse_lin
from .report import board_report, play_report, solver_report, summary_report
from .solver import SolverUnavailable, solve


def collect(sources: list[str]) -> list[tuple[str, str, list[Path]]]:
    """Return (label, LIN text, files) per distinct hand. A folder expands to its
    .lin files; identical content (e.g. 'name (1).lin' re-downloads) is one hand."""
    by_hash: dict[str, tuple[str, str, list[Path]]] = {}
    for source in sources:
        path = Path(source)
        if path.is_dir():
            items = [(f.name, f.read_text(encoding="utf-8"), f) for f in sorted(path.glob("*.lin"))]
        elif path.is_file():
            items = [(path.name, path.read_text(encoding="utf-8"), path)]
        else:
            items = [(source[:60], fetch_lin(source), None)]
        for label, lin, file in items:
            key = hashlib.sha1(lin.strip().encode("utf-8")).hexdigest()
            entry = by_hash.setdefault(key, (label, lin, []))
            if file is not None:
                entry[2].append(file)
    return list(by_hash.values())


def archive(files: list[Path], folder: Path) -> int:
    folder.mkdir(parents=True, exist_ok=True)
    for f in files:
        target = folder / f.name
        if target.exists():
            target = folder / f"{f.stem}_{datetime.datetime.now():%H%M%S}{f.suffix}"
        shutil.move(str(f), str(target))
    return len(files)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="bridge_analyzer", description="Analyze hands played on Bridge Base Online.")
    ap.add_argument("sources", nargs="+", help="a folder of .lin files, a .lin/.txt file, a fetchlin URL, or raw LIN text")
    ap.add_argument("--username", default="steffl54", help="BBO username whose seat is labeled (default: steffl54)")
    ap.add_argument("--play", action="store_true", help="add a trick-by-trick review of the card play")
    ap.add_argument("--solve", action="store_true", help="add double-dummy analysis (needs the endplay solver env)")
    ap.add_argument("--docx", metavar="FILE", help="also write a Word report to this file")
    ap.add_argument("--lang", choices=["en", "ro"], default="en", help="language of the Word report (default: en)")
    ap.add_argument("--archive", metavar="DIR", help="after a successful run, move the processed .lin files here")
    ap.add_argument("-o", "--output", help="write the text report to this file instead of stdout")
    args = ap.parse_args(argv)

    analyses, dds, processed = [], [], []
    for label, lin, files in collect(args.sources):
        try:
            board = parse_lin(lin, username=args.username)
            a = analyze_board(board, lin)
        except (ValueError, KeyError, IndexError) as e:
            print(f"Skipped {label!r}: {e}", file=sys.stderr)
            continue
        dd = None
        if args.solve:
            try:
                dd = solve(board)
            except SolverUnavailable as e:
                print(f"Double dummy skipped for {label!r}: {e}", file=sys.stderr)
        analyses.append(a)
        dds.append(dd)
        processed.extend(files)

    if not analyses:
        print("No boards could be analyzed.", file=sys.stderr)
        return 1

    def order(pair):
        n = pair[0].board.number
        return int(n) if n and n.isdigit() else 10**6

    pairs = sorted(zip(analyses, dds), key=order)
    analyses, dds = [p[0] for p in pairs], [p[1] for p in pairs]

    parts = []
    for a, dd in pairs:
        parts.append(board_report(a, args.username))
        if dd:
            parts.append(solver_report(a, dd))
        if args.play:
            parts.append(play_report(a, args.username))
    if len(analyses) > 1:
        parts.append(summary_report(summarize(analyses)))
    text = "\n\n".join(parts) + "\n"

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print(f"Report written to {args.output}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text, end="")

    if args.docx:
        from .docx_report import build_report

        Path(args.docx).parent.mkdir(parents=True, exist_ok=True)
        build_report(analyses, dds, args.docx, args.username, datetime.date.today(), lang=args.lang)
        print(f"Word report written to {args.docx}", file=sys.stderr)

    if args.archive and processed:
        n = archive(processed, Path(args.archive))
        print(f"Moved {n} processed file(s) to {args.archive}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
