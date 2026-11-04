import random
import unittest

from bridge_analyzer.analysis import (
    analyze_board,
    declarer_side_tricks,
    duplicate_score,
    hcp,
    summarize,
)
from bridge_analyzer.lin_tools import CLOCKWISE, RANK_ORDER, parse_lin
from bridge_analyzer.analysis import play_log
from bridge_analyzer.report import board_report, play_report, solver_report
from bridge_analyzer.solver import solve, solver_python


class ScoreTests(unittest.TestCase):
    def test_known_scores(self):
        cases = [
            # level, strain, doubled, tricks, vul, expected
            (3, "NT", 0, 9, False, 400),
            (4, "H", 0, 10, True, 620),
            (4, "H", 0, 11, True, 650),
            (2, "S", 0, 8, False, 110),
            (1, "NT", 1, 7, False, 180),
            (6, "NT", 0, 12, True, 1440),
            (7, "NT", 0, 13, False, 1520),
            (5, "C", 0, 11, False, 400),
            (4, "S", 0, 9, False, -50),
            (4, "S", 0, 8, True, -200),
            (4, "S", 1, 8, True, -500),
            (4, "S", 1, 7, False, -500),
            (4, "S", 1, 6, False, -800),
            (4, "S", 2, 8, False, -600),
            (2, "H", 1, 8, False, 470),   # doubled, made exactly
            (2, "H", 1, 9, False, 570),   # doubled +1 non-vul
            (2, "H", 2, 8, True, 840),    # redoubled, made, vul
        ]
        for level, strain, dbl, tricks, vul, expected in cases:
            with self.subTest(level=level, strain=strain, dbl=dbl, tricks=tricks, vul=vul):
                self.assertEqual(duplicate_score(level, strain, dbl, tricks, vul), expected)


class TrickTests(unittest.TestCase):
    def test_trump_beats_led_suit_and_winner_leads_next(self):
        deal = _deal(seed=1)
        plays, expected = _simulate(deal, declarer="S", strain="H", seed=2)
        self.assertEqual(declarer_side_tricks(plays, "S", "H"), expected)

    def test_ruff_and_running_count(self):
        # Declarer S, W leads. Trump H. Trick 1: W leads C5, N ruffs H2, E C7, S C2 -> N wins.
        # Trick 2 led by N: S5 S6 SA S2 -> S wins. N is dummy, so both tricks are the declaring side's.
        log = play_log(["C5", "H2", "C7", "C2", "S5", "S6", "SA", "S2"], "S", "H")
        self.assertEqual([t.winner for t in log], ["N", "S"])
        self.assertEqual(log[0].ruffers, ["N"])
        self.assertEqual([t.declarer_won for t in log], [1, 2])

    def test_play_report_with_claim(self):
        deal = _deal(7)
        plays, _ = _simulate(deal, declarer="S", strain="H", seed=8)
        lin = _lin(deal, plays[:32], bid="3H") + "mc|9|"
        a = analyze_board(parse_lin(lin), lin)
        text = play_report(a, "steffl54")
        self.assertIn("Opening lead: West", text)
        self.assertIn("Play stopped after 8 tricks; claim gave declarer", text)
        self.assertEqual(len(a.tricks), 8)

    def test_incomplete_play_is_unknown(self):
        self.assertIsNone(declarer_side_tricks(["SA", "S2", "S3", "S4"], "S", "NT"))


class SolverTests(unittest.TestCase):
    LIN = ("pn|steffl54,W,N,E|md|2SQ63H7DQT85CA9432,SKJ542HKJ82DK2CJ5,SA7H96543DAJ97CT8|"
           "sv|e|mb|1S|mb|p|mb|1N|mb|p|mb|2H|mb|p|mb|3S|mb|p|mb|4S|mb|p|mb|p|mb|p|mc|8|")

    def test_report_from_table(self):
        a = analyze_board(parse_lin(self.LIN), self.LIN)
        dd = {"table": {p: {d: 7 for d in ("C", "D", "H", "S", "NT")} for p in "NESW"},
              "par_score": 90, "par_contracts": ["2D N="]}
        text = solver_report(a, dd)
        self.assertIn("double dummy gives 7 - down 3 at best defense", text)
        self.assertIn("Actual result 8 tricks: 1 trick better than double dummy", text)

    def test_missed_game_note(self):
        lin = self.LIN.replace("mb|4S", "mb|2S")  # West ends in 2S
        a = analyze_board(parse_lin(lin), lin)
        dd = {"table": {p: {d: 10 for d in ("C", "D", "H", "S", "NT")} for p in "NESW"},
              "par_score": 0, "par_contracts": []}
        self.assertIn("a game was available", solver_report(a, dd))
        dd["table"]["W"]["S"] = 8
        self.assertNotIn("Missed", solver_report(a, dd))

    def test_missed_slam_note(self):
        a = analyze_board(parse_lin(self.LIN), self.LIN)  # 4S by West
        dd = {"table": {p: {d: 12 for d in ("C", "D", "H", "S", "NT")} for p in "NESW"},
              "par_score": 0, "par_contracts": []}
        self.assertIn("Missed: double dummy gives 12 tricks, so a slam was available", solver_report(a, dd))
        dd["table"]["W"]["S"] = 10
        self.assertNotIn("Missed", solver_report(a, dd))

    @unittest.skipUnless(solver_python().exists(), "endplay solver env not installed")
    def test_real_solver_board_16(self):
        dd = solve(parse_lin(self.LIN))
        self.assertEqual(dd["table"]["W"]["S"], 7)
        self.assertEqual(dd["table"]["N"]["C"], 8)
        self.assertEqual(dd["par_score"], 90)


class BoardTests(unittest.TestCase):
    def test_full_board_matches_independent_simulation(self):
        for seed in range(20):
            deal = _deal(seed)
            strain = random.Random(seed).choice(["NT", "S", "H", "D", "C"])
            plays, expected = _simulate(deal, declarer="S", strain=strain, seed=seed + 100)
            lin = _lin(deal, plays, bid=f"3{strain}")
            board = parse_lin(lin)
            a = analyze_board(board, lin)
            self.assertEqual(a.declarer_tricks, expected, f"seed {seed}")
            self.assertEqual(a.tricks_source, "play")
            self.assertEqual(a.role, "declarer")
            self.assertEqual(sum(a.hcp.values()), 40)

    def test_claim_overrides_play_and_missing_result_is_none(self):
        deal = _deal(3)
        lin = _lin(deal, [], bid="3NT")
        a = analyze_board(parse_lin(lin), lin)
        self.assertIsNone(a.declarer_tricks)
        self.assertIsNone(a.declarer_score)
        a = analyze_board(parse_lin(lin + "mc|10|"), lin + "mc|10|")
        self.assertEqual((a.declarer_tricks, a.tricks_source), (10, "claim"))
        self.assertEqual(a.declarer_score, 430)  # 3NT +1 non-vul

    def test_report_never_leaks_other_usernames(self):
        deal = _deal(4)
        plays, _ = _simulate(deal, declarer="S", strain="NT", seed=5)
        lin = _lin(deal, plays, bid="3NT")
        a = analyze_board(parse_lin(lin), lin)
        text = board_report(a, "steffl54")
        for secret in ("secretW", "secretN", "secretE"):
            self.assertNotIn(secret, text)
        self.assertIn("by South (steffl54)", text)

    def test_passed_out_and_summary(self):
        deal = _deal(6)
        lin = _lin(deal, [], bid=None)
        a = analyze_board(parse_lin(lin), lin)
        self.assertIsNone(a.board.contract)
        s = summarize([a])
        self.assertEqual((s.boards, s.passed_out), (1, 1))

    def test_hcp(self):
        self.assertEqual(hcp({"S": ["A", "K"], "H": ["Q"], "D": ["J", "T"], "C": []}), 10)


# --- synthetic LIN builder -------------------------------------------------

def _deal(seed):
    cards = [s + r for s in "SHDC" for r in RANK_ORDER]
    random.Random(seed).shuffle(cards)
    return {pos: cards[i * 13 : (i + 1) * 13] for i, pos in enumerate(CLOCKWISE)}


def _simulate(deal, declarer, strain, seed):
    """Random legal play with an independently computed winner (numeric ranks)."""
    rng = random.Random(seed)
    trump = None if strain == "NT" else strain
    hands = {p: list(c) for p, c in deal.items()}
    rank = lambda c: 14 - RANK_ORDER.index(c[1])
    leader = CLOCKWISE[(CLOCKWISE.index(declarer) + 1) % 4]
    plays, decl_tricks = [], 0
    for _ in range(13):
        trick = []
        for k in range(4):
            p = CLOCKWISE[(CLOCKWISE.index(leader) + k) % 4]
            if trick:
                follow = [c for c in hands[p] if c[0] == trick[0][1][0]]
            else:
                follow = []
            card = rng.choice(follow or hands[p])
            hands[p].remove(card)
            trick.append((p, card))
            plays.append(card)
        led = trick[0][1][0]
        key = lambda pc: (pc[1][0] == trump, pc[1][0] == led, rank(pc[1]))
        leader = max(trick, key=key)[0]
        if leader in (declarer, CLOCKWISE[(CLOCKWISE.index(declarer) + 2) % 4]):
            decl_tricks += 1
    return plays, decl_tricks


def _lin(deal, plays, bid):
    def hand(pos):
        out = ""
        for s in "SHDC":
            out += s + "".join(c[1] for c in deal[pos] if c[0] == s)
        return out

    md = "3" + ",".join(hand(p) for p in ("S", "W", "N", "E"))  # dealer N, order S,W,N,E
    if bid is None:
        auction = ["p"] * 4
    else:
        auction = ["p", "p", bid.replace("NT", "N"), "p", "p", "p"]  # N,E pass, S bids
    parts = ["pn|steffl54,secretW,secretN,secretE", f"md|{md}", "sv|o"]
    parts += [f"mb|{c}" for c in auction]
    parts += [f"pc|{c}" for c in plays]
    return "|".join(parts) + "|"


if __name__ == "__main__":
    unittest.main()
