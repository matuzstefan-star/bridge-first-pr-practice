"""One PNG per player hand (North and South), to send separately on WhatsApp."""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

import bridzs_doc
import lecke2
from bridzs_doc import SUITS, SYM, HCP, hu, parse

FONTS = r"C:\Windows\Fonts"
TEXT = ImageFont.truetype(os.path.join(FONTS, "segoeui.ttf"), 34)
TEXT_B = ImageFont.truetype(os.path.join(FONTS, "segoeuib.ttf"), 44)
CARD = ImageFont.truetype(os.path.join(FONTS, "segoeuib.ttf"), 64)
SUIT = ImageFont.truetype(os.path.join(FONTS, "seguisym.ttf"), 64)
SMALL = ImageFont.truetype(os.path.join(FONTS, "segoeui.ttf"), 30)

NAVY, RED, BLACK, GREY = (31, 56, 100), (192, 0, 0), (20, 20, 20), (110, 110, 110)
SEATS = {"N": ("Észak", "Eszak"), "S": ("Dél", "Del")}  # display name, file-safe name


def card(lesson, num, deal, seat, path):
    img = Image.new("RGB", (900, 760), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([12, 12, 887, 747], outline=NAVY, width=4)
    d.text((50, 40), f"{lesson}. lecke · {num}. leosztás", font=TEXT, fill=GREY)
    d.text((50, 90), f"A te lapjaid – {SEATS[seat][0]}", font=TEXT_B, fill=NAVY)
    d.text((50, 150), f"Osztó: {deal['dealer']}", font=SMALL, fill=GREY)
    hand = parse(deal[seat])
    y = 220
    for s in SUITS:
        colour = RED if s in "HD" else BLACK
        d.text((70, y), SYM[s], font=SUIT, fill=colour)
        d.text((160, y), hu(hand[s]), font=CARD, fill=BLACK)
        y += 105
    pts = sum(HCP.get(c, 0) for c in deal[seat].replace(" ", ""))
    d.text((50, 675), f"{pts} figurapont", font=SMALL, fill=GREY)
    img.save(path)


SEAT_NAMES = {"N": "Észak", "S": "Dél", "W": "Nyugat", "E": "Kelet"}


def hand_block(d, x, y, seat, deal, title_font=SMALL):
    d.text((x, y), SEAT_NAMES[seat], font=TEXT_B, fill=NAVY)
    hand = parse(deal[seat])
    for i, s in enumerate(SUITS):
        yy = y + 60 + i * 62
        d.text((x, yy), SYM[s], font=SUIT_M, fill=RED if s in "HD" else BLACK)
        d.text((x + 60, yy), hu(hand[s]), font=CARD_M, fill=BLACK)
    pts = sum(HCP.get(c, 0) for c in deal[seat].replace(" ", ""))
    d.text((x, y + 60 + 4 * 62 + 5), f"{pts} fp", font=SMALL, fill=GREY)


SUIT_M = ImageFont.truetype(os.path.join(FONTS, "seguisym.ttf"), 44)
CARD_M = ImageFont.truetype(os.path.join(FONTS, "segoeuib.ttf"), 44)


def teacher(lesson, num, deal, student, path):
    """The full deal, for the teacher."""
    img = Image.new("RGB", (1300, 1180), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([12, 12, 1287, 1167], outline=NAVY, width=4)
    d.text((50, 35), f"{lesson}. lecke · {num}. leosztás – Osztó: {deal['dealer']}", font=TEXT, fill=GREY)
    hand_block(d, 500, 100, "N", deal)
    hand_block(d, 60, 450, "W", deal)
    hand_block(d, 920, 450, "E", deal)
    hand_block(d, 500, 800, "S", deal)
    d.rectangle([470, 470, 830, 760], fill=(232, 240, 232))
    for txt, xy in (("É", (650, 500)), ("Ny", (500, 615)), ("K", (800, 615)), ("D", (650, 730))):
        d.text(xy, txt, font=TEXT_B, fill=NAVY, anchor="mm")
    d.text((650, 615), f"{SEAT_NAMES[student]} = a barátod", font=SMALL, fill=NAVY, anchor="mm")
    img.save(path)


def main(root, student="S"):
    for lesson, deals in ((1, bridzs_doc.DEALS), (2, lecke2.DEALS)):
        out = os.path.join(root, f"Lapok_Lecke_{lesson}")
        os.makedirs(out, exist_ok=True)
        for f in os.listdir(out):
            os.remove(os.path.join(out, f))
        for num, deal in enumerate(deals, 1):
            card(lesson, num, deal, student, os.path.join(out, f"L{lesson}_{num:02d}_barat.png"))
            teacher(lesson, num, deal, student, os.path.join(out, f"L{lesson}_{num:02d}_Steffy.png"))
        print(out, sorted(os.listdir(out))[:2], len(os.listdir(out)))


main(sys.argv[1])
