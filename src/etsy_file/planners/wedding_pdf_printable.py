"""
Bold & Balanced Wedding Bible — Printable PDF Planner
Generated with Python reportlab

Features:
  - Print-optimised layout: minimal ink, wide binding margins
  - Elegant black & blush colour scheme — prints beautifully in B&W too
  - Generous write-in lines for handwriting
  - Section divider pages with decorative borders
  - US Letter AND A4 versions

Usage:
    pip install reportlab
    python wedding_pdf_printable.py

Output (in ./output/):
    Bold_Balanced_Wedding_Bible_Printable_Letter.pdf
    Bold_Balanced_Wedding_Bible_Printable_A4.pdf
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

# ─────────────────────────────────────────────────────────────────────
# PALETTE  (print-friendly — falls back gracefully on B&W printers)
# ─────────────────────────────────────────────────────────────────────
C = {
    "accent":      HexColor("#C9A84C"),   # gold accent
    "accent2":     HexColor("#B76E79"),   # rose gold
    "blush":       HexColor("#FCE4EC"),   # very light pink fill
    "border":      HexColor("#C0A0A8"),   # mid-pink border
    "dark":        HexColor("#212121"),   # near-black text
    "mid":         HexColor("#5D4037"),   # warm brown sub-text
    "line":        HexColor("#D4B8BE"),   # ruled-line colour
    "light_line":  HexColor("#EBEBEB"),   # table row stripe
    "white":       HexColor("#FFFFFF"),
    "divider_bg":  HexColor("#FDE8EE"),   # section divider page bg
}

# ─────────────────────────────────────────────────────────────────────
# SECTIONS
# ─────────────────────────────────────────────────────────────────────
SECTIONS = [
    {"id": "intro",     "num": "01", "name": "Introduction & How To Use"},
    {"id": "details",   "num": "02", "name": "Wedding Details"},
    {"id": "budget",    "num": "03", "name": "Budget Planner"},
    {"id": "guests",    "num": "04", "name": "Guest List & RSVPs"},
    {"id": "vendors",   "num": "05", "name": "Vendor Contacts"},
    {"id": "timeline",  "num": "06", "name": "Day-of Timeline"},
    {"id": "checklist", "num": "07", "name": "Master Checklist"},
    {"id": "bridal",    "num": "08", "name": "Bridal Party"},
    {"id": "seating",   "num": "09", "name": "Seating Chart"},
    {"id": "registry",  "num": "10", "name": "Gift Registry & Tracker"},
    {"id": "notes",     "num": "11", "name": "Notes & Inspiration"},
    {"id": "honeymoon", "num": "12", "name": "Honeymoon Planning"},
]


# ─────────────────────────────────────────────────────────────────────
# BUILDER
# ─────────────────────────────────────────────────────────────────────

class PrintablePDF:
    # Layout constants (set per page size in __init__)
    BIND_MARGIN = 0.75 * inch   # left margin (hole-punch / binding)
    OUTER_MARGIN = 0.5 * inch
    TOP_MARGIN = 0.6 * inch
    BOT_MARGIN = 0.5 * inch
    HDR_H = 0.45 * inch         # header stripe height

    def __init__(self, path: Path, pagesize: tuple[float, float]) -> None:
        self.path = path
        self.W, self.H = pagesize
        self.c = Canvas(str(path), pagesize=pagesize)
        self.c.setTitle("Bold & Balanced Wedding Bible — Printable Planner")
        self.c.setAuthor("The Planners Collective")
        self._pages = 0
        self._page_num = 0   # running page number for footer

        # Derived layout values
        self.TW = self.W - self.BIND_MARGIN - self.OUTER_MARGIN  # text width
        self.X0 = self.BIND_MARGIN                               # left edge of content
        self.X1 = self.X0 + self.TW                             # right edge of content
        self.Y0 = self.BOT_MARGIN                               # bottom of content
        self.Y1 = self.H - self.TOP_MARGIN                     # top of content

    # ── internal helpers ────────────────────────────────────────────

    def _new_page(self) -> None:
        if self._pages > 0:
            self.c.showPage()
        self._pages += 1
        self._page_num += 1

    def _header(self, section_num: str, section_name: str) -> None:
        """Thin gold rule + section label at top of content pages."""
        y = self.Y1 - self.HDR_H
        # gold left accent block
        self.c.setFillColor(C["accent"])
        self.c.rect(self.X0, y, 4, self.HDR_H, stroke=0, fill=1)
        # text
        self.c.setFillColor(C["dark"])
        self.c.setFont("Helvetica-Bold", 9)
        label = f"{section_num}  ·  {section_name.upper()}"
        self.c.drawString(self.X0 + 10, y + 14, label)
        # horizontal rule
        self.c.setStrokeColor(C["accent"])
        self.c.setLineWidth(0.5)
        self.c.line(self.X0, y - 2, self.X1, y - 2)

    def _footer(self, section_name: str) -> None:
        """Page number + section name at bottom."""
        fy = self.Y0 - 16
        self.c.setFont("Helvetica", 7)
        self.c.setFillColor(C["border"])
        self.c.drawString(self.X0, fy, "Bold & Balanced Wedding Bible  ·  The Planners Collective")
        pg_str = str(self._page_num)
        self.c.drawRightString(self.X1, fy, pg_str)
        # thin bottom rule
        self.c.setStrokeColor(C["line"])
        self.c.setLineWidth(0.4)
        self.c.line(self.X0, fy + 9, self.X1, fy + 9)

    def _content_top(self) -> float:
        """Y coord just below header."""
        return self.Y1 - self.HDR_H - 14

    def _ruled_lines(self, y_start: float, y_end: float, line_h: float = 26) -> None:
        """Draw ruled writing lines from y_start downward to y_end."""
        self.c.setStrokeColor(C["line"])
        self.c.setLineWidth(0.4)
        y = y_start
        while y - line_h >= y_end:
            y -= line_h
            self.c.line(self.X0, y, self.X1, y)

    def _label(self, x: float, y: float, text: str, size: int = 8,
               bold: bool = False, color: str = "dark") -> None:
        font = "Helvetica-Bold" if bold else "Helvetica"
        self.c.setFont(font, size)
        self.c.setFillColor(C[color])
        self.c.drawString(x, y, text)

    def _field_row(self, y: float, label: str, x_offset: float = 0,
                   w: float | None = None) -> float:
        """Label above a single write-in line. Returns new y below line."""
        fx = self.X0 + x_offset
        fw = w if w is not None else self.TW - x_offset
        self._label(fx, y, label, size=7, color="mid")
        y -= 20
        self.c.setStrokeColor(C["line"])
        self.c.setLineWidth(0.5)
        self.c.line(fx, y, fx + fw, y)
        return y - 8

    def _section_divider(self, num: str, name: str) -> None:
        """Full-page decorative divider for each section."""
        self._new_page()
        # blush background
        self.c.setFillColor(C["divider_bg"])
        self.c.rect(0, 0, self.W, self.H, stroke=0, fill=1)
        # decorative double-border frame
        pad = 0.35 * inch
        self.c.setStrokeColor(C["border"])
        self.c.setLineWidth(1.2)
        self.c.rect(pad, pad, self.W - 2 * pad, self.H - 2 * pad, fill=0)
        self.c.setLineWidth(0.4)
        pad2 = pad + 7
        self.c.rect(pad2, pad2, self.W - 2 * pad2, self.H - 2 * pad2, fill=0)
        # corner diamonds
        for cx, cy in [(pad, pad), (self.W - pad, pad),
                       (pad, self.H - pad), (self.W - pad, self.H - pad)]:
            self._diamond(cx, cy, 6)
        # section number
        self.c.setFont("Helvetica", 36)
        self.c.setFillColor(C["accent"])
        n_w = self.c.stringWidth(num, "Helvetica", 36)
        self.c.drawString((self.W - n_w) / 2, self.H * 0.58, num)
        # gold rule above/below number
        rule_x0 = self.W * 0.25
        rule_x1 = self.W * 0.75
        self.c.setStrokeColor(C["accent"])
        self.c.setLineWidth(0.8)
        self.c.line(rule_x0, self.H * 0.56, rule_x1, self.H * 0.56)
        self.c.line(rule_x0, self.H * 0.62, rule_x1, self.H * 0.62)
        # section name
        self.c.setFont("Helvetica-Bold", 18)
        self.c.setFillColor(C["dark"])
        tw = self.c.stringWidth(name.upper(), "Helvetica-Bold", 18)
        self.c.drawString((self.W - tw) / 2, self.H * 0.48, name.upper())
        # sub-line
        self.c.setFont("Helvetica", 9)
        self.c.setFillColor(C["accent2"])
        sub = "Bold & Balanced Wedding Bible  ·  The Planners Collective"
        sw = self.c.stringWidth(sub, "Helvetica", 9)
        self.c.drawString((self.W - sw) / 2, self.H * 0.44, sub)

    def _diamond(self, cx: float, cy: float, r: float) -> None:
        p = self.c.beginPath()
        p.moveTo(cx, cy + r)
        p.lineTo(cx + r, cy)
        p.lineTo(cx, cy - r)
        p.lineTo(cx - r, cy)
        p.close()
        self.c.setFillColor(C["accent"])
        self.c.drawPath(p, stroke=0, fill=1)

    def _content_page(self, sec: dict, title: str = "") -> float:
        """Start a new content page, draw header/footer, return content top Y."""
        self._new_page()
        self._header(sec["num"], sec["name"])
        self._footer(sec["name"])
        y = self._content_top()
        if title:
            self._label(self.X0, y, title, size=12, bold=True)
            y -= 22
        return y

    def _table_header(self, y: float, cols: list[tuple[str, float]]) -> float:
        """
        Draw a table header row. cols = [(label, width_fraction), ...]
        Returns y below the header row.
        """
        ROW_H = 18
        x = self.X0
        total_w = self.TW
        self.c.setFillColor(C["accent"])
        self.c.rect(x, y - ROW_H, total_w, ROW_H, stroke=0, fill=1)
        self.c.setFillColor(C["white"])
        self.c.setFont("Helvetica-Bold", 7)
        cur_x = x + 4
        for label, frac in cols:
            self.c.drawString(cur_x, y - 13, label)
            cur_x += total_w * frac
        return y - ROW_H - 1

    def _table_rows(self, y: float, cols: list[tuple[str, float]],
                    n_rows: int, row_h: float = 18) -> float:
        """Draw n_rows of alternating-stripe empty table rows."""
        total_w = self.TW
        self.c.setFont("Helvetica", 7)
        for i in range(n_rows):
            fill = C["light_line"] if i % 2 == 0 else C["white"]
            self.c.setFillColor(fill)
            self.c.rect(self.X0, y - row_h, total_w, row_h, stroke=0, fill=1)
            # column dividers
            self.c.setStrokeColor(C["line"])
            self.c.setLineWidth(0.3)
            cur_x = self.X0
            for _, frac in cols[:-1]:
                cur_x += total_w * frac
                self.c.line(cur_x, y, cur_x, y - row_h)
            # bottom rule
            self.c.line(self.X0, y - row_h, self.X0 + total_w, y - row_h)
            y -= row_h
        # outer border
        self.c.setStrokeColor(C["border"])
        self.c.setLineWidth(0.6)
        total_h = row_h * n_rows
        self.c.rect(self.X0, y, total_w, total_h, fill=0)
        return y - 8

    # ── COVER PAGE ───────────────────────────────────────────────────

    def build_cover(self) -> None:
        self._new_page()
        W, H = self.W, self.H

        # blush background
        self.c.setFillColor(C["blush"])
        self.c.rect(0, 0, W, H, stroke=0, fill=1)

        # top gold bar
        self.c.setFillColor(C["accent"])
        self.c.rect(0, H - 0.12 * H, W, 0.12 * H, stroke=0, fill=1)

        # thin blush strip inside gold bar
        self.c.setFillColor(C["divider_bg"])
        self.c.rect(0, H - 0.12 * H + 4, W, 2, stroke=0, fill=1)

        # title block
        self.c.setFillColor(C["dark"])
        self.c.setFont("Helvetica-Bold", 26)
        title1 = "Bold & Balanced"
        tw = self.c.stringWidth(title1, "Helvetica-Bold", 26)
        self.c.drawString((W - tw) / 2, H * 0.72, title1)

        self.c.setFont("Helvetica-Bold", 22)
        title2 = "Wedding Bible"
        tw = self.c.stringWidth(title2, "Helvetica-Bold", 22)
        self.c.drawString((W - tw) / 2, H * 0.65, title2)

        # gold rules
        self.c.setStrokeColor(C["accent"])
        self.c.setLineWidth(1.2)
        self.c.line(W * 0.2, H * 0.63, W * 0.8, H * 0.63)
        self.c.line(W * 0.2, H * 0.74, W * 0.8, H * 0.74)

        # sub-title
        self.c.setFont("Helvetica", 11)
        self.c.setFillColor(C["accent2"])
        sub = "Modern Luxury Wedding Planning System"
        sw = self.c.stringWidth(sub, "Helvetica", 11)
        self.c.drawString((W - sw) / 2, H * 0.60, sub)

        # decorative diamonds row
        for i in range(5):
            self._diamond(W * 0.3 + i * W * 0.1, H * 0.57, 4)

        # personalisation fields
        field_x = W * 0.2
        field_w = W * 0.6
        for label, fy in [
            ("Bride / Partner 1", H * 0.47),
            ("Groom / Partner 2", H * 0.41),
            ("Wedding Date", H * 0.35),
            ("Venue", H * 0.29),
        ]:
            self.c.setFont("Helvetica", 8)
            self.c.setFillColor(C["mid"])
            self.c.drawString(field_x, fy + 12, label)
            self.c.setStrokeColor(C["accent"])
            self.c.setLineWidth(0.6)
            self.c.line(field_x, fy, field_x + field_w, fy)

        # bottom branding bar
        self.c.setFillColor(C["accent"])
        self.c.rect(0, 0, W, 0.06 * H, stroke=0, fill=1)
        self.c.setFont("Helvetica", 8)
        self.c.setFillColor(C["white"])
        brand = "THE PLANNERS COLLECTIVE  ·  Printable Edition"
        bw = self.c.stringWidth(brand, "Helvetica", 8)
        self.c.drawString((W - bw) / 2, 0.06 * H * 0.4, brand)

    # ── SECTION 01: INTRODUCTION ─────────────────────────────────────

    def build_intro(self) -> None:
        sec = SECTIONS[0]
        self._section_divider(sec["num"], sec["name"])

        y = self._content_page(sec, "Welcome to Your Wedding Planner")

        intro_lines = [
            "Congratulations on your engagement! This planner is your all-in-one guide",
            "to organise every detail of your wedding day — from the first budget meeting",
            "to the final thank-you notes.",
            "",
            "HOW TO USE THIS PLANNER",
            "",
            "Print all pages at home or at your local print shop. We recommend printing",
            "on 80–100gsm paper for the best writing experience. Bind with a ring binder,",
            "disc system, or have it spiral-bound for a truly beautiful keepsake.",
            "",
            "Each section begins with a decorative divider page, followed by planning",
            "worksheets, checklists, and lined notes pages. Work through the sections",
            "in order or jump directly to what you need today.",
            "",
            "PRINTING TIPS",
            "",
            "• Print double-sided (flip on long edge) for a book-style finish",
            "• Leave the left margin clear for hole-punching or binding",
            "• For best colour, use the colour PDF; the B&W version prints cleanly too",
            "• Laminate the cover page for a professional finish",
            "",
            "We wish you a beautiful, stress-free wedding planning journey.",
            "",
            "With love,",
            "The Planners Collective",
        ]
        self.c.setFont("Helvetica", 8.5)
        self.c.setFillColor(C["dark"])
        for line in intro_lines:
            if line.startswith("HOW TO") or line.startswith("PRINTING"):
                self.c.setFont("Helvetica-Bold", 9)
                self.c.setFillColor(C["accent2"])
            elif line.startswith("•"):
                self.c.setFont("Helvetica", 8.5)
                self.c.setFillColor(C["dark"])
                self.c.drawString(self.X0 + 12, y, line)
                y -= 14
                continue
            else:
                self.c.setFont("Helvetica", 8.5)
                self.c.setFillColor(C["dark"])
            self.c.drawString(self.X0, y, line)
            y -= 14

        # Table of contents
        y -= 16
        self._label(self.X0, y, "CONTENTS", size=10, bold=True, color="dark")
        y -= 4
        self.c.setStrokeColor(C["accent"])
        self.c.setLineWidth(0.6)
        self.c.line(self.X0, y, self.X1, y)
        y -= 14
        for s in SECTIONS:
            self.c.setFont("Helvetica", 8)
            self.c.setFillColor(C["dark"])
            self.c.drawString(self.X0 + 4, y, f"Section {s['num']}  —  {s['name']}")
            self.c.setFillColor(C["line"])
            dots_x = self.X0 + 200
            self.c.drawString(dots_x, y, "· · · · · · · · · · · · · · · · · ·")
            y -= 13

    # ── SECTION 02: WEDDING DETAILS ──────────────────────────────────

    def build_details(self) -> None:
        sec = SECTIONS[1]
        self._section_divider(sec["num"], sec["name"])

        y = self._content_page(sec, "The Basics")
        fields_col1 = [
            "Bride / Partner 1 Full Name",
            "Bride / Partner 1 Phone",
            "Bride / Partner 1 Email",
            "Groom / Partner 2 Full Name",
            "Groom / Partner 2 Phone",
            "Groom / Partner 2 Email",
        ]
        half = self.TW / 2 - 12
        for i, lbl in enumerate(fields_col1):
            col_x = 0 if i % 2 == 0 else half + 24
            # alternate: stack them
        # Actually stack vertically for readability
        for lbl in fields_col1:
            y = self._field_row(y, lbl)

        y -= 8
        self._label(self.X0, y, "THE BIG DAY", size=10, bold=True)
        y -= 18
        two_col = [
            ("Wedding Date", "Ceremony Time"),
            ("Ceremony Venue", "Reception Venue"),
            ("Ceremony Address", "Reception Address"),
            ("Officiant Name", "Officiant Phone"),
            ("Wedding Hashtag", "Colour Palette"),
        ]
        hw = self.TW / 2 - 10
        for left_lbl, right_lbl in two_col:
            self.c.setFont("Helvetica", 7)
            self.c.setFillColor(C["mid"])
            self.c.drawString(self.X0, y, left_lbl)
            self.c.drawString(self.X0 + hw + 20, y, right_lbl)
            y -= 20
            self.c.setStrokeColor(C["line"])
            self.c.setLineWidth(0.5)
            self.c.line(self.X0, y, self.X0 + hw, y)
            self.c.line(self.X0 + hw + 20, y, self.X1, y)
            y -= 10

        # Page 2 – notes / vision
        y = self._content_page(sec, "Wedding Vision & Inspiration")
        self.c.setFont("Helvetica", 8)
        self.c.setFillColor(C["mid"])
        self.c.drawString(self.X0, y, "Describe the overall feel / mood you want for your day:")
        y -= 8
        self._ruled_lines(y, self.Y0 + 20, line_h=24)

    # ── SECTION 03: BUDGET ───────────────────────────────────────────

    def build_budget(self) -> None:
        sec = SECTIONS[2]
        self._section_divider(sec["num"], sec["name"])

        y = self._content_page(sec, "Budget Summary")
        for lbl in ["Total Wedding Budget  $", "Amount Paid to Date  $",
                     "Amount Still Owed  $", "Contingency Reserve  $"]:
            y = self._field_row(y, lbl, w=self.TW * 0.5)

        y -= 12
        cols = [
            ("CATEGORY", 0.30),
            ("BUDGETED ($)", 0.18),
            ("ACTUAL ($)", 0.18),
            ("PAID ($)", 0.18),
            ("NOTES", 0.16),
        ]
        categories = [
            "Venue — Ceremony", "Venue — Reception", "Catering / Food",
            "Bar / Beverages", "Photography", "Videography",
            "Florist / Flowers", "Music / DJ / Band", "Cake / Desserts",
            "Hair & Make-Up", "Wedding Dress", "Groom's Attire",
            "Invitations / Stationery", "Transportation", "Honeymoon Deposit",
            "Favours / Gifts", "Decorations", "Officiant",
            "Rings", "Miscellaneous",
        ]
        y = self._table_header(y, cols)
        y = self._table_rows(y, cols, len(categories))

        # Page 2 – category detail notes
        y = self._content_page(sec, "Budget Notes")
        self.c.setFont("Helvetica", 8)
        self.c.setFillColor(C["mid"])
        self.c.drawString(self.X0, y,
            "Use this page to note deposit deadlines, payment terms, and money-saving ideas:")
        y -= 8
        self._ruled_lines(y, self.Y0 + 20, line_h=24)

    # ── SECTION 04: GUEST LIST ───────────────────────────────────────

    def build_guests(self) -> None:
        sec = SECTIONS[3]
        self._section_divider(sec["num"], sec["name"])

        y = self._content_page(sec, "Guest List Totals")
        summary_fields = [
            ("Total Invited", "Adults Invited", "Children Invited"),
            ("Total Attending", "Declined / Unable", "Awaiting RSVP"),
            ("Dietary Requirements", "Vegetarian / Vegan", "Gluten-Free"),
        ]
        hw = self.TW / 3 - 8
        for row in summary_fields:
            for i, lbl in enumerate(row):
                self.c.setFont("Helvetica", 7)
                self.c.setFillColor(C["mid"])
                self.c.drawString(self.X0 + i * (hw + 12), y, lbl)
            y -= 20
            for i in range(3):
                self.c.setStrokeColor(C["line"])
                self.c.setLineWidth(0.5)
                self.c.line(self.X0 + i * (hw + 12), y,
                            self.X0 + i * (hw + 12) + hw, y)
            y -= 12

        y -= 8
        cols = [
            ("GUEST NAME", 0.28),
            ("SIDE B/G", 0.10),
            ("TABLE #", 0.09),
            ("RSVP", 0.09),
            ("MEAL", 0.10),
            ("DIETARY", 0.14),
            ("GIFT RCVD", 0.10),
            ("THANK YOU", 0.10),
        ]
        y = self._table_header(y, cols)
        y = self._table_rows(y, cols, 22, row_h=16)

        # page 2 — more guests
        y = self._content_page(sec, "Guest List — continued")
        y = self._table_header(y, cols)
        y = self._table_rows(y, cols, 30, row_h=16)

        # page 3 — more guests
        y = self._content_page(sec, "Guest List — continued")
        y = self._table_header(y, cols)
        y = self._table_rows(y, cols, 30, row_h=16)

    # ── SECTION 05: VENDORS ──────────────────────────────────────────

    def build_vendors(self) -> None:
        sec = SECTIONS[4]
        self._section_divider(sec["num"], sec["name"])

        vendor_types = [
            "Photographer", "Videographer", "Caterer / Food",
            "Bar / Beverages", "Florist", "Cake / Desserts",
            "Hair Stylist", "Make-Up Artist", "DJ / Band / Music",
            "Venue — Ceremony", "Venue — Reception", "Officiant",
            "Wedding Planner / Coordinator", "Transportation",
            "Stationery / Invitations", "Photo Booth",
        ]

        for i, vtype in enumerate(vendor_types):
            if i % 2 == 0:
                y = self._content_page(sec, "Vendor Contacts")

            # Vendor card
            card_h = (self.Y1 - self.HDR_H - 30 - self.Y0) / 2 - 10
            card_y = y if i % 2 == 0 else y
            # light blush card background
            self.c.setFillColor(C["blush"])
            self.c.rect(self.X0, card_y - card_h, self.TW, card_h, stroke=0, fill=1)
            self.c.setStrokeColor(C["border"])
            self.c.setLineWidth(0.5)
            self.c.rect(self.X0, card_y - card_h, self.TW, card_h, fill=0)
            # vendor type header
            self.c.setFillColor(C["accent"])
            self.c.rect(self.X0, card_y - 16, self.TW, 16, stroke=0, fill=1)
            self.c.setFont("Helvetica-Bold", 8)
            self.c.setFillColor(C["white"])
            self.c.drawString(self.X0 + 6, card_y - 11, vtype.upper())

            # fields inside card
            fy = card_y - 28
            card_fields_l = [
                ("Company / Name", self.TW * 0.55),
                ("Website", self.TW * 0.55),
                ("Contact Person", self.TW * 0.55),
            ]
            card_fields_r = [
                ("Phone", self.TW * 0.38),
                ("Email", self.TW * 0.38),
                ("Booked? Y / N", self.TW * 0.38),
            ]
            fy2 = fy
            for (lbl_l, w_l), (lbl_r, w_r) in zip(card_fields_l, card_fields_r):
                self.c.setFont("Helvetica", 6.5)
                self.c.setFillColor(C["mid"])
                self.c.drawString(self.X0 + 6, fy2, lbl_l)
                self.c.drawString(self.X0 + self.TW * 0.58, fy2, lbl_r)
                fy2 -= 16
                self.c.setStrokeColor(C["line"])
                self.c.setLineWidth(0.4)
                self.c.line(self.X0 + 6, fy2, self.X0 + 6 + w_l, fy2)
                self.c.line(self.X0 + self.TW * 0.58, fy2,
                            self.X0 + self.TW * 0.58 + w_r, fy2)
                fy2 -= 8

            # price / deposit row
            for lbl, x_off, w_f in [
                ("Quoted Price $", 6, 0.25),
                ("Deposit Paid $", self.TW * 0.32, 0.25),
                ("Balance Due $", self.TW * 0.62, 0.32),
            ]:
                self.c.setFont("Helvetica", 6.5)
                self.c.setFillColor(C["mid"])
                self.c.drawString(self.X0 + x_off, fy2, lbl)
                fy2 -= 16
                self.c.setStrokeColor(C["line"])
                self.c.setLineWidth(0.4)
                self.c.line(self.X0 + x_off, fy2,
                            self.X0 + x_off + self.TW * w_f, fy2)
            fy2 -= 8
            # notes line
            self.c.setFont("Helvetica", 6.5)
            self.c.setFillColor(C["mid"])
            self.c.drawString(self.X0 + 6, fy2, "Notes / Contract Details")
            fy2 -= 16
            self.c.setStrokeColor(C["line"])
            self.c.setLineWidth(0.4)
            self.c.line(self.X0 + 6, fy2, self.X1 - 6, fy2)

            y = card_y - card_h - 14

    # ── SECTION 06: DAY-OF TIMELINE ──────────────────────────────────

    def build_timeline(self) -> None:
        sec = SECTIONS[5]
        self._section_divider(sec["num"], sec["name"])

        y = self._content_page(sec, "Day-of Timeline")
        cols = [
            ("TIME", 0.13),
            ("EVENT / ACTIVITY", 0.35),
            ("LOCATION", 0.22),
            ("PERSON RESPONSIBLE", 0.20),
            ("DONE", 0.10),
        ]
        y = self._table_header(y, cols)
        y = self._table_rows(y, cols, 28, row_h=17)

        y = self._content_page(sec, "Day-of Timeline — continued")
        y = self._table_header(y, cols)
        y = self._table_rows(y, cols, 28, row_h=17)

        y = self._content_page(sec, "Wedding Morning Schedule")
        morning_slots = [
            "6:00 AM", "7:00 AM", "7:30 AM", "8:00 AM", "8:30 AM",
            "9:00 AM", "9:30 AM", "10:00 AM", "10:30 AM", "11:00 AM",
            "11:30 AM", "12:00 PM",
        ]
        for slot in morning_slots:
            self._label(self.X0, y, slot, size=7, bold=True, color="accent2")
            self.c.setStrokeColor(C["line"])
            self.c.setLineWidth(0.4)
            self.c.line(self.X0 + 50, y - 2, self.X1, y - 2)
            y -= 22

    # ── SECTION 07: MASTER CHECKLIST ─────────────────────────────────

    def build_checklist(self) -> None:
        sec = SECTIONS[6]
        self._section_divider(sec["num"], sec["name"])

        timeline_tasks = {
            "12+ Months Before": [
                "Set your overall budget",
                "Decide on wedding vision and theme",
                "Create your initial guest list",
                "Research and book your venue",
                "Set your wedding date",
                "Hire a wedding planner (if using one)",
                "Start dress shopping",
                "Book photographer and videographer",
                "Begin honeymoon research",
            ],
            "9–12 Months Before": [
                "Book caterer / choose catering package",
                "Book florist",
                "Book DJ / band / musicians",
                "Book officiant",
                "Send save-the-dates",
                "Order wedding dress",
                "Book hair and make-up artists",
                "Arrange accommodation for out-of-town guests",
                "Begin cake tastings",
            ],
            "6–9 Months Before": [
                "Order wedding cake",
                "Book transportation",
                "Plan honeymoon and book flights/hotel",
                "Create wedding website",
                "Register for gifts",
                "Begin bridal party attire shopping",
                "Plan rehearsal dinner",
                "Order wedding invitations",
                "Schedule engagement photos",
            ],
            "3–6 Months Before": [
                "Mail invitations (8–12 weeks before)",
                "Order wedding rings",
                "Book hair & make-up trials",
                "Finalise rehearsal dinner details",
                "Book photo booth (if desired)",
                "Purchase wedding favours",
                "Plan wedding ceremony details with officiant",
                "Finalise menu with caterer",
                "Begin writing personal vows",
            ],
            "1–3 Months Before": [
                "Chase outstanding RSVPs",
                "Finalise seating chart",
                "Confirm all vendor bookings",
                "Break in wedding shoes",
                "Purchase wedding party gifts",
                "Arrange day-of emergency kit",
                "Create detailed day-of timeline",
                "Finalise processional / recessional music",
                "Apply for marriage licence",
            ],
            "Final Weeks": [
                "Final dress fitting",
                "Deliver final guest numbers to caterer",
                "Confirm final details with all vendors",
                "Prepare vendor tip envelopes",
                "Assign a day-of coordinator / point of contact",
                "Prepare overnight bag for wedding night",
                "Confirm honeymoon travel details",
                "Hand off vendor contact list to coordinator",
            ],
            "Wedding Week": [
                "Pick up wedding dress",
                "Confirm delivery schedule with all vendors",
                "Delegate tasks to wedding party",
                "Get a good night's sleep!",
                "Enjoy your rehearsal and rehearsal dinner",
                "Prepare personal vows and any readings",
                "Relax — you've planned the perfect day!",
            ],
        }

        for period, tasks in timeline_tasks.items():
            n_per_page = 18
            for chunk_start in range(0, len(tasks), n_per_page):
                y = self._content_page(sec, f"Checklist — {period}")
                chunk = tasks[chunk_start:chunk_start + n_per_page]
                for task in chunk:
                    # checkbox
                    self.c.setStrokeColor(C["border"])
                    self.c.setLineWidth(0.6)
                    self.c.rect(self.X0, y - 9, 9, 9, fill=0)
                    self.c.setFont("Helvetica", 8)
                    self.c.setFillColor(C["dark"])
                    self.c.drawString(self.X0 + 14, y - 1, task)
                    y -= 18
                    if y < self.Y0 + 30:
                        break

    # ── SECTION 08: BRIDAL PARTY ──────────────────────────────────────

    def build_bridal(self) -> None:
        sec = SECTIONS[7]
        self._section_divider(sec["num"], sec["name"])

        y = self._content_page(sec, "Bridal Party Details")
        roles = [
            ("Maid of Honour", "Best Man"),
            ("Bridesmaid 1", "Groomsman 1"),
            ("Bridesmaid 2", "Groomsman 2"),
            ("Bridesmaid 3", "Groomsman 3"),
            ("Bridesmaid 4", "Groomsman 4"),
            ("Flower Girl", "Ring Bearer"),
        ]
        hw = self.TW / 2 - 10
        for left_role, right_role in roles:
            for prefix, x_off in [(left_role, 0), (right_role, hw + 20)]:
                # role label
                self.c.setFillColor(C["accent"])
                self.c.rect(self.X0 + x_off, y - 14, hw, 14, stroke=0, fill=1)
                self.c.setFont("Helvetica-Bold", 7)
                self.c.setFillColor(C["white"])
                self.c.drawString(self.X0 + x_off + 4, y - 10, prefix.upper())
            y -= 18

            for sub_label in ["Name", "Phone", "Dress / Suit Size", "Colour / Style"]:
                self.c.setFont("Helvetica", 6.5)
                self.c.setFillColor(C["mid"])
                self.c.drawString(self.X0 + 4, y, sub_label)
                self.c.drawString(self.X0 + hw + 24, y, sub_label)
                y -= 16
                self.c.setStrokeColor(C["line"])
                self.c.setLineWidth(0.4)
                self.c.line(self.X0 + 4, y, self.X0 + hw - 4, y)
                self.c.line(self.X0 + hw + 24, y, self.X1 - 4, y)
                y -= 8
            y -= 6

    # ── SECTION 09: SEATING CHART ─────────────────────────────────────

    def build_seating(self) -> None:
        sec = SECTIONS[8]
        self._section_divider(sec["num"], sec["name"])

        # Table grid — 8 tables per page, 2 columns
        tables_per_page = 8
        total_tables = 20
        table_w = self.TW / 2 - 8
        table_fields = 8  # seats per table card

        page_count = -1
        for t_idx in range(total_tables):
            if t_idx % tables_per_page == 0:
                page_count += 1
                y = self._content_page(sec, "Seating Chart")
                col_heights = [y, y]

            col = t_idx % 2
            tx = self.X0 if col == 0 else self.X0 + table_w + 16
            ty = col_heights[col]
            card_h = 14 + table_fields * 14 + 6

            # card bg + header
            self.c.setFillColor(C["blush"])
            self.c.rect(tx, ty - card_h, table_w, card_h, stroke=0, fill=1)
            self.c.setFillColor(C["accent2"])
            self.c.rect(tx, ty - 14, table_w, 14, stroke=0, fill=1)
            self.c.setFont("Helvetica-Bold", 7)
            self.c.setFillColor(C["white"])
            self.c.drawString(tx + 4, ty - 10, f"TABLE  {t_idx + 1}")
            self.c.drawRightString(tx + table_w - 4, ty - 10, f"Seats: {table_fields}")

            # seat lines
            sy = ty - 22
            for seat in range(1, table_fields + 1):
                self.c.setFont("Helvetica", 6)
                self.c.setFillColor(C["mid"])
                self.c.drawString(tx + 4, sy, f"{seat}.")
                self.c.setStrokeColor(C["line"])
                self.c.setLineWidth(0.35)
                self.c.line(tx + 14, sy - 2, tx + table_w - 4, sy - 2)
                sy -= 14

            col_heights[col] = ty - card_h - 10

    # ── SECTION 10: GIFT REGISTRY & TRACKER ──────────────────────────

    def build_registry(self) -> None:
        sec = SECTIONS[9]
        self._section_divider(sec["num"], sec["name"])

        y = self._content_page(sec, "Registry Details")
        for store_num in range(1, 4):
            self._label(self.X0, y, f"Registry Store {store_num}", size=9,
                        bold=True, color="accent2")
            y -= 18
            for lbl in ["Store / Website Name", "Registry URL / Code",
                        "Login Username", "Login Password (hint)"]:
                y = self._field_row(y, lbl, w=self.TW * 0.7)
            y -= 10

        y = self._content_page(sec, "Gift Tracker")
        cols = [
            ("GIFT DESCRIPTION", 0.30),
            ("FROM", 0.20),
            ("DATE RCVD", 0.14),
            ("VALUE $", 0.12),
            ("THANK YOU SENT", 0.14),
            ("NOTES", 0.10),
        ]
        y = self._table_header(y, cols)
        y = self._table_rows(y, cols, 25, row_h=17)

        y = self._content_page(sec, "Gift Tracker — continued")
        y = self._table_header(y, cols)
        y = self._table_rows(y, cols, 30, row_h=17)

    # ── SECTION 11: NOTES & INSPIRATION ──────────────────────────────

    def build_notes(self) -> None:
        sec = SECTIONS[10]
        self._section_divider(sec["num"], sec["name"])

        page_titles = [
            "Ideas & Inspiration",
            "Ceremony Notes",
            "Reception Notes",
            "Vendor Meeting Notes",
            "General Notes",
        ]
        for title in page_titles:
            y = self._content_page(sec, title)
            self._ruled_lines(y, self.Y0 + 20, line_h=24)

    # ── SECTION 12: HONEYMOON ─────────────────────────────────────────

    def build_honeymoon(self) -> None:
        sec = SECTIONS[11]
        self._section_divider(sec["num"], sec["name"])

        y = self._content_page(sec, "Honeymoon Overview")
        for lbl in ["Destination", "Departure Date", "Return Date",
                     "Total Budget  $", "Amount Paid  $", "Balance Due  $"]:
            y = self._field_row(y, lbl, w=self.TW * 0.6)

        y -= 10
        self._label(self.X0, y, "TRAVEL DETAILS", size=9, bold=True)
        y -= 18
        travel_pairs = [
            ("Outbound Flight / Train Ref", "Outbound Departure Time"),
            ("Return Flight / Train Ref", "Return Departure Time"),
            ("Airport / Station", "Transfer Details"),
        ]
        hw = self.TW / 2 - 10
        for l_lbl, r_lbl in travel_pairs:
            self.c.setFont("Helvetica", 7)
            self.c.setFillColor(C["mid"])
            self.c.drawString(self.X0, y, l_lbl)
            self.c.drawString(self.X0 + hw + 20, y, r_lbl)
            y -= 20
            self.c.setStrokeColor(C["line"])
            self.c.setLineWidth(0.5)
            self.c.line(self.X0, y, self.X0 + hw, y)
            self.c.line(self.X0 + hw + 20, y, self.X1, y)
            y -= 10

        y -= 6
        self._label(self.X0, y, "ACCOMMODATION", size=9, bold=True)
        y -= 18
        for lbl in ["Hotel / Resort Name", "Confirmation Number",
                     "Check-in Date & Time", "Check-out Date & Time",
                     "Hotel Address", "Hotel Phone"]:
            y = self._field_row(y, lbl)

        # Honeymoon packing / itinerary page
        y = self._content_page(sec, "Honeymoon Packing & Itinerary")
        self._label(self.X0, y, "PACKING LIST", size=9, bold=True)
        y -= 18
        packing = [
            "Passports / Travel Documents", "Travel Insurance Documents",
            "Flight / Hotel Confirmations", "Currency / Travel Cards",
            "Formal Outfit for Dinners", "Swimwear", "Sunscreen",
            "Camera / Chargers", "Medications", "Emergency Contacts List",
        ]
        for item in packing:
            self.c.setStrokeColor(C["border"])
            self.c.setLineWidth(0.6)
            self.c.rect(self.X0, y - 9, 9, 9, fill=0)
            self.c.setFont("Helvetica", 8)
            self.c.setFillColor(C["dark"])
            self.c.drawString(self.X0 + 14, y - 1, item)
            y -= 18

        y -= 10
        self._label(self.X0, y, "DAILY ITINERARY NOTES", size=9, bold=True)
        y -= 8
        self._ruled_lines(y, self.Y0 + 20, line_h=24)

    # ── MAIN BUILDER ──────────────────────────────────────────────────

    def build(self) -> None:
        self.build_cover()
        self.build_intro()
        self.build_details()
        self.build_budget()
        self.build_guests()
        self.build_vendors()
        self.build_timeline()
        self.build_checklist()
        self.build_bridal()
        self.build_seating()
        self.build_registry()
        self.build_notes()
        self.build_honeymoon()
        self.c.save()
        print(f"  ✓ Saved: {self.path}  ({self._pages} pages)")


# ─────────────────────────────────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    out = Path("output")
    out.mkdir(exist_ok=True)

    for label, pagesize in [("Letter", letter), ("A4", A4)]:
        print(f"Building Printable PDF ({label}) …")
        path = out / f"Bold_Balanced_Wedding_Bible_Printable_{label}.pdf"
        pdf = PrintablePDF(path=path, pagesize=pagesize)
        pdf.build()

    print("\nDone! Both printable PDFs are ready.")


if __name__ == "__main__":
    main()
