"""Shared Word helpers for the Easy Bidding documents (large print, red hearts/diamonds)."""
import re
from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

RED = RGBColor(0xC0, 0x00, 0x00)
NAVY = RGBColor(0x1F, 0x3A, 0x5F)
FONT = "Arial"
HCP = {"A": 4, "K": 3, "Q": 2, "J": 1}


def new_doc(body_size, margin_cm):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, side, Cm(margin_cm))
    st = doc.styles["Normal"]
    st.font.name = FONT
    st.font.size = Pt(body_size)
    st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    st.paragraph_format.space_after = Pt(3)
    st.paragraph_format.space_before = Pt(0)
    return doc


def rich(par, text, size=None, bold=False, color=None):
    """Add text to a paragraph. **x** = bold. ♥ and ♦ are always red."""
    for i, chunk in enumerate(re.split(r"\*\*", text)):
        is_bold = bold or (i % 2 == 1)
        for piece in re.split(r"([♥♦♠♣])", chunk):
            if not piece:
                continue
            run = par.add_run(piece)
            run.bold = is_bold
            run.font.name = FONT
            if size:
                run.font.size = Pt(size)
            if piece in "♥♦":
                run.font.color.rgb = RED
            elif color is not None:
                run.font.color.rgb = color
    return par


def para(doc_or_cell, text, size=None, bold=False, align=None, after=3, color=None):
    p = doc_or_cell.add_paragraph()
    rich(p, text, size, bold, color)
    p.paragraph_format.space_after = Pt(after)
    if align == "center":
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return p


def heading(doc, text, size, before=8, after=3):
    p = doc.add_paragraph()
    rich(p, text, size, True, NAVY)
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    p.paragraph_format.keep_with_next = True
    return p


def shade(cell, hex_fill):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tcPr.append(shd)


def cell_text(cell, text, size, bold=False):
    cell.paragraphs[0].text = ""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        p.paragraph_format.space_after = Pt(1)
        rich(p, line, size, bold)


def table(doc, rows, widths_cm, size, header=True, head_fill="1F3A5F", stripe="EEF3F8"):
    t = doc.add_table(rows=len(rows), cols=len(rows[0]))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = t.cell(r, c)
            cell.width = Cm(widths_cm[c])
            if header and r == 0:
                cell_text(cell, val, size, True)
                shade(cell, head_fill)
                for run in cell.paragraphs[0].runs:
                    run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            else:
                cell_text(cell, val, size)
                if r % 2 == 0:
                    shade(cell, stripe)
    # keep rows from splitting across pages
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr()
        cant = OxmlElement("w:cantSplit")
        trPr.append(cant)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


def box(doc, title, lines, size, fill="FFF4D6", width_cm=18.4):
    """A shaded one-cell 'remember' box."""
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.cell(0, 0)
    cell.width = Cm(width_cm)
    shade(cell, fill)
    cell.paragraphs[0].text = ""
    p = cell.paragraphs[0]
    rich(p, title, size + 1, True, NAVY)
    p.paragraph_format.space_after = Pt(2)
    for line in lines:
        q = cell.add_paragraph()
        q.paragraph_format.space_after = Pt(1)
        rich(q, line, size)
    doc.add_paragraph().paragraph_format.space_after = Pt(0)
    return t


# ---------- hands ----------

def check_hand(hand, stated_hcp):
    """hand = 'spades hearts diamonds clubs' (T = 10, '-' = void). Returns HCP after checks."""
    suits = hand.split()
    assert len(suits) == 4, hand
    cards = sum(0 if s == "-" else len(s) for s in suits)
    assert cards == 13, f"{hand}: {cards} cards"
    for s in suits:
        assert len(set(s)) == len(s), f"duplicate card in {hand}"
    pts = sum(HCP.get(ch, 0) for ch in hand)
    assert pts == stated_hcp, f"{hand}: {pts} HCP, text says {stated_hcp}"
    return pts


def hand_line(hand):
    suits = hand.split()
    out = []
    for sym, s in zip("♠♥♦♣", suits):
        out.append(sym + " " + ("—" if s == "-" else " ".join("10" if c == "T" else c for c in s)))
    return "     ".join(out)
