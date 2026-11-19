"""Easy Bidding - the four-page partnership card (A4, large print). Usage: python -X utf8 card.py OUT.docx"""
import sys
from docbuild import new_doc, para, heading, table, box

S = 12      # body size
H = 14      # heading size
W2 = [4.2, 14.2]


def build(out):
    doc = new_doc(S, 1.3)
    para(doc, "EASY BIDDING", 22, True, "center", 0)
    para(doc, "A simple bridge system for new players  ·  Partnership card", 12, False, "center", 2)
    para(doc, "Partner 1: ______________________     Partner 2: ______________________", 11, False, "center", 6)

    box(doc, "THE FOUR NUMBERS", [
        "**6** points → you may answer partner     **12** points → you may open",
        "**25** points together → game (3NT, 4♥, 4♠)     **33** together → slam",
        "Count: Ace = 4, King = 3, Queen = 2, Jack = 1.   Balanced = no void, no singleton, at most one doubleton.",
    ], S)

    box(doc, "THE LADDER  (how strong is my answer?)", [
        "**0–5**  Pass     **6–9**  STEP: the lowest bid     **10–12**  JUMP: one level higher = invitation",
        "**13+**  GAME: bid game, or bid a new suit and keep going until game",
    ], S, fill="E3F1E3")

    heading(doc, "OPENING BIDS", H, 4)
    table(doc, [
        ["Bid", "Meaning"],
        ["1♣ / 1♦", "12–21, no 5-card major. Open the longer minor. 3-3 → 1♣, 4-4 → 1♦"],
        ["1♥ / 1♠", "12–21, 5+ cards. Two 5-card suits → open the higher"],
        ["1NT", "15–17, balanced (a 5-card major is allowed)"],
        ["2♣", "22+, any hand. The ONLY artificial opening"],
        ["2♦ / 2♥ / 2♠", "WEAK: 6 cards, 6–10 points"],
        ["2NT", "20–21, balanced"],
        ["3 of a suit", "WEAK: 7 cards, 6–10 points"],
    ], W2, S)

    heading(doc, "ANSWERING 1♥ OR 1♠  (support first!)", H, 2)
    table(doc, [
        ["Answer", "Meaning"],
        ["Raise to 2", "6–9, 3+ cards in partner's major"],
        ["Raise to 3", "10–12, 3+ cards (invitation)"],
        ["Raise to 4", "13+, 3+ cards (game)"],
        ["1♠ over 1♥", "6+, 4+ spades, no heart support"],
        ["1NT", "6–9, no support"],
        ["New suit at 2", "10+, 4+ cards. Partner must bid again"],
        ["2NT / 3NT", "10–12 / 13–15, balanced, no support"],
    ], W2, S)

    heading(doc, "ANSWERING 1♣ OR 1♦  (majors first!)", H, 2)
    table(doc, [
        ["Answer", "Meaning"],
        ["1♥ / 1♠", "6+, 4+ cards. Two 4-card majors → 1♥ first. 5 spades → 1♠ first"],
        ["1♦ over 1♣", "6+, 4+ diamonds, no 4-card major"],
        ["1NT / 2NT / 3NT", "6–9 / 10–12 / 13–15, balanced, no 4-card major"],
        ["Raise the minor", "2 = 6–9, 3 = 10–12, with 5+ cards"],
        ["2♣ over 1♦", "10+, 4+ clubs. Partner must bid again"],
    ], W2, S)

    # ---------------- page 2 ----------------
    doc.add_page_break()
    heading(doc, "ANSWERING 1NT  (15–17)", H, 0)
    table(doc, [
        ["Answer", "Meaning"],
        ["Pass", "0–7, balanced"],
        ["2♣  STAYMAN", "8+, a 4-card major. Partner: 2♦ = no major, 2♥ = 4 hearts, 2♠ = 4 spades"],
        ["2♦  TRANSFER", "5+ hearts, any points. Partner MUST bid 2♥"],
        ["2♥  TRANSFER", "5+ spades, any points. Partner MUST bid 2♠"],
        ["2♠", "0–7, 6+ clubs or diamonds. Partner MUST bid 3♣: you pass, or bid 3♦"],
        ["2NT", "8–9, invitation, no major (partner bids 3NT with 16–17)"],
        ["3NT", "10–15, no major"],
        ["6NT", "18–19 (15 + 18 = 33)"],
    ], W2, S)
    para(doc, "**After Stayman:** fit → raise (8–9 → 3 of the major, 10+ → 4). No fit → 2NT (8–9) or 3NT (10+).", S)
    para(doc, "**Transfer = bid the suit just BELOW your long major.** Partner says your suit for you.", S)

    heading(doc, "AFTER THE TRANSFER  (partner has bid your major)", H, 4)
    table(doc, [
        ["You have", "Your second bid"],
        ["0–7", "Pass"],
        ["8–9, 5 cards", "2NT. Partner with 15: pass (2 cards) or 3 of the major (3 cards). With 16–17: 3NT (2 cards) or 4 of the major (3 cards)"],
        ["8–9, 6+ cards", "3 of the major (invitation)"],
        ["10–15, 5 cards", "3NT. Partner: pass with 2 cards, 4 of the major with 3+"],
        ["10–15, 6+ cards", "4 of the major"],
    ], W2, S)

    heading(doc, "OTHER OPENINGS: HOW TO ANSWER", H, 6)
    table(doc, [
        ["Partner opened", "You answer"],
        ["2♣  (22+)", "ALWAYS 2♦ (any hand). Then: opener's 2NT = 22–24 balanced (pass with 0–2, otherwise answer as after 2NT). A suit = 5+ cards, keep bidding until game"],
        ["2NT  (20–21)", "0–4 pass.  5+: 3♣ Stayman (4-card major), 3♦ / 3♥ TRANSFER (5+ hearts / spades), else 3NT.  12+: 6NT.  After the transfer: 5 cards → 3NT, 6+ cards → 4 of the major"],
        ["Weak 2 / weak 3", "Usually PASS. 3-card support → raise one level (to block). 16+ with support → game"],
    ], [4.2, 14.2], S)

    # ---------------- page 3 ----------------
    doc.add_page_break()
    heading(doc, "OPENER'S SECOND BID", H, 0)
    table(doc, [
        ["Opener has", "What to do"],
        ["12–14  minimum", "The lowest natural bid: 1NT, rebid a 6-card suit, raise partner one level, a new suit at the 1 level"],
        ["15–17  medium", "JUMP: raise partner to 3, jump in your 6-card suit"],
        ["18–21  strong", "Balanced 18–19 → jump to 2NT. With a fit → raise partner to game"],
        ["After a raise", "1♠–2♠: pass with 12–14, 3♠ with 15–17, 4♠ with 18+.   1♠–3♠: 4♠ with 14+"],
    ], [4.2, 14.2], S)
    para(doc, "**Golden rule:** a NEW SUIT from partner is a question - always answer it, never pass.", S)

    heading(doc, "WHEN THE OPPONENTS OPEN", H, 6)
    table(doc, [
        ["Our bid", "Meaning"],
        ["Overcall at 1 level", "8–16, 5+ cards"],
        ["Overcall at 2 level", "10–16, 5+ good cards. Partner raises with 3+ cards and 6+ points"],
        ["1NT overcall", "15–18, balanced, a stopper in their suit. Same answers as after our 1NT"],
        ["Double", "TAKEOUT: 12+, short in their suit, support for the other suits (or 17+ any hand)"],
        ["Partner of doubler", "MUST bid, even with 0. 0–8 cheapest bid in your longest suit (major first), 9–11 jump, 12+ game"],
    ], [4.2, 14.2], S)
    para(doc, "**Double rule:** a double is for TAKEOUT only when the opponents opened a suit and partner has not bid yet. Every other double is for PENALTY.", S)

    heading(doc, "SLAM: BLACKWOOD 4NT  (\"how many aces?\")", H, 2)
    para(doc, "5♣ = 0 or 4 aces     5♦ = 1     5♥ = 2     5♠ = 3", S, True)
    para(doc, "Two aces missing → stop at 5. One ace missing → small slam. Use 4NT only with 33+ together and an agreed suit. After our 1NT/2NT we never bid 4NT: we bid 6NT.", S)

    # ---------------- page 4 ----------------
    doc.add_page_break()
    heading(doc, "LEADS AND SIGNALS", H, 0)
    para(doc, "**Leads:** partner's suit first.  Top of a sequence (K from K-Q-J).  Top of a doubleton.  Against NT: 4th card from your longest suit.", S)
    para(doc, "**Signals:** HIGH card = \"I like this suit, continue\".  LOW card = \"I don't like it\".", S)

    heading(doc, "ON BBO: ALERT THESE BIDS", H, 2)
    table(doc, [
        ["Bid", "Type this explanation"],
        ["2♣ opening", "Strong, 22+, any hand"],
        ["2♦ answer to 2♣", "Waiting, any hand"],
        ["Weak 2♦/2♥/2♠", "Weak, 6 cards, 6-10"],
        ["2♣ / 3♣ over our NT", "Stayman, asks for a 4-card major"],
        ["2♦ / 2♥ over 1NT,\n3♦ / 3♥ over 2NT", "Transfer: 5+ hearts / 5+ spades"],
        ["2♠ over 1NT", "Weak, long minor: partner must bid 3♣"],
        ["Raise 1♥–4♥, 1♠–4♠", "Game values, 13+ (not weak)"],
        ["Double after partner opened", "Penalty"],
    ], [7.4, 11.0], S)
    doc.save(out)


if __name__ == "__main__":
    build(sys.argv[1])
