import sys
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SUITS = "SHDC"
SYM = {"S": "♠", "H": "♥", "D": "♦", "C": "♣"}
RED = RGBColor(0xC0, 0x00, 0x00)
HU_RANK = {"A": "A", "K": "K", "Q": "D", "J": "B", "T": "10"}
HCP = {"A": 4, "K": 3, "Q": 2, "J": 1}
RANKS = "AKQJT98765432"

# Hands as "spades hearts diamonds clubs", English letters, T = 10.
DEALS = [
    dict(
        title="1. leosztás – Válasz 1-es szinten, egyszerű emelés",
        dealer="Észak",
        N="KT73 AQ962 K5 84", S="AQJ85 73 Q84 KJ6",
        W="94 KJT AJT9 QT95", E="62 854 7632 A732",
        auction=["1♥", "passz", "1♠", "passz", "2♠", "passz", "4♠", "passz", "passz", "passz"],
        explain=[
            ("1♥", "12 fp és 5 kör. Főszínt (pikk, kör) csak legalább 5 lappal nyitunk."),
            ("1♠", "Új szín 1-es szinten: 6+ fp, legalább 4 lap, egy körig kényszerítő. Ez a 2/1 rendszerben is pontosan úgy működik, mint régen."),
            ("2♠", "4 lapos pikk támogatás, minimális nyitás (12–15 fp)."),
            ("4♠", "Dél 13 fp + Észak legalább 12 fp = 25+ fp és pikk fit → gém. Szlemre nincs esély, ezért egyenesen 4♠."),
        ],
        lead="♠9 (Nyugat, passzív adu kezdés)",
        play=[
            "Felvevő: Dél. Számold meg a vesztőket: ♦A, ♣A, esetleg egy második treff, és a ♥K helyzete a kérdés.",
            "Két körben húzd ki az adukat (az ellenfeleknél 2-2 az elosztás).",
            "Dél kezéből indíts kis kört az asztal ♥D-ja felé (impassz). A ♥K Nyugatnál van, így a ♥D nyer.",
            "♥A, majd a harmadik kört lopd meg Dél kezében: a kör szín 3-3 volt, az asztal két maradék köre magas. Egy adu bemenettel (♠K) menj át, és dobd el rájuk a vesztő treffet és kárót.",
            "Eredmény: 11 ütés. Csak a ♦A és a ♣A veszít.",
        ],
        lesson="Az 1-es szintű válaszok a 2/1 rendszerben ugyanúgy működnek, mint a hagyományos licitben. Az újdonság a 2-es szintű válaszoknál jön.",
    ),
    dict(
        title="2. leosztás – A kényszerítő 1SZ válasz",
        dealer="Észak",
        N="AKJ74 K6 83 KT85", S="95 QJ83 KJ742 62",
        W="QT8 T975 AT9 J97", E="632 A42 Q65 AQ43",
        auction=["1♠", "passz", "1SZ", "passz", "2♣", "passz", "2♠", "passz", "passz", "passz"],
        explain=[
            ("1♠", "14 fp, 5 pikk."),
            ("1SZ", "Kényszerítő (forcing) 1SZ: 6–12 fp, nincs 3 lapos pikk támogatás. Dél nem mondhat 2♦-t: a 2/1 rendszerben az új szín 2-es szinten gémig kényszerítő, ehhez 7 fp nagyon kevés. 1♥ sem lehetséges, mert az 1♠ felett már nincs 1-es szint."),
            ("2♣", "Észak nem passzolhat (az 1SZ kényszerítő). A 4 lapos treffjét mutatja."),
            ("2♠", "Preferencia: Dél mindkét színben 2 lapos, ezért az 5 lapos pikket választja. Ez nem erőt mutat, csak választást."),
            ("passz", "Északnak minimális nyitása van, megállunk."),
        ],
        lead="♠2 (Kelet)",
        play=[
            "Felvevő: Észak. Várható vesztők: ♠D, ♥A, egy-két káró, két treff.",
            "Fő technika: a treff vesztőket lopd meg az asztalon. Dél két kis aduja (♠9, ♠5) erre való. Ezért korán add le a treffet, és a harmadik treffet lopd meg az asztalon.",
            "A kört az asztal felől játszd a ♥K felé: ha a ♥A Keletnél van, a király ütést hoz.",
            "Reális eredmény: 8 ütés, a 2♠ teljesül. 2SZ vagy 3♠ már túl magas lenne.",
        ],
        lead_note=None,
        lesson="Főszín nyitás után az 1SZ válasz kényszerítő. Így a gyenge válaszadó is el tudja mondani a véleményét, és a nyitó második licitje után megtaláljuk a legjobb részfelvételt.",
    ),
    dict(
        title="3. leosztás – Limitemelés",
        dealer="Észak",
        N="AQT65 KQ7 AJ4 83", S="KJ82 864 KT62 A5",
        W="974 AJT9 987 KQJ", E="3 532 Q53 T97642",
        auction=["1♠", "passz", "3♠", "passz", "4♠", "passz", "passz", "passz"],
        explain=[
            ("1♠", "16 fp, 5 pikk."),
            ("3♠", "Limitemelés: 10–11 fp és 4 lapos pikk. Jelentése: »Partner, ha a nyitásod minimumnál jobb, menj gémbe.«"),
            ("4♠", "Északnak 16 fp-ja van (kb. 14+ fp-tal elfogadjuk a meghívást), ezért gémet licitál."),
        ],
        lead="♣10 (Kelet)",
        play=[
            "Felvevő: Észak. A ♣A-val ütsz az asztalon.",
            "Három körben húzd ki az adukat (Nyugatnál 3 adu van).",
            "Káró: ♦A, majd kis káró Dél ♦K10 felé. Ha Kelet kicsit tesz, a ♦10 nyer (impassz a ♦D ellen). A ♦K után Dél negyedik kárója magas: dobj rá egy vesztőt (♥7 vagy ♣8).",
            "Végül add le a ♥A-t és egy treffet: 11 ütés.",
        ],
        lesson="Az 1♠–2♠ emelés 6–9 fp-t, az 1♠–3♠ limitemelés 10–11 fp-t és 4 lapos fitet jelent. A nyitó dönti el, hogy elfogadja-e a meghívást.",
    ),
    dict(
        title="4. leosztás – A 2/1 válasz és a gyors érkezés elve",
        dealer="Észak",
        N="KQJ873 A5 Q84 72", S="A62 864 KJ3 AJ95",
        W="T95 KQJT T97 864", E="4 9732 A652 KQT3",
        auction=["1♠", "passz", "2♣", "passz", "2♠", "passz", "4♠", "passz", "passz", "passz"],
        explain=[
            ("1♠", "12 fp, 6 pikk."),
            ("2♣", "EZ A 2/1! Új szín 2-es szinten, ugrás nélkül, főszín nyitásra: 12–13+ fp, gémig kényszerítő. Innen kezdve senki sem passzolhat gém előtt, ezért nincs szükség ugrásokra. Dél 3 lapos pikk támogatással először a treffjét mutatja."),
            ("2♠", "6 lapos pikk (vagy egyszerűen nincs jobb licit, minimális kézzel)."),
            ("4♠", "A gyors érkezés elve: mivel a gém forsz már él, az ugrás egyenesen 4♠-be minimális kezet jelez, szlem érdeklődés nélkül. A 3♠ (lassú út) több erőt és szlem érdeklődést mutatna."),
        ],
        lead="♣K (Kelet)",
        play=[
            "Felvevő: Észak. Ütsz a ♣A-val az asztalon.",
            "Három körben húzd ki az adukat, majd üsd ki a ♦A-t.",
            "Vesztők: egy kör, a ♦A és egy treff. Pontosan 10 ütés.",
            "3SZ itt veszélyes lenne: Nyugat ♥KDB10 indítása után a kör szín könnyen elveszhet. A 6-3 pikk fit a biztos út.",
        ],
        lesson="1♠–2♣ / 1♠–2♦ / 1♥–2♣ / 1♥–2♦ / 1♠–2♥ = gémig kényszerítő. Utána: a lassú licit erős, a gyors ugrás a gémbe gyenge (minimális).",
    ),
    dict(
        title="5. leosztás – 2♥ válasz 1♠ nyitásra; a lassú út erősebb",
        dealer="Észak",
        N="AK963 KT52 A4 Q6", S="72 AQJ84 K83 KT5",
        W="QJT8 976 QJT 987", E="54 3 97652 AJ432",
        auction=["1♠", "passz", "2♥", "passz", "3♥", "passz", "4♥", "passz", "passz", "passz"],
        explain=[
            ("1♠", "16 fp, 5 pikk, 4 kör."),
            ("2♥", "2/1 válasz: legalább 5 kör és 12–13+ fp, gémig kényszerítő. (A 2♥ válasz mindig 5+ lapot ígér.)"),
            ("3♥", "Kör fit. Mivel már gém forsz van, a nyitó lassan, 3♥-rel emel: ez extra erőt mutat (a 4♥ minimális kezet jelentene)."),
            ("4♥", "Dél minimális (13 fp), nincs szlem érdeklődése, ezért lezár. 16 + 13 = 29 fp: szlemhez kevés."),
        ],
        lead="♦D (Nyugat, sorozat élről)",
        play=[
            "Felvevő: Dél. Ütsz a ♦A-val az asztalon.",
            "Három körben húzd ki az adukat (Nyugatnál 3 adu van). Az asztalon marad egy adu.",
            "♦K, majd a harmadik kárót lopd meg az asztalon.",
            "A treff vesztőket (♣A és esetleg egy második) a pikk szín felállításával csökkentheted: ♠A, ♠K, majd pikk lopás.",
            "Eredmény: legalább 11 ütés.",
        ],
        lesson="Ha már gém forsz van, nem kell ugrani. Lassú emelés (3♥) = jobb kéz, ugrás a gémbe (4♥) = minimum.",
    ),
    dict(
        title="6. leosztás – 2/1 mellékszín nyitás után: 1♦–2♣",
        dealer="Észak",
        N="KJ4 QT3 AK85 972", S="A62 KJ5 74 AQJ63",
        W="QT98 A98 QJT 854", E="753 7642 9632 KT",
        auction=["1♦", "passz", "2♣", "passz", "2SZ", "passz", "3SZ", "passz", "passz", "passz"],
        explain=[
            ("1♦", "13 fp, egyenletes elosztás. 1SZ-hez (15–17 fp) gyenge, ezért 1♦ (4 lap)."),
            ("2♣", "2/1 válasz 1♦-ra: 12–13+ fp, 5+ treff, gémig kényszerítő."),
            ("2SZ", "Egyenletes elosztás, minimális (12–14 fp) nyitás, fogásokkal a főszínekben."),
            ("3SZ", "Dél 15 fp + Észak 12–14 fp = 27–29 fp: gém, de szlemhez (33 fp) kevés."),
        ],
        lead="♥2 (Kelet, negyedik a legjobb lapjától)",
        play=[
            "Felvevő: Észak. Számold a biztos ütéseket: ♠A, ♠K, ♦A, ♦K = 4. Plusz ütések: treff (5 ütés is lehet) és kör (2 ütés a ♥A kiütése után).",
            "A treff impassz: Észak kezéből indíts ♣9-et! Ha Kelet kicsit tesz, Dél ♣B-vel üt. A ♣K Keletnél van (K10 duplán), a második körben leesik.",
            "Mindig a gyenge kéz felől indíts az erős színhez (Észak → Dél ♣ADB). Bemenetek Északhoz: ♠K, ♦A, ♦K.",
            "Eredmény: 11 ütés.",
        ],
        lesson="Mellékszín nyitás után is érvényes a 2/1: az 1♦–2♣ gémig kényszerítő. A nyitó 2SZ válasza egyenletes elosztású minimumot mutat.",
    ),
    dict(
        title="7. leosztás – 1SZ nyitás és Stayman",
        dealer="Észak",
        N="AQ5 KJ84 KT3 A92", S="86 AT72 QJ54 K84",
        W="KJT9 Q96 987 765", E="7432 53 A62 QJT3",
        auction=["1SZ", "passz", "2♣", "passz", "2♥", "passz", "4♥", "passz", "passz", "passz"],
        explain=[
            ("1SZ", "15–17 fp, egyenletes elosztás (itt 17 fp)."),
            ("2♣", "Stayman: »Van 4 lapos főszíned?« Dél 4 lapos kört keres, és van gém ereje (10 fp)."),
            ("2♥", "4 lapos kör. (2♦ = nincs 4 lapos főszín, 2♠ = 4 pikk, nincs 4 kör.)"),
            ("4♥", "Megvan a 4-4 kör fit és a gém erő."),
        ],
        lead="♣D (Kelet)",
        play=[
            "Felvevő: Észak. Ütsz a ♣A-val.",
            "Adu impassz: Dél ♥A10 felől indíts kört Észak ♥KB felé; ha Nyugat kicsit tesz, a ♥B nyer. A ♥D Nyugatnál van, a harmadik körben leesik.",
            "Pikk impassz ugyanígy, Dél felől a ♠AD felé. A ♠5-öt lopd meg az asztalon.",
            "Üsd ki a ♦A-t: Dél negyedik kárójára eldobhatod Észak vesztő treffjét.",
            "Eredmény: 4♥ kényelmesen teljesül, jó játékkal 12 ütés is lehet.",
        ],
        lesson="1SZ nyitás után a 2♣ (Stayman) 4-4 főszín fitet keres. A 4-4 fit főszínben általában jobb, mint a 3SZ.",
    ),
    dict(
        title="8. leosztás – Jacoby-transzfer",
        dealer="Észak",
        N="KQ4 AK6 J853 QT5", S="AJ973 85 Q6 KJ42",
        W="T86 QJ43 92 A763", E="52 T972 AKT74 98",
        auction=["1SZ", "passz", "2♥", "passz", "2♠", "passz", "3SZ", "passz", "4♠", "passz", "passz", "passz"],
        explain=[
            ("1SZ", "15 fp, egyenletes elosztás."),
            ("2♥", "Jacoby-transzfer: legalább 5 pikket ígér (nem kört!). A nyitónak 2♠-t kell mondania. Ugyanígy: 2♦ = 5+ kör."),
            ("2♠", "Kötelező válasz a transzferre."),
            ("3SZ", "»Pontosan 5 pikkem van és gém erőm. Válassz: 3SZ vagy 4♠.«"),
            ("4♠", "Északnak 3 pikkje van, így megvan az 5-3 fit: a 4♠ biztonságosabb."),
        ],
        lead="♦K (Kelet)",
        play=[
            "Felvevő: Észak. A transzfer előnye: az erős kéz a felvevő, a kezdés felé jön.",
            "Kelet elviszi a ♦K-t és a ♦A-t. A harmadik kárót az asztalon magas aduval (♠B) lopd, hogy Nyugat ne tudjon felüllopni.",
            "Három körben húzd ki az adukat, majd ♥A, ♥K, és a harmadik kört lopd meg az asztalon.",
            "Üsd ki a ♣A-t. Vesztők: ♦A, ♦K, ♣A → 10 ütés.",
            "3SZ-ben a gyenge káró (♦B853 + ♦D6) miatt az ellenfelek elvihetnék a káró ütéseket: a pikk fit a biztos út.",
        ],
        lesson="1SZ után: 2♦ = transzfer körre, 2♥ = transzfer pikkre. Így a partner (az erős kéz) lesz a felvevő.",
    ),
]


def parse(hand):
    return dict(zip(SUITS, hand.split()))


def validate(deals):
    for d in deals:
        seen = set()
        for seat in "NESW":
            h = parse(d[seat])
            n = sum(len(v) for v in h.values())
            assert n == 13, (d["title"], seat, n)
            for s, cards in h.items():
                for c in cards:
                    assert c in RANKS, (d["title"], seat, c)
                    assert (s, c) not in seen, (d["title"], seat, s, c)
                    seen.add((s, c))
        assert len(seen) == 52, d["title"]
        pts = {seat: sum(HCP.get(c, 0) for c in d[seat].replace(" ", "")) for seat in "NESW"}
        print(d["title"], pts)


def hu(cards):
    return " ".join(HU_RANK.get(c, c) for c in cards) if cards else "—"


def shade(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def no_borders(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "nil")
        borders.append(el)
    tblPr.append(borders)


def add_suit_text(par, text, size=None, bold=False):
    """Write text, colouring hearts and diamonds red."""
    buf = ""
    for ch in text:
        if ch in "♥♦":
            if buf:
                r = par.add_run(buf); r.bold = bold
                if size: r.font.size = size
                buf = ""
            r = par.add_run(ch); r.font.color.rgb = RED; r.bold = bold
            if size: r.font.size = size
        else:
            buf += ch
    if buf:
        r = par.add_run(buf); r.bold = bold
        if size: r.font.size = size


def hand_cell(cell, name, hand):
    h = parse(hand)
    p = cell.paragraphs[0]
    r = p.add_run(name); r.bold = True; r.font.size = Pt(10)
    for s in SUITS:
        p = cell.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        sym = p.add_run(SYM[s] + " ")
        if s in "HD":
            sym.font.color.rgb = RED
        p.add_run(hu(h[s]))
    pts = sum(HCP.get(c, 0) for c in hand.replace(" ", ""))
    p = cell.add_paragraph()
    r = p.add_run(f"{pts} fp"); r.italic = True; r.font.size = Pt(9)
    for q in cell.paragraphs:
        q.paragraph_format.space_after = Pt(0)
    r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)


def diagram(doc, d):
    t = doc.add_table(rows=3, cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    no_borders(t)
    widths = [Cm(5), Cm(4), Cm(5)]
    for row in t.rows:
        for i, c in enumerate(row.cells):
            c.width = widths[i]
    hand_cell(t.cell(0, 1), "Észak", d["N"])
    hand_cell(t.cell(1, 0), "Nyugat", d["W"])
    hand_cell(t.cell(1, 2), "Kelet", d["E"])
    hand_cell(t.cell(2, 1), "Dél", d["S"])
    mid = t.cell(1, 1)
    shade(mid, "E8F0E8")
    p = mid.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("É").bold = True
    p = mid.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("Ny        K").bold = True
    p = mid.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run("D").bold = True
    p = mid.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(f"Osztó: {d['dealer']}"); r.font.size = Pt(8)
    for q in mid.paragraphs:
        q.paragraph_format.space_after = Pt(0)


def auction_table(doc, bids):
    # Dealer is always North: West's first cell is empty.
    cells = [""] + bids
    rows = (len(cells) + 3) // 4
    t = doc.add_table(rows=rows + 1, cols=4)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, name in enumerate(["Nyugat", "Észak", "Kelet", "Dél"]):
        c = t.cell(0, i); c.width = Cm(2.6)
        shade(c, "DDE6F0")
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run(name).bold = True
    for idx, b in enumerate(cells):
        c = t.cell(1 + idx // 4, idx % 4); c.width = Cm(2.6)
        p = c.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        ours = (idx % 4) in (1, 3) and b != "passz"
        add_suit_text(p, b, bold=ours)


def para(doc, text="", style=None, bold_prefix=None):
    p = doc.add_paragraph(style=style)
    if bold_prefix:
        add_suit_text(p, bold_prefix, bold=True)
    add_suit_text(p, text)
    return p


def build(deals, out, subtitle, basics_title, basics, extra_gloss=()):
    doc = Document()
    sec = doc.sections[0]
    sec.page_height, sec.page_width = Cm(29.7), Cm(21)
    for m in ("left_margin", "right_margin"):
        setattr(sec, m, Cm(2))
    sec.top_margin = sec.bottom_margin = Cm(1.8)

    normal = doc.styles["Normal"]
    normal.font.name = "Calibri"; normal.font.size = Pt(11)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), "Calibri")
    normal.paragraph_format.space_after = Pt(2)
    for name, size, color in (("Title", 24, "1F3864"), ("Heading 1", 16, "1F3864"), ("Heading 2", 12, "2E5597")):
        st = doc.styles[name]
        st.font.name = "Calibri"; st.font.size = Pt(size); st.font.bold = True
        st.font.color.rgb = RGBColor.from_string(color)
        st.paragraph_format.space_before = Pt(8 if name != "Title" else 0)
        st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.keep_with_next = True

    # --- Intro ---
    doc.add_paragraph("Bridzs újrakezdőknek", style="Title")
    p = doc.add_paragraph()
    r = p.add_run(subtitle)
    r.font.size = Pt(13); r.italic = True
    p = doc.add_paragraph()
    r = p.add_run("Összeállította: Matuz Stefan (Steffy), a Horoscope for Bridge Players szerzője")
    r.font.size = Pt(10); r.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    doc.add_paragraph("Hogyan használd", style="Heading 1")
    for t in [
        "Minden leosztásnál először takard le a többi kezet, és nézd csak Észak és Dél lapjait. Próbáld meg magad kilicitálni, mielőtt elolvasod a magyarázatot.",
        "Az ellenfelek (Kelet–Nyugat) mindig passzolnak, hogy a saját licitünkre koncentrálhass.",
        "Utána olvasd el a licitmagyarázatot, végül a játéktervet. Minden leosztás végén egy rövid tanulság foglalja össze a lényeget.",
    ]:
        doc.add_paragraph(t, style="List Bullet")

    doc.add_paragraph(basics_title, style="Heading 1")
    for pre, txt in basics:
        para(doc, txt, style="List Bullet", bold_prefix=pre)

    doc.add_paragraph("Kis szótár", style="Heading 2")
    gloss = [
        ("figurapont (fp)", "high card points (HCP): A = 4, K = 3, D = 2, B = 1"),
        ("lapok", "A = ász, K = király, D = dáma (Q), B = bubi (J)"),
        ("SZ, szanzadu", "notrump (NT)"),
        ("kényszerítő", "forcing"),
        ("gémig kényszerítő", "game forcing (GF)"),
        ("felvétel / felvevő", "contract / declarer"),
        ("asztal", "dummy"),
        ("impassz", "finesse"),
        ("lopás", "ruff"),
        ("vesztő", "loser"),
        ("fogás", "stopper"),
        ("gém / gém forsz", "game / game force"),
        ("egyenletes elosztás", "balanced hand"),
    ] + list(extra_gloss)
    t = doc.add_table(rows=len(gloss), cols=2)
    t.style = "Table Grid"
    for i, (a, b) in enumerate(gloss):
        t.cell(i, 0).width = Cm(5); t.cell(i, 1).width = Cm(11)
        t.cell(i, 0).paragraphs[0].add_run(a).bold = True
        t.cell(i, 1).paragraphs[0].add_run(b)

    # --- Deals ---
    for d in deals:
        h = doc.add_paragraph(style="Heading 1")
        h.paragraph_format.page_break_before = True
        add_suit_text(h, d["title"])
        diagram(doc, d)
        doc.add_paragraph("Licit", style="Heading 2")
        auction_table(doc, d["auction"])
        doc.add_paragraph("Licitmagyarázat", style="Heading 2")
        for bid, txt in d["explain"]:
            para(doc, txt, style="List Bullet", bold_prefix=bid + " – ")
        doc.add_paragraph("Játékterv", style="Heading 2")
        para(doc, d["lead"], bold_prefix="Kezdés: ")
        for txt in d["play"]:
            para(doc, txt, style="List Bullet")
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        add_suit_text(p, "Tanulság: ", bold=True)
        add_suit_text(p, d["lesson"])
        for r in p.runs:
            r.font.color.rgb = r.font.color.rgb or RGBColor(0x1F, 0x38, 0x64)

    doc.save(out)
    print("saved", out)


BASICS_1 = [
    ("Nyitás: ", "12+ figurapont (fp). Főszínt (♠, ♥) csak legalább 5 lappal nyitunk. Különben 1♣ vagy 1♦ (a hosszabb mellékszín, legalább 3 lap)."),
    ("1SZ nyitás: ", "15–17 fp, egyenletes elosztás."),
    ("2♣ nyitás: ", "erős, mesterséges (kb. 22+ fp). A 2♦, 2♥, 2♠ nyitás gyenge kettes (6 lap, 5–10 fp)."),
    ("Válasz 1-es szinten (pl. 1♥–1♠): ", "6+ fp, 4+ lap, egy körig kényszerítő."),
    ("1SZ válasz főszín nyitásra: ", "kényszerítő, 6–12 fp. A nyitó nem passzolhat."),
    ("Emelés: ", "1♠–2♠ = 6–9 fp, 3+ lap. 1♠–3♠ = limitemelés, 10–11 fp, 4+ lap."),
    ("A 2/1 lényege: ", "ha a válaszadó új színt mond 2-es szinten, ugrás nélkül (pl. 1♠–2♣, 1♥–2♦, 1♦–2♣), az 12–13+ fp-t mutat és gémig kényszerítő. Utána egyik játékos sem passzolhat gém előtt."),
    ("Gyors érkezés elve: ", "gém forsz után a lassú licit erősebb, az ugrás egyenesen a gémbe minimális kezet jelez."),
    ("1SZ nyitás után: ", "2♣ = Stayman (4 lapos főszínt keres), 2♦ = transzfer körre, 2♥ = transzfer pikkre."),
]


if __name__ == "__main__":
    validate(DEALS)
    build(DEALS, sys.argv[1], "A 2/1 licitrendszer (Two over One Game Force) – 1. lecke: 8 gyakorló leosztás",
          "A 2/1 rendszer alapjai", BASICS_1)
