"""
Bold & Balanced Wedding Bible — Mini Freebie Wedding Planner
A condensed 12-page starter planner — lead magnet, bundle freebie, or standalone starter

Usage:
    pip install reportlab
    python wedding_mini_freebie.py

Output (in ./output/):
    Bold_Balanced_Wedding_Bible_Mini_Freebie.pdf
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

W, H = letter
M  = 0.65 * inch
TW = W - 2 * M
X0 = M
X1 = W - M
Y0 = 0.5 * inch
Y1 = H - 0.55 * inch

C = {
    "hot_pink":  HexColor("#E91E8C"),
    "pink":      HexColor("#F48FB1"),
    "blush":     HexColor("#FDE8EE"),
    "gold":      HexColor("#C9A84C"),
    "light_gold":HexColor("#FFF9C4"),
    "rose_gold": HexColor("#B76E79"),
    "dark":      HexColor("#212121"),
    "mid":       HexColor("#5D4037"),
    "line":      HexColor("#E0C0CC"),
    "white":     HexColor("#FFFFFF"),
    "cream":     HexColor("#FFF8E7"),
    "teal":      HexColor("#4DB6AC"),
    "green":     HexColor("#66BB6A"),
}

_pg = 0


def new_page(c: Canvas) -> None:
    global _pg
    if _pg > 0:
        c.showPage()
    _pg += 1


def page_header(c: Canvas, section: str) -> float:
    global _pg
    c.setFillColor(C["hot_pink"])
    c.rect(X0, Y1 - 0.38 * inch, TW, 0.38 * inch, stroke=0, fill=1)
    c.setFillColor(C["gold"])
    c.rect(X0, Y1 - 0.38 * inch - 3, TW, 3, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(white)
    c.drawString(X0 + 6, Y1 - 0.24 * inch, section.upper())
    c.drawRightString(X1 - 4, Y1 - 0.24 * inch, f"Page {_pg}")
    return Y1 - 0.38 * inch - 14


def page_footer(c: Canvas) -> None:
    c.setFont("Helvetica", 7)
    c.setFillColor(C["line"])
    c.drawString(X0, Y0 - 14,
        "Bold & Balanced Wedding Bible  ·  Mini Starter Planner  ·  The Planners Collective")
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(C["hot_pink"])
    upsell = "Get the FULL 9-version bundle at Etsy.com  ·  Search: Bold Balanced Wedding Bible"
    uw = c.stringWidth(upsell, "Helvetica-Bold", 7)
    c.drawString((W - uw) / 2, Y0 - 24, upsell)
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.3)
    c.line(X0, Y0 - 2, X1, Y0 - 2)


def heading(c: Canvas, text: str, y: float, size: int = 10) -> float:
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(C["rose_gold"])
    c.drawString(X0, y, text)
    c.setStrokeColor(C["gold"])
    c.setLineWidth(0.5)
    c.line(X0, y - 3, X1, y - 3)
    return y - 15


def field_row(c: Canvas, label: str, y: float,
              w: float | None = None, indent: float = 0) -> float:
    fw = w if w is not None else TW - indent
    c.setFont("Helvetica", 7)
    c.setFillColor(C["mid"])
    c.drawString(X0 + indent, y, label)
    y -= 18
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.5)
    c.line(X0 + indent, y, X0 + indent + fw, y)
    return y - 8


def ruled_lines(c: Canvas, y: float, n: int = 6, lh: float = 24) -> float:
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.4)
    for _ in range(n):
        y -= lh
        c.line(X0, y, X1, y)
    return y - 6


def checkbox(c: Canvas, text: str, y: float, indent: float = 0) -> float:
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.6)
    c.rect(X0 + indent, y - 9, 9, 9, fill=0)
    c.setFont("Helvetica", 8)
    c.setFillColor(C["dark"])
    # simple wrap
    words = text.split()
    line = ""
    max_chars = int((TW - indent - 16) / (8 * 0.52))
    lines = []
    for word in words:
        if len(line + " " + word) <= max_chars:
            line = (line + " " + word).strip()
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    for i, ln in enumerate(lines):
        c.drawString(X0 + indent + 14, y - (i * 12), ln)
    return y - max(12 * len(lines), 14) - 2


def two_col_fields(c: Canvas, pairs: list[tuple[str, str]], y: float) -> float:
    hw = TW / 2 - 8
    for left_lbl, right_lbl in pairs:
        c.setFont("Helvetica", 7)
        c.setFillColor(C["mid"])
        c.drawString(X0, y, left_lbl)
        c.drawString(X0 + hw + 16, y, right_lbl)
        y -= 18
        c.setStrokeColor(C["line"])
        c.setLineWidth(0.5)
        c.line(X0, y, X0 + hw, y)
        c.line(X0 + hw + 16, y, X1, y)
        y -= 8
    return y


def table_header(c: Canvas, y: float, cols: list[tuple[str, float]]) -> float:
    c.setFillColor(C["gold"])
    c.rect(X0, y - 16, TW, 16, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(white)
    cx = X0 + 4
    for lbl, frac in cols:
        c.drawString(cx, y - 11, lbl)
        cx += TW * frac
    return y - 17


def table_rows(c: Canvas, y: float, cols: list[tuple[str, float]],
               n_rows: int, row_h: float = 17) -> float:
    for i in range(n_rows):
        fill = C["blush"] if i % 2 == 0 else C["white"]
        c.setFillColor(fill)
        c.rect(X0, y - row_h, TW, row_h, stroke=0, fill=1)
        cx = X0
        for _, frac in cols[:-1]:
            cx += TW * frac
            c.setStrokeColor(C["line"])
            c.setLineWidth(0.3)
            c.line(cx, y, cx, y - row_h)
        c.line(X0, y - row_h, X0 + TW, y - row_h)
        y -= row_h
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.5)
    c.rect(X0, y, TW, row_h * n_rows, fill=0)
    return y - 6


def diamond(c: Canvas, cx: float, cy: float, r: float) -> None:
    p = c.beginPath()
    p.moveTo(cx, cy + r)
    p.lineTo(cx + r, cy)
    p.lineTo(cx, cy - r)
    p.lineTo(cx - r, cy)
    p.close()
    c.setFillColor(C["gold"])
    c.drawPath(p, stroke=0, fill=1)


# ─────────────────────────────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────────────────────────────

def build_cover(c: Canvas) -> None:
    new_page(c)
    c.setFillColor(C["blush"])
    c.rect(0, 0, W, H, stroke=0, fill=1)

    c.setFillColor(C["gold"])
    c.rect(0, H - 0.9 * inch, W, 0.9 * inch, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(white)
    c.drawCentredString(W / 2, H - 0.38 * inch, "THE PLANNERS COLLECTIVE")

    # Title
    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(C["dark"])
    t1 = "Wedding Bible"
    t1w = c.stringWidth(t1, "Helvetica-Bold", 26)
    c.drawString((W - t1w) / 2, H * 0.73, t1)

    c.setFont("Helvetica-Bold", 14)
    t2 = "Mini Starter Planner"
    t2w = c.stringWidth(t2, "Helvetica-Bold", 14)
    c.drawString((W - t2w) / 2, H * 0.68, t2)

    c.setStrokeColor(C["gold"])
    c.setLineWidth(1.2)
    c.line(W * 0.2, H * 0.66, W * 0.8, H * 0.66)
    c.line(W * 0.2, H * 0.75, W * 0.8, H * 0.75)

    c.setFont("Helvetica", 10)
    c.setFillColor(C["rose_gold"])
    sub = "Your free 12-page wedding planning starter kit"
    sw = c.stringWidth(sub, "Helvetica", 10)
    c.drawString((W - sw) / 2, H * 0.62, sub)

    # diamonds row
    for i in range(5):
        diamond(c, W * 0.30 + i * W * 0.10, H * 0.595, 4)

    # personalisation box
    c.setFillColor(white)
    c.roundRect(M, H * 0.42, TW, H * 0.155, 6, stroke=0, fill=1)
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.8)
    c.roundRect(M, H * 0.42, TW, H * 0.155, 6, fill=0)

    by = H * 0.57
    hw = TW / 2 - 8
    for lbl, cx in [("Bride / Partner 1", M + 12), ("Groom / Partner 2", M + hw + 28),
                    ("Wedding Date", M + 12), ("Venue", M + hw + 28)]:
        c.setFont("Helvetica", 7.5)
        c.setFillColor(C["mid"])
        c.drawString(cx, by, lbl)
        by2 = by - 16
        c.setStrokeColor(C["gold"])
        c.setLineWidth(0.5)
        c.line(cx, by2, cx + hw - 12, by2)
        if cx == M + hw + 28:
            by -= 26

    # Free badge
    c.setFillColor(C["hot_pink"])
    c.circle(X1 - 22, H * 0.36, 22, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(white)
    c.drawCentredString(X1 - 22, H * 0.365, "FREE")

    # Upsell teaser
    c.setFillColor(C["light_gold"])
    c.rect(M, H * 0.26, TW, H * 0.08, stroke=0, fill=1)
    c.setStrokeColor(C["gold"])
    c.setLineWidth(0.5)
    c.rect(M, H * 0.26, TW, H * 0.08, fill=0)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(C["dark"])
    c.drawCentredString(W / 2, H * 0.325,
        "Want the full 9-version bundle? Search 'Bold Balanced Wedding Bible' on Etsy!")
    c.setFont("Helvetica", 7.5)
    c.setFillColor(C["rose_gold"])
    c.drawCentredString(W / 2, H * 0.30,
        "Includes Excel + Google Sheets + GoodNotes + Printable PDF + Bonus Toolkit and more ✦")

    c.setFillColor(C["hot_pink"])
    c.rect(0, 0, W, 0.48 * inch, stroke=0, fill=1)
    c.setFont("Helvetica", 7.5)
    c.setFillColor(white)
    b = "Compliments of The Planners Collective  ·  etsy.com/shop/ThePlannersCollective"
    bw = c.stringWidth(b, "Helvetica", 7.5)
    c.drawString((W - bw) / 2, 0.16 * inch, b)


def build_quick_details(c: Canvas) -> None:
    new_page(c)
    y = page_header(c, "Wedding Details")

    y = heading(c, "THE BASICS", y)
    y = two_col_fields(c, [
        ("Bride / Partner 1 Full Name", "Groom / Partner 2 Full Name"),
        ("Ceremony Date", "Ceremony Time"),
        ("Ceremony Venue", "Reception Venue"),
        ("Ceremony Address", "Reception Address"),
        ("Officiant", "Wedding Hashtag"),
    ], y)

    y -= 4
    y = heading(c, "WEDDING VISION", y)
    c.setFont("Helvetica", 7.5)
    c.setFillColor(C["mid"])
    c.drawString(X0, y, "Describe the overall feel and style of your wedding day:")
    y -= 4
    y = ruled_lines(c, y, n=5, lh=24)

    y -= 4
    y = heading(c, "IMPORTANT CONTACTS", y)
    y = two_col_fields(c, [
        ("Maid of Honour", "Best Man"),
        ("Wedding Coordinator", "Florist"),
        ("Photographer", "Caterer"),
    ], y)

    page_footer(c)


def build_budget_summary(c: Canvas) -> None:
    new_page(c)
    y = page_header(c, "Budget Summary")

    y = heading(c, "BUDGET OVERVIEW", y)
    hw = TW / 2 - 8
    for lbl in ["Total Wedding Budget  $", "Total Spent to Date  $",
                 "Remaining Budget  $", "Contingency Reserve  $"]:
        y = field_row(c, lbl, y, w=hw)

    y -= 4
    y = heading(c, "BUDGET BY CATEGORY", y)
    cols = [("CATEGORY", 0.30), ("BUDGETED $", 0.20), ("ACTUAL $", 0.20),
            ("DIFFERENCE", 0.18), ("NOTES", 0.12)]
    cats = ["Venue", "Catering", "Photography", "Flowers", "Music",
            "Cake", "Hair & Make-Up", "Attire", "Transport", "Other"]
    y = table_header(c, y, cols)
    y = table_rows(c, y, cols, len(cats), row_h=16)

    page_footer(c)


def build_guest_mini(c: Canvas) -> None:
    new_page(c)
    y = page_header(c, "Guest List")

    y = heading(c, "GUEST TOTALS", y)
    y = two_col_fields(c, [
        ("Total Invited", "Adults"),
        ("Total Attending", "Children"),
        ("Awaiting RSVP", "Declined"),
    ], y)

    y -= 4
    y = heading(c, "GUEST LIST", y)
    cols = [("GUEST NAME", 0.30), ("PHONE / EMAIL", 0.28),
            ("TABLE #", 0.10), ("RSVP", 0.10), ("MEAL", 0.12), ("THANK YOU", 0.10)]
    y = table_header(c, y, cols)
    y = table_rows(c, y, cols, 18, row_h=16)

    page_footer(c)


def build_vendor_mini(c: Canvas) -> None:
    new_page(c)
    y = page_header(c, "Vendor Contacts")

    y = heading(c, "KEY VENDORS", y)
    vendors = [
        "Venue — Ceremony", "Venue — Reception", "Photographer",
        "Caterer", "Florist", "DJ / Band", "Hair & Make-Up",
        "Transport", "Wedding Cake",
    ]
    cols = [("VENDOR", 0.22), ("COMPANY / NAME", 0.26), ("PHONE", 0.18),
            ("BOOKED?", 0.12), ("QUOTED $", 0.12), ("NOTES", 0.10)]
    y = table_header(c, y, cols)

    for i, vtype in enumerate(vendors):
        fill = C["blush"] if i % 2 == 0 else C["white"]
        c.setFillColor(fill)
        c.rect(X0, y - 16, TW, 16, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(C["dark"])
        c.drawString(X0 + 4, y - 11, vtype)
        y -= 16

    c.setStrokeColor(C["line"])
    c.setLineWidth(0.5)
    c.rect(X0, y, TW, 16 * len(vendors), fill=0)

    page_footer(c)


def build_timeline_mini(c: Canvas) -> None:
    new_page(c)
    y = page_header(c, "Day-of Timeline")

    y = heading(c, "WEDDING DAY TIMELINE", y)
    default_times = [
        ("6:00 AM",  "Morning routine / wake up"),
        ("7:00 AM",  "Hair & make-up begins"),
        ("10:00 AM", "Photographer arrives"),
        ("11:00 AM", "Bridal party dressed and ready"),
        ("12:00 PM", "Guests arrive at ceremony venue"),
        ("12:30 PM", "Ceremony begins"),
        ("1:15 PM",  "Couple and family photos"),
        ("2:00 PM",  "Cocktail hour"),
        ("3:30 PM",  "Guests seated for reception"),
        ("3:45 PM",  "Couple introduction & first dance"),
        ("4:00 PM",  "Entrée served"),
        ("4:30 PM",  "Welcome speeches"),
        ("6:00 PM",  "Cake cutting"),
        ("6:30 PM",  "Dancing begins"),
        ("10:30 PM", "Reception concludes"),
    ]

    cols = [("TIME", 0.14), ("EVENT / ACTIVITY", 0.38),
            ("LOCATION", 0.26), ("DONE?", 0.22)]
    y = table_header(c, y, cols)

    for i, (time, event) in enumerate(default_times):
        fill = C["blush"] if i % 2 == 0 else C["white"]
        c.setFillColor(fill)
        c.rect(X0, y - 16, TW, 16, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(C["rose_gold"])
        c.drawString(X0 + 4, y - 11, time)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(C["dark"])
        c.drawString(X0 + TW * 0.14 + 4, y - 11, event)
        y -= 16

    # Extra blank rows
    for i in range(5):
        fill = C["blush"] if (len(default_times) + i) % 2 == 0 else C["white"]
        c.setFillColor(fill)
        c.rect(X0, y - 16, TW, 16, stroke=0, fill=1)
        y -= 16

    c.setStrokeColor(C["line"])
    c.setLineWidth(0.5)
    c.rect(X0, y, TW, 16 * (len(default_times) + 5), fill=0)

    page_footer(c)


def build_checklist_mini(c: Canvas) -> None:
    new_page(c)
    y = page_header(c, "Wedding Checklist")

    y = heading(c, "ESSENTIAL WEDDING CHECKLIST", y)

    timeline = {
        "12+ MONTHS": [
            "Set total wedding budget",
            "Choose and book venue",
            "Set wedding date",
            "Book photographer and videographer",
            "Start dress shopping",
        ],
        "6–12 MONTHS": [
            "Send save-the-dates",
            "Book caterer, florist, DJ/band",
            "Order wedding dress",
            "Plan and book honeymoon",
            "Book hair and make-up",
        ],
        "3–6 MONTHS": [
            "Send invitations",
            "Order wedding rings",
            "Book transportation",
            "Register for gifts",
            "Plan rehearsal dinner",
        ],
        "1–3 MONTHS": [
            "Chase RSVPs",
            "Finalise seating chart",
            "Confirm all vendors",
            "Write personal vows",
            "Apply for marriage licence",
        ],
        "FINAL WEEKS": [
            "Final dress fitting",
            "Confirm vendors — final details",
            "Prepare tip envelopes",
            "Pack wedding night bag",
            "Get a good night's sleep!",
        ],
    }

    n_cols = 2
    col_w = TW / n_cols - 6
    col_items = list(timeline.items())
    left_sections = col_items[:3]
    right_sections = col_items[3:]

    left_y = y
    right_y = y

    for period, tasks in left_sections:
        c.setFillColor(C["hot_pink"])
        c.rect(X0, left_y - 13, col_w, 13, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(white)
        c.drawString(X0 + 4, left_y - 9, period)
        left_y -= 17
        for task in tasks:
            left_y = checkbox(c, task, left_y, indent=4)
        left_y -= 4

    for period, tasks in right_sections:
        rx = X0 + col_w + 12
        c.setFillColor(C["hot_pink"])
        c.rect(rx, right_y - 13, col_w, 13, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(white)
        c.drawString(rx + 4, right_y - 9, period)
        right_y -= 17
        for task in tasks:
            c.setStrokeColor(C["line"])
            c.setLineWidth(0.6)
            c.rect(rx + 4, right_y - 9, 9, 9, fill=0)
            c.setFont("Helvetica", 8)
            c.setFillColor(C["dark"])
            c.drawString(rx + 16, right_y, task)
            right_y -= 14

    page_footer(c)


def build_notes_page(c: Canvas, title: str, section_label: str) -> None:
    new_page(c)
    y = page_header(c, section_label)
    y = heading(c, title, y)
    y = ruled_lines(c, y, n=22, lh=23)
    page_footer(c)


def build_upsell_page(c: Canvas) -> None:
    new_page(c)
    c.setFillColor(C["blush"])
    c.rect(0, 0, W, H, stroke=0, fill=1)

    pad = 0.35 * inch
    c.setStrokeColor(C["line"])
    c.setLineWidth(1.2)
    c.rect(pad, pad, W - 2 * pad, H - 2 * pad, fill=0)

    for cx, cy in [(pad, pad), (W - pad, pad), (pad, H - pad), (W - pad, H - pad)]:
        diamond(c, cx, cy, 7)

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(C["dark"])
    t = "Ready for the full experience?"
    tw = c.stringWidth(t, "Helvetica-Bold", 18)
    c.drawString((W - tw) / 2, H * 0.78, t)

    c.setStrokeColor(C["gold"])
    c.setLineWidth(0.8)
    c.line(W * 0.2, H * 0.76, W * 0.8, H * 0.76)

    c.setFont("Helvetica", 10)
    c.setFillColor(C["rose_gold"])
    sub = "Upgrade to the Bold & Balanced Wedding Bible — Full Bundle"
    sw = c.stringWidth(sub, "Helvetica", 10)
    c.drawString((W - sw) / 2, H * 0.72, sub)

    bundle_items = [
        ("Version 1", "Excel Automated Planner — live formulas, charts, dashboards"),
        ("Version 2", "Google Sheets Planner — edit from any device, share with partner"),
        ("Version 3", "GoodNotes iPad PDF — 46 pages, hyperlinked tabs, Apple Pencil ready"),
        ("Version 4", "Printable PDF — 53 pages, bind at home or print shop"),
        ("Version 5", "Canva Template Blueprint — build your own editable Canva version"),
        ("Version 6", "Bonus Toolkit — emergency kit, tip guide, vow prompts, speeches"),
        ("Version 7", "Etsy Listing Copy — ready-to-use titles, descriptions, tags"),
        ("Version 8", "Customer Instructions Guide — professional welcome PDF"),
        ("Version 9", "This Mini Freebie — for friends, family, or as a lead magnet!"),
    ]

    c.setFillColor(white)
    c.roundRect(M, H * 0.32, TW, H * 0.37, 8, stroke=0, fill=1)
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.6)
    c.roundRect(M, H * 0.32, TW, H * 0.37, 8, fill=0)

    iy = H * 0.685
    for ver, desc in bundle_items:
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(C["hot_pink"])
        c.drawString(M + 12, iy, ver)
        c.setFont("Helvetica", 8)
        c.setFillColor(C["dark"])
        c.drawString(M + 72, iy, desc)
        iy -= 13

    c.setFillColor(C["hot_pink"])
    c.roundRect(W * 0.25, H * 0.24, W * 0.5, H * 0.065, 8, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(white)
    btn = "Search 'Bold Balanced Wedding Bible' on Etsy"
    bw = c.stringWidth(btn, "Helvetica-Bold", 11)
    c.drawString((W - bw) / 2, H * 0.265, btn)

    c.setFont("Helvetica", 9)
    c.setFillColor(C["mid"])
    note = "Or visit: etsy.com/shop/ThePlannersCollective"
    nw = c.stringWidth(note, "Helvetica", 9)
    c.drawString((W - nw) / 2, H * 0.215, note)

    c.setFont("Helvetica", 8)
    c.setFillColor(C["rose_gold"])
    thanks = "Thank you for downloading! We'd love a ⭐⭐⭐⭐⭐ review if you enjoyed this planner."
    tw2 = c.stringWidth(thanks, "Helvetica", 8)
    c.drawString((W - tw2) / 2, H * 0.165, thanks)


# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    out = Path("output")
    out.mkdir(exist_ok=True)
    path = out / "Bold_Balanced_Wedding_Bible_Mini_Freebie.pdf"

    print("Building Mini Freebie PDF …")
    c = Canvas(str(path), pagesize=letter)
    c.setTitle("Bold & Balanced Wedding Bible — Mini Starter Planner")
    c.setAuthor("The Planners Collective")

    global _pg
    _pg = 0

    build_cover(c)
    build_quick_details(c)
    build_budget_summary(c)
    build_guest_mini(c)
    build_vendor_mini(c)
    build_timeline_mini(c)
    build_checklist_mini(c)
    build_notes_page(c, "CEREMONY NOTES", "Notes — Ceremony")
    build_notes_page(c, "RECEPTION NOTES", "Notes — Reception")
    build_notes_page(c, "IDEAS & INSPIRATION", "Notes — Ideas")
    build_notes_page(c, "GENERAL NOTES", "Notes — General")
    build_upsell_page(c)

    c.save()
    print(f"  ✓ Saved: {path}  ({_pg} pages)")
    print("\nDone!")


if __name__ == "__main__":
    main()
