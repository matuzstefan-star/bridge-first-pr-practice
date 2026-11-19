"""Easy Bidding - the explanation booklet with examples and a quiz. Usage: python -X utf8 booklet.py OUT.docx"""
import sys
from docbuild import new_doc, para, heading, table, box, check_hand, hand_line

S = 13
H1 = 18
H2 = 14


def example(doc, hand, hcp, text):
    check_hand(hand, hcp)
    para(doc, hand_line(hand) + f"     ({hcp} points)", S, True, after=1).paragraph_format.keep_with_next = True
    para(doc, text, S, after=6)


# Quiz: (situation, hand, HCP, answer, why)
QUIZ = [
    ("You are the dealer.", "AQ864 K72 Q5 J83", 12, "1♠",
     "12 points and 5 spades. A 5-card major is opened at the 1 level."),
    ("You are the dealer.", "K73 AJ4 KQ82 A95", 17, "1NT",
     "17 points and a balanced hand (4-3-3-3): 15–17 balanced is always 1NT."),
    ("You are the dealer.", "94 KQJ975 83 T62", 6, "2♥",
     "Only 6 points, but 6 good hearts: a weak two."),
    ("Partner opens 1♥.", "K84 Q73 J962 Q85", 8, "2♥",
     "Support first. 3 hearts and 6–9 points → STEP: raise to 2♥."),
    ("Partner opens 1♥.", "A85 K962 KJ4 863", 11, "3♥",
     "Heart support and 10–12 points → JUMP: 3♥ invites partner to game."),
    ("Partner opens 1♥.", "KQ3 52 AQT86 K74", 14, "2♦",
     "No heart support (only 2). 10+ points → new suit at the 2 level. Partner must bid again, and with 14 you will make sure you reach game."),
    ("Partner opens 1♠.", "Q4 72 K863 AQ952", 11, "2♣",
     "Only 2 spades: no support. 11 points → new suit at the 2 level, your longest suit."),
    ("Partner opens 1♦.", "KJ75 83 Q64 J972", 7, "1♠",
     "Majors first! 7 points and 4 spades → 1♠, even with only a 4-card suit."),
    ("Partner opens 1NT.", "KJ84 A62 Q73 952", 10, "2♣ (Stayman)",
     "10 points and 4 spades. If partner answers 2♠ → bid 4♠. If 2♦ or 2♥ → bid 3NT."),
    ("Partner opens 1NT.", "J97642 83 Q5 742", 3, "2♥ (transfer)",
     "A weak hand with 6 spades. Bid 2♥, partner must bid 2♠, and you pass. Much safer than 1NT."),
    ("Partner opens 1NT.", "KQ864 A73 J52 84", 10, "2♥ (transfer), then 3NT",
     "5 spades and 10 points. After partner's 2♠ bid 3NT: partner passes with 2 spades or bids 4♠ with 3."),
    ("Partner opens 2♣.", "952 J84 Q763 842", 3, "2♦",
     "After 2♣ we ALWAYS answer 2♦, whatever we hold."),
    ("Partner opens a weak 2♥.", "AK5 Q83 AK72 K64", 19, "4♥",
     "19 points and 3 hearts: 16+ with support → bid game."),
    ("The opponent on your right opens 1♦.", "KJ93 AQ84 5 K962", 13, "Double",
     "13 points, short in diamonds, 4 cards in every other suit: a perfect takeout double."),
    ("The opponent on your right opens 1♣.", "AQJ84 K63 752 84", 10, "1♠",
     "10 points and a good 5-card suit: overcall at the 1 level."),
    ("You opened 1♠ and partner raised to 2♠.", "AKJ85 KQ4 A62 73", 17, "3♠",
     "15–17 after a raise → invite with 3♠. Partner bids 4♠ with 8–9, passes with 6–7."),
]


def build(out):
    doc = new_doc(S, 2.0)

    # ---------- cover ----------
    para(doc, "", S, after=60)
    para(doc, "EASY BIDDING", 34, True, "center", 6)
    para(doc, "A simple bridge system for new players", 18, False, "center", 30)
    para(doc, "Few rules  ·  Natural bids  ·  Easy to remember", 15, False, "center", 6)
    para(doc, "For players who enjoy bridge on BBO and want a system they can keep in their head.", 13, False, "center", 80)
    para(doc, "by Steffy (Ştefan Matuz)", 14, True, "center", 0)
    doc.add_page_break()

    # ---------- intro ----------
    heading(doc, "Why this system?", H1, 0)
    para(doc, "Modern systems such as 2/1, Strong Club or Polish Club are excellent, but they ask you to remember dozens of agreements. If you forget one at the table, you and your partner end up in the wrong contract and the fun is gone.", S)
    para(doc, "Easy Bidding has the opposite goal: **you remember everything**. It is built on three ideas:", S)
    para(doc, "1.  **Bid what you have.** Almost every bid is natural: if you bid hearts, you have hearts.", S)
    para(doc, "2.  **The same numbers everywhere.** 6 – 12 – 25 – 33, and the Ladder 6–9 / 10–12 / 13+.", S)
    para(doc, "3.  **Only five agreements to learn:** the strong 2♣, the weak twos, Stayman, transfers and Blackwood.", S)
    para(doc, "Keep the two-page partnership card on the table, or next to your screen when you play on BBO. After a few weeks you will not need it.", S, after=10)

    # ---------- 1 ----------
    heading(doc, "1.  Counting your hand", H1)
    para(doc, "We count only high-card points: **Ace = 4, King = 3, Queen = 2, Jack = 1**. The whole pack has 40 points, so an average hand has 10.", S)
    para(doc, "A hand is **balanced** when it has no void, no singleton and at most one doubleton. There are only three balanced shapes: **4-3-3-3, 4-4-3-2 and 5-3-3-2**.", S)
    box(doc, "Remember: the four numbers", [
        "**6** points: you may answer partner.     **12** points: you may open.",
        "**25** points together: bid game (3NT, 4♥ or 4♠).     **33** together: bid slam.",
    ], S)
    example(doc, "KQ5 A84 J963 Q72", 12, "Balanced (4-3-3-3 shape), 12 points: just enough to open.")

    # ---------- 2 ----------
    heading(doc, "2.  Opening the bidding", H1)
    para(doc, "With fewer than 12 points, pass (except for the weak openings below). With 12 or more, follow this order:", S)
    table(doc, [
        ["Ask yourself", "Then open"],
        ["22 points or more?", "2♣ (strong, any hand)"],
        ["Balanced with 15–17?  20–21?", "1NT  /  2NT"],
        ["A 5-card major?", "1♥ or 1♠ (two 5-card suits: the higher)"],
        ["None of these?", "1♣ or 1♦: the longer minor (3-3 → 1♣, 4-4 → 1♦)"],
    ], [7.0, 10.0], S)
    para(doc, "**Weak openings** (6–10 points): with a good 6-card suit open 2♦, 2♥ or 2♠; with a good 7-card suit open at the 3 level. They make life hard for the opponents and tell partner \"I have a long suit and a weak hand\". There is no weak 2♣ - 2♣ is always strong.", S)
    example(doc, "AQ864 K72 Q5 J83", 12, "Open **1♠**: 12 points and five spades.")
    example(doc, "K72 AJ4 Q83 AJ62", 15, "Open **1NT**: 15 points, balanced.")
    example(doc, "AJ5 K4 Q873 KJ62", 14, "Open **1♦**: no 5-card major, 4-4 in the minors → 1♦. You will rebid 1NT to show 12–14 balanced.")

    # ---------- 3 ----------
    heading(doc, "3.  Answering partner: the Ladder", H1)
    para(doc, "Every time partner opens one of a suit, find your rung on the Ladder:", S)
    box(doc, "THE LADDER", [
        "**0–5**  Pass.",
        "**6–9**  STEP: make the lowest sensible bid.",
        "**10–12**  JUMP: bid one level higher than needed. This is an invitation: \"partner, bid game if you have more than a minimum\".",
        "**13+**  GAME: bid game directly, or bid a new suit and keep bidding until you reach game.",
    ], S, fill="E3F1E3")
    heading(doc, "When partner opens 1♥ or 1♠: support first", H2)
    para(doc, "With 3 or more cards in partner's major you have found an 8-card fit. Say so at once: **2** with 6–9, **3** with 10–12, **4** with 13+. Without support, bid 1♠ over 1♥ with four spades, a new suit at the 2 level with 10+, or no-trumps (1NT 6–9, 2NT 10–12, 3NT 13–15).", S)
    heading(doc, "When partner opens 1♣ or 1♦: majors first", H2)
    para(doc, "Partner may have only three cards in the minor, so look for a major fit first. With a 4-card major bid it at the 1 level (two 4-card majors → 1♥ first; five spades → 1♠ first). Without a major, bid no-trumps with a balanced hand or raise partner's minor with 5+ cards.", S)
    box(doc, "Golden rule", [
        "A **new suit** from partner is a question. Always answer it - never pass.",
    ], S)

    # ---------- 4 ----------
    heading(doc, "4.  The opener's second bid", H1)
    para(doc, "The opener's first bid said \"12–21\". The second bid says which part:", S)
    table(doc, [
        ["Opener has", "Second bid"],
        ["12–14  minimum", "The lowest natural bid: 1NT (balanced), rebid a 6-card suit, raise partner one level with 4 cards, or a new suit at the 1 level"],
        ["15–17  medium", "JUMP: raise partner to 3, or jump in your own 6-card suit"],
        ["18–21  strong", "Balanced 18–19 → jump to 2NT. With a fit → raise partner to game"],
    ], [4.5, 12.5], S)
    para(doc, "When partner has **raised** your major: 1♠–2♠ → pass with 12–14, 3♠ with 15–17, 4♠ with 18+. 1♠–3♠ → bid 4♠ with 14 or more.", S)

    # ---------- 5 ----------
    heading(doc, "5.  No-trump openings: Stayman and transfers", H1)
    para(doc, "After partner's 1NT (15–17) you know almost exactly how many points you have together. Just add:", S)
    table(doc, [
        ["You have", "You bid"],
        ["0–7", "Pass. With 5+ hearts or spades: transfer, then pass. With 6+ clubs or diamonds: 2♠, then pass 3♣ or bid 3♦"],
        ["8–9", "2NT (invitation). With a 4-card major: 2♣ Stayman first. With a 5-card major: transfer first"],
        ["10–15", "3NT. With a 4-card major: 2♣ Stayman first. With a 5-card major: transfer first"],
        ["18–19", "6NT"],
    ], [3.5, 13.5], S)
    para(doc, "**Stayman (2♣)** asks: \"do you have a 4-card major?\" Partner answers 2♦ (no), 2♥ (four hearts) or 2♠ (four spades). If you find a fit, raise; if not, return to no-trumps.", S)
    para(doc, "**Transfers (2♦ and 2♥):** with five or more hearts bid 2♦, with five or more spades bid 2♥ - the suit just below yours. Partner MUST bid your suit. This way the strong 1NT hand becomes declarer and the opening lead comes up to its honours.", S)
    box(doc, "Easy way to remember", [
        "Bid the suit just **BELOW** your long major. Partner says your suit for you.",
    ], S)
    table(doc, [
        ["After the transfer you have", "Your second bid"],
        ["0–7", "Pass"],
        ["8–9", "5 cards: 2NT.  6+ cards: 3 of the major (invitation)"],
        ["10–15", "5 cards: 3NT (partner bids 4 of the major with 3+ cards).  6+ cards: 4 of the major"],
    ], [6.0, 11.0], S)
    para(doc, "With a weak hand and a long **minor** bid 2♠: partner must answer 3♣, and you pass or bid 3♦.", S)
    para(doc, "After a **2NT opening** (and after 2♣–2♦–2NT) everything works the same, one level higher: 3♣ is Stayman, 3♦ and 3♥ are transfers.", S)
    example(doc, "KQ864 A73 J52 84", 10, "Partner opens 1NT. Bid **2♥** (transfer). Partner bids 2♠; you bid **3NT**. Partner passes with 2 spades or bids 4♠ with 3.")
    example(doc, "KJ84 A62 Q73 952", 10, "Partner opens 1NT. Bid **2♣**. If partner says 2♠ → 4♠. Otherwise → 3NT.")

    # ---------- 6 ----------
    heading(doc, "6.  The strong 2♣ and the weak openings", H1)
    para(doc, "**2♣** shows 22 or more points. Partner always answers **2♦**, whatever the hand - this keeps the bidding low so the strong hand can describe itself. Then opener bids 2NT with 22–24 balanced (the only time you may stop below game, with 0–2 points), otherwise bids a 5-card suit. From then on, keep bidding until game.", S)
    para(doc, "**Weak twos and threes:** partner has a long suit and 6–10 points. Usually you pass. With 3-card support raise one level - not to make it, but to take bidding space away from the opponents. With 16+ and support bid game.", S)

    # ---------- 7 ----------
    heading(doc, "7.  When the opponents open", H1)
    table(doc, [
        ["Bid", "Meaning"],
        ["Overcall at the 1 level", "8–16, 5+ cards"],
        ["Overcall at the 2 level", "10–16, 5+ good cards"],
        ["1NT overcall", "15–18, balanced, a stopper in their suit"],
        ["Double", "12+, short in their suit, support for the other three suits (or 17+ any hand)"],
    ], [5.5, 11.5], S)
    para(doc, "After partner's **takeout double** you must bid, even with 0 points: 0–8 bid your longest suit as cheaply as possible (a major if you can), 9–11 jump, 12+ bid game.", S)
    box(doc, "The double rule (one rule for all doubles)", [
        "A double is for **TAKEOUT** only when the opponents opened a suit and partner has not bid yet.",
        "**Every other double is for PENALTY:** \"I think they will go down\".",
    ], S)
    example(doc, "KJ93 AQ84 5 K962", 13, "The opponent on your right opens 1♦. **Double**: short diamonds, support for all the other suits.")

    # ---------- 8 ----------
    heading(doc, "8.  Slam with Blackwood", H1)
    para(doc, "When you know you have 33 points together and a fit, bid **4NT** to ask partner how many aces they hold:", S)
    para(doc, "5♣ = 0 or 4 aces      5♦ = 1      5♥ = 2      5♠ = 3", S, True)
    para(doc, "If two aces are missing, stop at the 5 level of your suit. If one is missing, bid the small slam (6). After our 1NT or 2NT opening we never use 4NT - we simply bid 6NT with enough points.", S)

    # ---------- 9 ----------
    heading(doc, "9.  Leads and signals", H1)
    para(doc, "**Opening lead:** partner's suit first. Otherwise lead the top of a sequence (the King from K-Q-J) or the top of a doubleton. Against no-trumps lead the 4th card from your longest suit.", S)
    para(doc, "**Signals:** when partner leads, play a HIGH card if you like the suit and want it continued, a LOW card if you do not.", S)

    # ---------- 10 ----------
    heading(doc, "10.  Playing Easy Bidding on BBO", H1)
    para(doc, "On BBO you alert your OWN bids: click **Alert** in the bidding box before your bid and type the explanation. Alert these:", S)
    table(doc, [
        ["Bid", "Explanation to type"],
        ["2♣ opening", "Strong, 22+, any hand"],
        ["2♦ answer to 2♣", "Waiting, any hand"],
        ["Weak 2♦/2♥/2♠", "Weak, 6 cards, 6-10"],
        ["2♣ / 3♣ over our NT", "Stayman, asks for a 4-card major"],
        ["2♦ / 2♥ over 1NT, 3♦ / 3♥ over 2NT", "Transfer: 5+ hearts / 5+ spades"],
        ["2♠ over 1NT", "Weak, long minor: partner must bid 3♣"],
        ["Raise 1♥–4♥ or 1♠–4♠", "Game values, 13+ (not weak)"],
        ["Double after partner opened", "Penalty"],
    ], [7.0, 10.0], S)
    para(doc, "Our system is close to SAYC (Standard American Yellow Card). When you fill in a convention card on BBO, start from SAYC and write the differences: no Jacoby 2NT, 2♠ over 1NT = weak minor, 2NT answer = 10–12, 4♥/4♠ raise = 13+, 2♦ always after 2♣, penalty doubles. Note: BBO robots play their own system - Easy Bidding is for you and your human partner.", S)

    # ---------- quiz ----------
    doc.add_page_break()
    heading(doc, "11.  Quiz: what do you bid?", H1, 0)
    para(doc, "Cover the answers on the next page and try each hand.", S, after=8)
    for i, (situation, hand, hcp, _, _) in enumerate(QUIZ, 1):
        check_hand(hand, hcp)
        para(doc, f"**{i}.**  {situation}", S, after=1).paragraph_format.keep_with_next = True
        para(doc, "      " + hand_line(hand), S, after=7)
    heading(doc, "Answers", H1, 0).paragraph_format.page_break_before = True
    for i, (_, hand, hcp, answer, why) in enumerate(QUIZ, 1):
        para(doc, f"**{i}.  {answer}**   ({hcp} points)  {why}", S, after=6)
    doc.save(out)


if __name__ == "__main__":
    build(sys.argv[1])
