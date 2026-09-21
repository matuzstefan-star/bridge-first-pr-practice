# Bridge First PR Practice

This repo exists so I could ship my first pull request with Claude Code.

## About

I'm Steffy — author of *Horoscope for Bridge Players* (available on Amazon) and a bridge trainer with 50 years of competitive experience. This repo is just a small practice ground, not affiliated with the book itself.

## Bridge hand analyzer

Analyzes hands played on Bridge Base Online (BBO): HCP and shape per seat,
contract and declarer, tricks taken (from the card play or the claim),
duplicate score, and a rough HCP check of the contract. With several boards
it also prints a summary for the chosen username's seat.

```
python -m bridge_analyzer <source> [<source> ...] [--play] [--username steffl54] [-o report.txt]
```

`--play` adds a trick-by-trick review: every trick with its winner, ruffs, the
tricks the declarer lost, and how a claim ended the hand. It reports what was
played; it does not judge the play (no double-dummy solver).

`--solve` adds double-dummy analysis (DDS by Bo Haglund, via `endplay`): the
trick table for every declarer/strain, par, and how the actual result compares.
`endplay` has no wheel for Python 3.14, so it lives in its own Python 3.13 venv
(`analizor done/solver-env`), called as a subprocess. Set `BRIDGE_SOLVER_PYTHON`
to point at a different interpreter that has `endplay` installed.

`<source>` is a folder of `.lin` files (identical re-downloads such as `name (1).lin`
are treated as one hand), a `fetchlin.php` URL, a handviewer URL with `lin=`, raw LIN text,
or a path to a `.lin`/`.txt` file. Only the chosen username's seat is named in
the report; the other seats appear as compass directions.

`bridge_analyzer/lin_tools.py` is a copy of the LIN parser from the
`import-done` skill. Card play (`pc|` tags) is read in `analysis.py`.

`--docx FILE` also writes a Word report (English by default, `--lang ro` for Romanian): summary page, then one page
per board: diagram, auction, result, double-dummy table, observations.
`--archive DIR` moves the processed `.lin` files to `DIR` after a successful run.

Run the tests with `python -m unittest discover -s tests -t .`
