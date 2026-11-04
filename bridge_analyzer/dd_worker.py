"""Double-dummy worker. Runs under the Python that has endplay installed (3.13),
not the analyzer's own interpreter. Reads a JSON deal on stdin, prints JSON.

stdin:  {"hands": {"N": "A7.96543.AJ97.T8", ...}, "dealer": "W", "vul": "EW"}
stdout: {"table": {"N": {"C": 8, "D": 8, "H": 6, "S": 4, "NT": 6}, ...},
         "par_score": 90, "par_contracts": ["2♦N=", ...]}   (par score is for N-S)
"""
import json
import sys

from endplay.dds import calc_dd_table, par
from endplay.types import Deal, Denom, Player, Vul

PLAYERS = {"N": Player.north, "E": Player.east, "S": Player.south, "W": Player.west}
DENOMS = {"C": Denom.clubs, "D": Denom.diamonds, "H": Denom.hearts, "S": Denom.spades, "NT": Denom.nt}
VULS = {"None": Vul.none, "NS": Vul.ns, "EW": Vul.ew, "Both": Vul.both}


def main() -> None:
    req = json.load(sys.stdin)
    h = req["hands"]
    deal = Deal("N:" + " ".join(h[p] for p in "NESW"))
    table = calc_dd_table(deal)
    out = {"table": {p: {d: table[DENOMS[d], PLAYERS[p]] for d in DENOMS} for p in "NESW"}}
    par_list = par(table, VULS[req.get("vul", "None")], PLAYERS[req.get("dealer", "N")])
    out["par_score"] = par_list.score
    out["par_contracts"] = [str(c) for c in par_list]
    sys.stdout.reconfigure(encoding="utf-8")
    json.dump(out, sys.stdout, ensure_ascii=False)


if __name__ == "__main__":
    main()
