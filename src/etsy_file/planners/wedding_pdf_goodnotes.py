"""
Bold & Balanced Wedding Bible — GoodNotes & iPad PDF Planner
Generated with Python reportlab

Features:
  - 12 colour-coded sections with clickable side navigation tabs
  - Every tab is a live hyperlink — tap to jump instantly in GoodNotes
  - Pre-drawn tables and lined pages sized for Apple Pencil handwriting
  - Pink / gold / cream luxury colour scheme throughout
  - Generates US Letter AND A4 versions

Usage:
    pip install reportlab
    python wedding_pdf_goodnotes.py

Output:
    Bold_Balanced_Wedding_Bible_GoodNotes_Letter.pdf
    Bold_Balanced_Wedding_Bible_GoodNotes_A4.pdf
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

# ─────────────────────────────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────────
C = {
    "hot_pink":   HexColor("#E91E8C"),
    "pink":       HexColor("#F48FB1"),
    "light_pink": HexColor("#FCE4EC"),
    "blush":      HexColor("#FDE8EE"),
    "yellow":     HexColor("#FFE082"),
    "gold":       HexColor("#C9A84C"),
    "light_gold": HexColor("#FFF9C4"),
    "black":      HexColor("#212121"),
    "cream":      HexColor("#FFF8E7"),
    "white":      HexColor("#FFFFFF"),
    "rose_gold":  HexColor("#B76E79"),
    "dark_pink":  HexColor("#AD1457"),
    "border":     HexColor("#E0C0CC"),
    "line":       HexColor("#F2DCE4"),
    "light_gray": HexColor("#F5F5F5"),
    "gold_line":  HexColor("#D4AF37"),
}

# ─────────────────────────────────────────────────────────────────────
# SECTION DEFINITIONS  (id, short tab label, colour, full name)
# ─────────────────────────────────────────────────────────────────────
SECTIONS = [
    {"id": "cover",     "label": "COVER",    "name": "Cover",           "color": C["hot_pink"]},
    {"id": "welcome",   "label": "WELCOME",  "name": "Welcome",         "color": C["pink"]},
    {"id": "overview",  "label": "DETAILS",  "name": "Wedding Details", "color": C["rose_gold"]},
    {"id": "budget",    "label": "BUDGET",   "name": "Budget Tracker",  "color": C["gold"]},
    {"id": "guests",    "label": "GUESTS",   "name": "Guest List",      "color": C["light_pink"]},
    {"id": "vendors",   "label": "VENDORS",  "name": "Vendor Tracker",  "color": C["rose_gold"]},
    {"id": "timeline",  "label": "TIMELINE", "name": "Day-of Timeline", "color": C["dark_pink"]},
    {"id": "checklist", "label": "TASKS",    "name": "Checklist",       "color": C["yellow"]},
    {"id": "bridal",    "label": "BRIDAL",   "name": "Bridal Party",    "color": C["pink"]},
    {"id": "seating",   "label": "SEATING",  "name": "Seating Chart",   "color": C["blush"]},
    {"id": "registry",  "label": "GIFTS",    "name": "Gift Registry",   "color": C["hot_pink"]},
    {"id": "honeymoon", "label": "MOON",     "name": "Honeymoon",       "color": C["gold"]},
]
N_SECTIONS = len(SECTIONS)

_SEC = {s["id"]: s for s in SECTIONS}


# ─────────────────────────────────────────────────────────────────────
# PDF BUILDER
# ─────────────────────────────────────────────────────────────────────

class WeddingPDF:
    TAB_W   = 40          # width of right-side tab strip
    HDR_H   = 50          # height of top header band
    MARGIN  = 16          # general page margin
    LN_SP   = 26          # ruled line spacing (handwriting rows)

    def __init__(self, path: str, pagesize=letter) -> None:
        self.path = path
        self.W, self.H = pagesize
        self.c = Canvas(path, pagesize=pagesize)
        self._pages = 0

        # Usable content rectangle
        self.CX  = self.MARGIN
        self.CY  = self.MARGIN
        self.CW  = self.W - self.TAB_W - self.MARGIN * 2
        self.CH  = self.H - self.HDR_H - self.MARGIN * 2
        self.CTH = self.H - self.HDR_H    # content top y
        self.TAB_ITEM_H = (self.H - self.HDR_H) / N_SECTIONS

    # ── Low-level drawing helpers ─────────────────────────────────

    def _rect(self, x, y, w, h, fill=None, stroke=None, lw=0.5) -> None:
        c = self.c
        c.setLineWidth(lw)
        if fill:
            c.setFillColor(fill)
        if stroke:
            c.setStrokeColor(stroke)
        c.rect(x, y, w, h,
               fill=1 if fill else 0,
               stroke=1 if stroke else 0)

    def _text(self, x, y, text, font="Helvetica", size=10,
              color=None, align="left") -> None:
        c = self.c
        c.setFont(font, size)
        c.setFillColor(color or C["black"])
        if align == "center":
            c.drawCentredString(x, y, text)
        elif align == "right":
            c.drawRightString(x, y, text)
        else:
            c.drawString(x, y, text)

    def _line(self, x1, y1, x2, y2, color=None, lw=0.5) -> None:
        c = self.c
        c.setStrokeColor(color or C["border"])
        c.setLineWidth(lw)
        c.line(x1, y1, x2, y2)

    # ── Page structure ────────────────────────────────────────────

    def draw_tabs(self, active_id: str) -> None:
        c = self.c
        for i, sec in enumerate(SECTIONS):
            x = self.W - self.TAB_W
            y = self.H - self.HDR_H - (i + 1) * self.TAB_ITEM_H
            h = self.TAB_ITEM_H
            is_active = sec["id"] == active_id

            # Active tab extends into content area
            extra = 6 if is_active else 0
            self._rect(x - extra, y, self.TAB_W + extra, h,
                       fill=sec["color"])

            # Thin separator line between tabs
            self._line(x - extra, y, self.W, y, color=C["white"], lw=0.8)

            # Rotated label
            c.saveState()
            c.setFont("Helvetica-Bold" if is_active else "Helvetica", 6.5)
            c.setFillColor(white if is_active else C["black"])
            mid_x = x - extra + (self.TAB_W + extra) / 2
            mid_y = y + h / 2
            c.translate(mid_x, mid_y)
            c.rotate(270)
            c.drawCentredString(0, -2.5, sec["label"])
            c.restoreState()

            # Hyperlink for non-active tabs
            if not is_active:
                c.linkRect("", sec["id"],
                           (x, y, self.W, y + h),
                           thickness=0)

        # Divider between content and tabs
        self._line(self.W - self.TAB_W, 0,
                   self.W - self.TAB_W, self.H,
                   color=C["border"], lw=0.8)

    def draw_header(self, section_id: str, page_title: str = "") -> None:
        sec = _SEC[section_id]
        c = self.c

        # Header fill
        self._rect(0, self.H - self.HDR_H,
                   self.W - self.TAB_W, self.HDR_H,
                   fill=sec["color"])

        # Gold top accent strip
        self._rect(0, self.H - 4,
                   self.W - self.TAB_W, 4,
                   fill=C["gold_line"])

        # Top micro-label
        self._text(self.MARGIN, self.H - 14,
                   "Bold & Balanced Wedding Bible",
                   size=6.5, color=white)

        # Page / section title
        title = page_title or sec["name"]
        self._text(self.MARGIN, self.H - self.HDR_H + 13,
                   title, font="Helvetica-Bold", size=17, color=white)

        # Thin gold rule under header
        self._line(0, self.H - self.HDR_H,
                   self.W - self.TAB_W, self.H - self.HDR_H,
                   color=C["gold_line"], lw=1)

    def new_page(self, section_id: str, page_title: str = "",
                 bookmark: bool = False) -> None:
        if self._pages > 0:
            self.c.showPage()
        self._pages += 1

        # White background
        self._rect(0, 0, self.W, self.H, fill=C["white"])

        if bookmark:
            self.c.bookmarkPage(section_id)

        self.draw_header(section_id, page_title)
        self.draw_tabs(section_id)

    # ── Reusable content components ───────────────────────────────

    def ruled_lines(self, x: float, y_top: float,
                    width: float, height: float) -> None:
        y = y_top - self.LN_SP
        while y > y_top - height:
            self._line(x, y, x + width, y, color=C["line"])
            y -= self.LN_SP

    def field_row(self, x: float, y: float, width: float,
                  label: str, wide: bool = False) -> float:
        """Draw one labelled input line. Returns y of next row."""
        h = 22
        self._text(x, y + 6, label.upper(),
                   font="Helvetica-Bold", size=7, color=C["dark_pink"])
        lw = width if wide else width * 0.55
        self._line(x + 70, y, x + lw, y, color=C["border"])
        return y - h

    def section_divider(self, section_id: str, subtitle: str = "") -> None:
        """Full-bleed section opening page."""
        sec = _SEC[section_id]
        self.new_page(section_id, sec["name"], bookmark=True)
        c = self.c

        # Full-bleed color panel (below header)
        self._rect(0, 0, self.W - self.TAB_W, self.H - self.HDR_H,
                   fill=sec["color"])

        # Cream inner panel
        pad = 28
        py = pad
        self._rect(pad, py,
                   self.W - self.TAB_W - pad * 2,
                   self.H - self.HDR_H - pad * 2,
                   fill=C["cream"])

        # Gold top accent inside panel
        self._rect(pad, self.H - self.HDR_H - pad - 6,
                   self.W - self.TAB_W - pad * 2, 6,
                   fill=C["gold_line"])

        # Section name (large)
        cx = (self.W - self.TAB_W) / 2
        cy = (self.H - self.HDR_H) / 2 + 20
        self._text(cx, cy + 40, "✦", font="Helvetica-Bold",
                   size=28, color=sec["color"], align="center")
        self._text(cx, cy, sec["name"], font="Helvetica-Bold",
                   size=26, color=sec["color"], align="center")
        if subtitle:
            self._text(cx, cy - 28, subtitle,
                       size=11, color=C["rose_gold"], align="center")

        # Gold rule
        rule_w = 160
        self._line(cx - rule_w / 2, cy - 18,
                   cx + rule_w / 2, cy - 18,
                   color=C["gold_line"], lw=1.2)

        # Bottom nav hint
        self._text(cx, py + 18,
                   "Use the tabs on the right to navigate",
                   size=8, color=C["rose_gold"], align="center")

    def table_page(self, section_id: str, page_title: str,
                   headers: list[str], col_widths: list[float],
                   rows: int = 22, row_h: float = 22) -> None:
        """Draw a full-page data table with alternating row shading."""
        self.new_page(section_id, page_title)
        x0 = self.CX
        y0 = self.CTH - self.MARGIN

        # Header row
        hdr_h = 26
        x = x0
        for col_w, hdr in zip(col_widths, headers):
            self._rect(x, y0 - hdr_h, col_w, hdr_h,
                       fill=_SEC[section_id]["color"])
            self._text(x + 4, y0 - hdr_h + 8, hdr,
                       font="Helvetica-Bold", size=7.5, color=white)
            x += col_w

        # Data rows
        y = y0 - hdr_h
        for r in range(rows):
            bg = C["blush"] if r % 2 == 0 else C["white"]
            x = x0
            for col_w in col_widths:
                self._rect(x, y - row_h, col_w, row_h,
                           fill=bg, stroke=C["border"], lw=0.3)
                x += col_w
            y -= row_h
            if y < self.MARGIN + row_h:
                break

    def checklist_column(self, x: float, y_start: float,
                         items: list[str], color=None) -> float:
        """Draw a column of checkbox items. Returns last y."""
        color = color or C["dark_pink"]
        box_size = 9
        lh = 20
        y = y_start
        for item in items:
            # Checkbox
            self._rect(x, y - box_size + 2, box_size, box_size,
                       stroke=color, lw=0.8)
            self._text(x + box_size + 6, y - 1, item,
                       size=8.5, color=C["black"])
            y -= lh
        return y

    def stat_box(self, x: float, y: float, w: float, h: float,
                 label: str, color=None) -> None:
        color = color or C["light_pink"]
        self._rect(x, y, w, h, fill=color, stroke=C["border"], lw=0.5)
        cx = x + w / 2
        self._text(cx, y + h * 0.55, label,
                   font="Helvetica-Bold", size=8, color=C["dark_pink"],
                   align="center")
        # Line for value
        self._line(x + 10, y + h * 0.25, x + w - 10, y + h * 0.25,
                   color=C["border"])

    # ─────────────────────────────────────────────────────────────
    # SECTION BUILDERS
    # ─────────────────────────────────────────────────────────────

    def build_cover(self) -> None:
        c = self.c
        self.c.showPage() if self._pages > 0 else None
        self._pages += 1
        self.c.bookmarkPage("cover")

        # Full bleed background
        self._rect(0, 0, self.W, self.H, fill=C["hot_pink"])

        # Cream inner panel
        pad = 32
        self._rect(pad, pad,
                   self.W - self.TAB_W - pad * 2,
                   self.H - pad * 2, fill=C["cream"])

        # Gold accent bars
        self._rect(pad, self.H - pad - 8,
                   self.W - self.TAB_W - pad * 2, 8, fill=C["gold_line"])
        self._rect(pad, pad, self.W - self.TAB_W - pad * 2, 8,
                   fill=C["gold_line"])

        # Blush inner inner panel
        inner_pad = pad + 22
        self._rect(inner_pad, inner_pad + 20,
                   self.W - self.TAB_W - inner_pad * 2,
                   self.H - inner_pad * 2 - 40, fill=C["blush"])

        cx = (self.W - self.TAB_W) / 2

        # Top decorative mark
        self._text(cx, self.H - 70, "✦  ✦  ✦",
                   font="Helvetica-Bold", size=14, color=C["gold_line"],
                   align="center")

        # Main title
        self._text(cx, self.H - 110,
                   "Bold & Balanced",
                   font="Helvetica-Bold", size=30, color=C["dark_pink"],
                   align="center")
        self._text(cx, self.H - 140,
                   "Wedding Bible",
                   font="Helvetica-Bold", size=30, color=C["hot_pink"],
                   align="center")

        # Subtitle
        self._text(cx, self.H - 170,
                   "Modern Luxury Wedding Planning System",
                   font="Helvetica", size=12, color=C["rose_gold"],
                   align="center")

        # Gold divider
        self._line(cx - 100, self.H - 186,
                   cx + 100, self.H - 186,
                   color=C["gold_line"], lw=1.5)

        # Input fields
        field_x = inner_pad + 20
        field_w = self.W - self.TAB_W - inner_pad * 2 - 40

        y = self.H - 230
        for label in ["Bride's Name", "Groom's Name", "Wedding Date",
                       "Wedding Venue"]:
            self._text(field_x, y + 6, label.upper(),
                       font="Helvetica-Bold", size=8, color=C["dark_pink"])
            self._line(field_x + 90, y, field_x + field_w, y,
                       color=C["border"], lw=0.8)
            y -= 32

        # Decorative rule
        self._line(cx - 100, y - 10, cx + 100, y - 10,
                   color=C["gold_line"], lw=1)

        # Footer
        self._text(cx, pad + 32,
                   "Marigold Bride  ✦  marigoldbride.com",
                   size=7.5, color=C["rose_gold"], align="center")
        self._text(cx, pad + 18,
                   "Use the tabs on the right to navigate your planner",
                   size=7, color=C["gold"], align="center")

        # Tabs
        self.draw_tabs("cover")

    def build_welcome(self) -> None:
        # Page 1: How to use
        self.section_divider("welcome", "Your digital wedding companion")

        self.new_page("welcome", "How to Use This Planner")
        cx = (self.W - self.TAB_W) / 2
        y = self.CTH - self.MARGIN - 10

        # Intro
        self._text(self.CX, y, "WELCOME TO YOUR BOLD & BALANCED WEDDING BIBLE",
                   font="Helvetica-Bold", size=9, color=C["dark_pink"])
        y -= 20
        self._line(self.CX, y, self.CX + self.CW, y, color=C["gold_line"], lw=1)
        y -= 18

        tips = [
            ("NAVIGATING",   "Tap any coloured tab on the right to jump to that section instantly."),
            ("WRITING",      "Use your Apple Pencil or stylus to fill in every field and table."),
            ("ADDING PAGES", "In GoodNotes, long-press a page thumbnail and choose 'Add Page' to "
                             "expand any section."),
            ("TEMPLATES",    "Duplicate this planner at the start to keep a blank master copy."),
            ("BACKUPS",      "Export as PDF regularly and save to iCloud or Google Drive."),
            ("SHARING",      "Export individual pages to share with vendors, photographers, "
                             "or your wedding planner."),
        ]

        for title, body in tips:
            # Title badge
            badge_w = 120
            self._rect(self.CX, y - 14, badge_w, 18,
                       fill=C["hot_pink"])
            self._text(self.CX + 6, y - 7, title,
                       font="Helvetica-Bold", size=7.5, color=white)
            # Body text
            self._text(self.CX + badge_w + 10, y - 7, body,
                       size=8, color=C["black"])
            y -= 36

        self._line(self.CX, y + 10, self.CX + self.CW, y + 10,
                   color=C["gold_line"], lw=1)
        y -= 24

        self._text(cx, y, "WHAT'S INSIDE YOUR PLANNER",
                   font="Helvetica-Bold", size=9, color=C["dark_pink"],
                   align="center")
        y -= 20

        # Two-column section list
        col1 = [s["name"] for s in SECTIONS[1:7]]
        col2 = [s["name"] for s in SECTIONS[7:]]
        col_w = self.CW / 2 - 10

        for i, (s1, s2) in enumerate(zip(col1, col2)):
            bg = C["blush"] if i % 2 == 0 else C["white"]
            self._rect(self.CX, y - 16, col_w, 18, fill=bg)
            self._rect(self.CX + col_w + 10, y - 16, col_w, 18, fill=bg)
            self._text(self.CX + 8, y - 6, f"  {s1}", size=8.5)
            self._text(self.CX + col_w + 18, y - 6, f"  {s2}", size=8.5)
            y -= 20

    def build_overview(self) -> None:
        self.section_divider("overview", "All your wedding details in one place")

        # Page 1: The Couple + Key Dates
        self.new_page("overview", "The Couple & Key Dates")
        y = self.CTH - self.MARGIN - 8

        for block_title, fields in [
            ("THE COUPLE", ["Bride's Full Name", "Groom's Full Name",
                            "Wedding Date", "Engagement Date",
                            "How We Met", "Wedding Hashtag"]),
            ("IMPORTANT DATES", ["Save the Dates Sent", "Invitations Sent",
                                 "RSVP Deadline", "Final Headcount Due",
                                 "Rehearsal Date", "Rehearsal Dinner"]),
        ]:
            self._rect(self.CX, y - 18, self.CW, 20,
                       fill=_SEC["overview"]["color"])
            self._text(self.CX + 8, y - 7, f"  {block_title}",
                       font="Helvetica-Bold", size=9, color=white)
            y -= 26
            for label in fields:
                self._text(self.CX + 4, y + 5, label,
                           font="Helvetica-Bold", size=8, color=C["dark_pink"])
                self._line(self.CX + 130, y, self.CX + self.CW, y,
                           color=C["border"])
                y -= 24
            y -= 8

        # Page 2: Venues & Contacts
        self.new_page("overview", "Venues & Key Contacts")
        y = self.CTH - self.MARGIN - 8

        for block_title, fields in [
            ("CEREMONY VENUE", ["Venue Name", "Address", "City / State",
                                "Ceremony Time", "Ceremony End", "Contact Name"]),
            ("RECEPTION VENUE", ["Venue Name", "Address", "City / State",
                                 "Doors Open", "Reception End", "Contact Name"]),
            ("KEY CONTACTS", ["Wedding Planner", "Planner Phone",
                              "Officiant", "Officiant Phone",
                              "Emergency Contact", "Emergency Phone"]),
        ]:
            self._rect(self.CX, y - 18, self.CW, 20,
                       fill=_SEC["overview"]["color"])
            self._text(self.CX + 8, y - 7, f"  {block_title}",
                       font="Helvetica-Bold", size=9, color=white)
            y -= 26
            for label in fields:
                self._text(self.CX + 4, y + 5, label,
                           font="Helvetica-Bold", size=8, color=C["dark_pink"])
                self._line(self.CX + 130, y, self.CX + self.CW, y,
                           color=C["border"])
                y -= 22
            y -= 8

    def build_budget(self) -> None:
        self.section_divider("budget", "Track every penny — no surprises")

        # Summary page
        self.new_page("budget", "Budget Summary")
        y = self.CTH - self.MARGIN - 8
        box_w = (self.CW - 10) / 3
        box_h = 50

        for i, (lbl, sub) in enumerate([
            ("TOTAL BUDGET", "Fill in your total"),
            ("TOTAL SPENT",  "Running total"),
            ("BALANCE LEFT", "Budget - Spent"),
        ]):
            bx = self.CX + i * (box_w + 5)
            color = [C["light_gold"], C["light_pink"], C["blush"]][i]
            self._rect(bx, y - box_h, box_w, box_h,
                       fill=color, stroke=C["border"], lw=0.5)
            self._text(bx + box_w / 2, y - 10, lbl,
                       font="Helvetica-Bold", size=8, color=C["dark_pink"],
                       align="center")
            self._line(bx + 10, y - box_h * 0.5,
                       bx + box_w - 10, y - box_h * 0.5,
                       color=C["border"])
            self._text(bx + box_w / 2, y - box_h + 8, sub,
                       size=7, color=C["rose_gold"], align="center")

        y -= box_h + 14

        # Category summary table
        self._rect(self.CX, y - 20, self.CW, 22, fill=C["hot_pink"])
        for i, hdr in enumerate(["CATEGORY", "BUDGETED", "ESTIMATED",
                                  "PAID", "BALANCE"]):
            hx = self.CX + i * self.CW / 5 + 4
            self._text(hx, y - 10, hdr,
                       font="Helvetica-Bold", size=7.5, color=white)
        y -= 22

        categories = [
            "Venue", "Catering", "Photography", "Videography",
            "Florals", "Music / DJ", "Attire & Beauty", "Transportation",
            "Stationery", "Rings", "Honeymoon", "Gifts & Favors",
            "Cake & Desserts", "Officiant", "Lighting & Decor", "Other",
        ]
        row_h = 20
        for i, cat in enumerate(categories):
            bg = C["blush"] if i % 2 == 0 else C["white"]
            self._rect(self.CX, y - row_h, self.CW, row_h,
                       fill=bg, stroke=C["border"], lw=0.2)
            self._text(self.CX + 4, y - row_h + 6, cat,
                       font="Helvetica-Bold", size=8)
            for j in range(1, 5):
                col_x = self.CX + j * self.CW / 5
                self._line(col_x, y - row_h, col_x, y,
                           color=C["border"], lw=0.3)
            y -= row_h
            if y < self.MARGIN:
                break

        # Detail pages
        hdrs = ["CATEGORY", "ITEM / DESCRIPTION", "BUDGET", "ESTIMATED",
                "PAID", "STATUS", "NOTES"]
        widths = [self.CW * f for f in [0.14, 0.26, 0.10, 0.10, 0.10, 0.14, 0.16]]
        for pg in range(3):
            self.table_page("budget", f"Budget Detail — Page {pg + 1}",
                            hdrs, widths, rows=24, row_h=22)

    def build_guests(self) -> None:
        self.section_divider("guests", "Keep track of every guest and RSVP")

        # Stats page
        self.new_page("guests", "Guest List Overview")
        y = self.CTH - self.MARGIN - 8

        stats = [("TOTAL INVITED", C["light_pink"]),
                 ("RSVP  YES",     C["blush"]),
                 ("RSVP  NO",      C["light_pink"]),
                 ("PENDING",       C["yellow"]),
                 ("TOTAL ADULTS",  C["blush"]),
                 ("TOTAL KIDS",    C["light_gold"])]

        box_w = (self.CW - 10) / 3
        box_h = 48
        for i, (lbl, bg) in enumerate(stats):
            row = i // 3
            col = i % 3
            bx = self.CX + col * (box_w + 5)
            by = y - row * (box_h + 8) - box_h
            self._rect(bx, by, box_w, box_h,
                       fill=bg, stroke=C["border"], lw=0.5)
            self._text(bx + box_w / 2, by + box_h - 12, lbl,
                       font="Helvetica-Bold", size=7.5, color=C["dark_pink"],
                       align="center")
            self._line(bx + 12, by + box_h * 0.42,
                       bx + box_w - 12, by + box_h * 0.42,
                       color=C["border"])

        y -= 2 * (box_h + 8) + 20

        # Notes area label
        self._rect(self.CX, y - 16, self.CW, 18, fill=C["rose_gold"])
        self._text(self.CX + 8, y - 6, "  NOTES & REMINDERS",
                   font="Helvetica-Bold", size=8.5, color=white)
        y -= 24
        self.ruled_lines(self.CX, y + self.LN_SP * 6,
                         self.CW, self.LN_SP * 6)

        # Guest table pages
        hdrs = ["#", "FIRST NAME", "LAST NAME", "GROUP",
                "ADULTS", "KIDS", "RSVP", "MEAL", "TABLE", "GIFT", "TY"]
        widths = [self.CW * f for f in
                  [0.04, 0.12, 0.12, 0.12, 0.06, 0.05,
                   0.08, 0.10, 0.07, 0.06, 0.06, 0.12]]
        # trim to exactly CW
        total = sum(widths)
        widths = [w / total * self.CW for w in widths]

        for pg in range(4):
            self.table_page("guests", f"Guest List — Page {pg + 1}",
                            hdrs, widths, rows=24, row_h=21)

    def build_vendors(self) -> None:
        self.section_divider("vendors", "All your vendors in one place")

        hdrs = ["CATEGORY", "VENDOR / COMPANY", "CONTACT",
                "PHONE", "EMAIL", "DEPOSIT PAID", "BALANCE", "STATUS"]
        widths = [self.CW * f for f in
                  [0.13, 0.20, 0.14, 0.12, 0.18, 0.10, 0.08, 0.05]]
        total = sum(widths)
        widths = [w / total * self.CW for w in widths]

        for pg in range(3):
            self.table_page("vendors", f"Vendor Tracker — Page {pg + 1}",
                            hdrs, widths, rows=22, row_h=22)

    def build_timeline(self) -> None:
        self.section_divider("timeline", "Your minute-by-minute wedding day")

        hdrs = ["TIME", "EVENT / ACTIVITY", "LOCATION",
                "PERSON / VENDOR", "NOTES"]
        widths = [self.CW * f for f in [0.12, 0.28, 0.22, 0.22, 0.16]]

        for pg in range(3):
            self.table_page("timeline", f"Day-of Timeline — Page {pg + 1}",
                            hdrs, widths, rows=26, row_h=21)

    def build_checklist(self) -> None:
        self.section_divider("checklist", "Every task from yes to I do")

        phases = [
            ("12+ Months Out", [
                "Set your wedding budget",
                "Create your initial guest list",
                "Choose your wedding date",
                "Book ceremony & reception venues",
                "Hire a wedding planner (optional)",
                "Start dress shopping",
                "Set up a wedding website",
                "Begin researching photographers",
            ]),
            ("9 - 12 Months", [
                "Book photographer & videographer",
                "Book your caterer",
                "Book florist",
                "Book DJ or live band",
                "Send save-the-dates",
                "Order your wedding dress",
                "Book hair & makeup artist",
                "Choose bridesmaids dresses",
            ]),
            ("6 - 9 Months", [
                "Book honeymoon travel & accommodation",
                "Plan honeymoon itinerary",
                "Order invitations & stationery",
                "Book transportation",
                "Schedule cake tasting",
                "Buy wedding rings",
                "Plan rehearsal dinner",
                "Book accommodation for out-of-town guests",
            ]),
            ("4 - 6 Months", [
                "Send wedding invitations",
                "Create wedding registry",
                "Order wedding cake",
                "Plan ceremony details with officiant",
                "Arrange hotel room blocks for guests",
                "Shop for wedding party gifts",
                "Schedule dress fittings",
                "Finalise wedding menu",
            ]),
            ("2 - 4 Months", [
                "Chase RSVP responses",
                "Finalise guest list and headcount",
                "Create seating plan",
                "Write your vows",
                "Confirm all vendors",
                "Arrange name change documents",
                "Buy wedding day accessories",
                "Create day-of timeline for vendors",
            ]),
            ("1 Month - Week Out", [
                "Final dress fitting",
                "Prepare payments & tips for vendors",
                "Confirm final headcount with caterer",
                "Distribute day-of timeline to all",
                "Prepare wedding emergency kit",
                "Delegate tasks to bridal party",
                "Break in your wedding shoes",
                "Write thank-you speech notes",
            ]),
            ("Wedding Day", [
                "Wake up early & eat breakfast",
                "Hair & makeup",
                "Get dressed - enjoy every moment!",
                "First look (if planned)",
                "Wedding party photos",
                "CEREMONY - you did it!",
                "Cocktail hour",
                "Grand reception entrance",
            ]),
            ("After Wedding", [
                "Send thank-you cards",
                "Return any rentals",
                "Change your name (if applicable)",
                "Preserve your wedding dress",
                "Write vendor reviews",
                "Share photos with guests",
                "Order photo prints / album",
                "Relax - you're married!",
            ]),
        ]

        col_w = (self.CW - 16) / 2  # two columns per page

        for i in range(0, len(phases), 2):
            self.new_page("checklist",
                          f"Checklist — {phases[i][0]}"
                          + (f" & {phases[i+1][0]}" if i + 1 < len(phases) else ""))
            y = self.CTH - self.MARGIN - 6

            for col_idx in range(2):
                if i + col_idx >= len(phases):
                    break
                phase_title, tasks = phases[i + col_idx]
                cx = self.CX + col_idx * (col_w + 16)

                # Phase header
                self._rect(cx, y - 20, col_w, 22,
                           fill=_SEC["checklist"]["color"])
                self._text(cx + 8, y - 9, phase_title,
                           font="Helvetica-Bold", size=9,
                           color=C["black"])

                ty = y - 28
                self.checklist_column(cx + 4, ty, tasks,
                                      color=C["dark_pink"])

    def build_bridal_party(self) -> None:
        self.section_divider("bridal", "Your dream team")

        for group, title in [("Bridesmaids & Maid of Honor",
                               "Bridal Party — Bride's Side"),
                              ("Groomsmen & Best Man",
                               "Bridal Party — Groom's Side")]:
            self.new_page("bridal", title)
            y = self.CTH - self.MARGIN - 6

            # Role + name header row
            col_labels = ["ROLE", "FULL NAME", "PHONE",
                          "ATTIRE COLOUR", "SIZE", "ORDERED?", "FITTING DATE"]
            widths = [self.CW * f for f in
                      [0.14, 0.19, 0.14, 0.17, 0.10, 0.10, 0.16]]
            hdr_h = 22
            x = self.CX
            self._rect(self.CX, y - hdr_h, self.CW, hdr_h,
                       fill=_SEC["bridal"]["color"])
            for lbl, cw_ in zip(col_labels, widths):
                self._text(x + 4, y - hdr_h + 7, lbl,
                           font="Helvetica-Bold", size=7, color=white)
                x += cw_
            y -= hdr_h

            row_h = 28
            for r in range(12):
                bg = C["blush"] if r % 2 == 0 else C["white"]
                x = self.CX
                for cw_ in widths:
                    self._rect(x, y - row_h, cw_, row_h,
                               fill=bg, stroke=C["border"], lw=0.3)
                    x += cw_
                y -= row_h
                if y < self.MARGIN:
                    break

            y -= 14
            self._rect(self.CX, y - 18, self.CW, 20, fill=C["rose_gold"])
            self._text(self.CX + 8, y - 7, "  NOTES",
                       font="Helvetica-Bold", size=8, color=white)
            y -= 26
            self.ruled_lines(self.CX, y + self.LN_SP * 4, self.CW,
                             self.LN_SP * 4)

    def build_seating(self) -> None:
        self.section_divider("seating", "Place every guest perfectly")

        # Table planner pages — 2 tables per page, 4 pages = 8 tables
        for page_num in range(3):
            self.new_page("seating", f"Seating Chart — Page {page_num + 1}")
            y = self.CTH - self.MARGIN - 6
            table_w = (self.CW - 12) / 2
            seats_per_table = 10

            for col in range(2):
                table_num = page_num * 2 + col + 1
                tx = self.CX + col * (table_w + 12)

                # Table header
                self._rect(tx, y - 22, table_w, 24,
                           fill=C["rose_gold"] if col == 0 else C["pink"])
                self._text(tx + table_w / 2, y - 9,
                           f"TABLE {table_num}",
                           font="Helvetica-Bold", size=10, color=white,
                           align="center")
                seat_y = y - 26

                for seat in range(1, seats_per_table + 1):
                    bg = C["blush"] if seat % 2 == 0 else C["white"]
                    self._rect(tx, seat_y - 20, table_w, 20,
                               fill=bg, stroke=C["border"], lw=0.3)
                    self._text(tx + 6, seat_y - 11,
                               f"{seat}.", size=8.5, color=C["rose_gold"])
                    self._line(tx + 26, seat_y - 14,
                               tx + table_w - 8, seat_y - 14,
                               color=C["border"])
                    seat_y -= 20

    def build_registry(self) -> None:
        self.section_divider("registry", "Track every gift with gratitude")

        # Stats
        self.new_page("registry", "Registry Overview")
        y = self.CTH - self.MARGIN - 8

        for i, (lbl, bg) in enumerate([
            ("TOTAL ITEMS ON REGISTRY",   C["light_pink"]),
            ("ITEMS PURCHASED",           C["blush"]),
            ("THANK-YOU CARDS SENT",      C["light_gold"]),
        ]):
            bw = (self.CW - 10) / 3
            bx = self.CX + i * (bw + 5)
            self._rect(bx, y - 44, bw, 46, fill=bg, stroke=C["border"], lw=0.5)
            self._text(bx + bw / 2, y - 12, lbl,
                       font="Helvetica-Bold", size=7, color=C["dark_pink"],
                       align="center")
            self._line(bx + 10, y - 28, bx + bw - 10, y - 28, color=C["border"])

        y -= 60

        # Wishlist note section
        self._rect(self.CX, y - 18, self.CW, 20, fill=C["hot_pink"])
        self._text(self.CX + 8, y - 7, "  REGISTRY NOTES & LINKS",
                   font="Helvetica-Bold", size=8.5, color=white)
        y -= 26
        self.ruled_lines(self.CX, y + self.LN_SP * 8, self.CW, self.LN_SP * 8)

        # Registry table pages
        hdrs = ["ITEM / GIFT", "STORE / WEBSITE", "PRICE",
                "QTY WANTED", "QTY RECEIVED", "PURCHASED?",
                "RECEIVED FROM", "THANK YOU SENT?"]
        widths = [self.CW * f for f in
                  [0.22, 0.18, 0.09, 0.09, 0.09, 0.09, 0.15, 0.09]]
        total = sum(widths)
        widths = [w / total * self.CW for w in widths]

        for pg in range(3):
            self.table_page("registry", f"Gift Registry — Page {pg + 1}",
                            hdrs, widths, rows=22, row_h=22)

    def build_honeymoon(self) -> None:
        self.section_divider("honeymoon", "Your dream getaway starts here")

        # Destination details
        self.new_page("honeymoon", "Honeymoon Details")
        y = self.CTH - self.MARGIN - 8

        self._rect(self.CX, y - 18, self.CW, 20,
                   fill=_SEC["honeymoon"]["color"])
        self._text(self.CX + 8, y - 7, "  DESTINATION & BOOKING",
                   font="Helvetica-Bold", size=9, color=white)
        y -= 26

        for label in ["Destination", "Departure Date", "Return Date",
                       "Number of Nights", "Hotel / Resort",
                       "Flight Confirmation #", "Hotel Confirmation #",
                       "Travel Insurance #", "Emergency Contact Abroad"]:
            self._text(self.CX + 4, y + 5, label,
                       font="Helvetica-Bold", size=8, color=C["dark_pink"])
            self._line(self.CX + 140, y, self.CX + self.CW, y,
                       color=C["border"])
            y -= 24

        y -= 10
        self._rect(self.CX, y - 18, self.CW, 20, fill=C["rose_gold"])
        self._text(self.CX + 8, y - 7, "  PACKING LIST NOTES",
                   font="Helvetica-Bold", size=9, color=white)
        y -= 26
        self.ruled_lines(self.CX, y + self.LN_SP * 5, self.CW, self.LN_SP * 5)

        # Itinerary page
        hdrs = ["DAY #", "DATE", "ACTIVITY / PLAN",
                "LOCATION", "BOOKING REF", "COST", "NOTES"]
        widths = [self.CW * f for f in
                  [0.07, 0.12, 0.26, 0.18, 0.12, 0.09, 0.16]]
        self.table_page("honeymoon", "Honeymoon Itinerary",
                        hdrs, widths, rows=26, row_h=22)

        # Budget page
        self.new_page("honeymoon", "Honeymoon Budget")
        y = self.CTH - self.MARGIN - 8

        hdrs2 = ["EXPENSE CATEGORY", "BUDGETED", "ACTUAL COST",
                 "PAID?", "NOTES"]
        widths2 = [self.CW * f for f in [0.30, 0.16, 0.16, 0.12, 0.26]]
        hdr_h = 24
        self._rect(self.CX, y - hdr_h, self.CW, hdr_h,
                   fill=_SEC["honeymoon"]["color"])
        x = self.CX
        for hdr, cw_ in zip(hdrs2, widths2):
            self._text(x + 4, y - hdr_h + 8, hdr,
                       font="Helvetica-Bold", size=8, color=white)
            x += cw_
        y -= hdr_h

        honey_cats = ["Flights", "Accommodation", "Activities & Tours",
                      "Food & Dining", "Shopping", "Travel Insurance",
                      "Airport Transfers", "Visa & Entry Fees",
                      "Spending Money", "Other"]
        row_h = 24
        for i, cat in enumerate(honey_cats):
            bg = C["light_gold"] if i % 2 == 0 else C["cream"]
            x = self.CX
            for j, cw_ in enumerate(widths2):
                self._rect(x, y - row_h, cw_, row_h,
                           fill=bg, stroke=C["border"], lw=0.3)
                if j == 0:
                    self._text(x + 6, y - row_h + 8, cat,
                               font="Helvetica-Bold", size=8.5)
                x += cw_
            y -= row_h

        # Total row
        self._rect(self.CX, y - row_h, self.CW, row_h,
                   fill=_SEC["honeymoon"]["color"])
        self._text(self.CX + 6, y - row_h + 8, "TOTAL",
                   font="Helvetica-Bold", size=9, color=white)
        y -= row_h + 14

        self._rect(self.CX, y - 18, self.CW, 20, fill=C["rose_gold"])
        self._text(self.CX + 8, y - 7, "  HONEYMOON NOTES & MEMORIES",
                   font="Helvetica-Bold", size=8.5, color=white)
        y -= 26
        self.ruled_lines(self.CX, y + self.LN_SP * 6, self.CW, self.LN_SP * 6)

    # ─────────────────────────────────────────────────────────────
    # MASTER BUILD
    # ─────────────────────────────────────────────────────────────

    def build(self) -> None:
        self.build_cover()
        self.build_welcome()
        self.build_overview()
        self.build_budget()
        self.build_guests()
        self.build_vendors()
        self.build_timeline()
        self.build_checklist()
        self.build_bridal_party()
        self.build_seating()
        self.build_registry()
        self.build_honeymoon()
        self.c.save()
        print(f"  ✓ Saved: {self.path}  ({self._pages} pages)")


# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    out = Path(__file__).parents[4] / "output"
    out.mkdir(exist_ok=True)

    for label, pagesize in [("Letter", letter), ("A4", A4)]:
        path = str(out / f"Bold_Balanced_Wedding_Bible_GoodNotes_{label}.pdf")
        print(f"Building GoodNotes PDF ({label}) …")
        WeddingPDF(path, pagesize=pagesize).build()

    print("\nDone! Both PDFs are ready.")


if __name__ == "__main__":
    main()
