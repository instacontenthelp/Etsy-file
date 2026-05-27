"""
Bold & Balanced Wedding Bible: Modern Luxury Wedding Planning System
Python openpyxl generator

Produces:
    Bold_Balanced_Wedding_Bible_SAMPLE.xlsx   — pre-filled with sample data
    Bold_Balanced_Wedding_Bible_BLANK.xlsx    — clean customer version

Usage:
    python wedding_planner_generator.py

Sheets:
    1.  Welcome          – Countdown, quick stats, navigation
    2.  Overview         – Key wedding details input
    3.  Budget Dashboard – Auto-totals, pie chart, category breakdown
    4.  Budget Detail    – Itemised budget table (formula-driven)
    5.  Guest List       – RSVP tracker with data validation
    6.  Vendors          – Vendor contacts and payment tracker
    7.  Timeline         – Day-of hour-by-hour schedule
    8.  Checklist        – Master task list with progress tracking
    9.  Bridal Party     – Bridal party details and attire
    10. Seating          – Table seating planner
    11. Registry         – Gift registry tracker
    12. Honeymoon        – Honeymoon itinerary and budget
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.formatting.rule import CellIsRule, DataBarRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.styles.differential import DifferentialStyle
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo

# ─────────────────────────────────────────────────────────────────────
# PALETTE
# ─────────────────────────────────────────────────────────────────────
P = {
    "hot_pink":   "E91E8C",
    "pink":       "F48FB1",
    "light_pink": "FCE4EC",
    "blush":      "FDE8EE",
    "yellow":     "FFE082",
    "gold":       "C9A84C",
    "light_gold": "FFF9C4",
    "black":      "212121",
    "cream":      "FFF8E7",
    "white":      "FFFFFF",
    "rose_gold":  "B76E79",
    "dark_pink":  "AD1457",
    "border":     "E0C0CC",
    "input":      "FFF9C4",
    "formula":    "FCE4EC",
    "green":      "C8E6C9",
    "green_dk":   "388E3C",
    "red_light":  "FFCDD2",
    "red_dk":     "C62828",
    "orange":     "FFE0B2",
}


# ─────────────────────────────────────────────────────────────────────
# STYLE HELPERS
# ─────────────────────────────────────────────────────────────────────

def _fill(c: str) -> PatternFill:
    return PatternFill("solid", fgColor=c)


def _font(size: int = 10, bold: bool = False,
          color: str = "212121", italic: bool = False) -> Font:
    return Font(name="Calibri", size=size, bold=bold,
                color=color, italic=italic)


def _align(h: str = "left", wrap: bool = True) -> Alignment:
    return Alignment(horizontal=h, vertical="center", wrap_text=wrap)


def _border(c: str = "E0C0CC") -> Border:
    s = Side(style="thin", color=c)
    return Border(left=s, right=s, top=s, bottom=s)


def w(ws, row: int, col: int, value=None, bg: str | None = None,
      fg: str = "212121", size: int = 10, bold: bool = False,
      italic: bool = False, align: str = "left", bdr: bool = True,
      fmt: str | None = None):
    c = ws.cell(row=row, column=col, value=value)
    if bg:
        c.fill = _fill(bg)
    c.font = _font(size, bold, fg, italic)
    c.alignment = _align(align)
    if bdr:
        c.border = _border()
    if fmt:
        c.number_format = fmt
    return c


def mg(ws, r1: int, c1: int, r2: int, c2: int, value=None,
       bg: str | None = None, fg: str = "FFFFFF", size: int = 14,
       bold: bool = True, align: str = "center"):
    ws.merge_cells(start_row=r1, start_column=c1,
                   end_row=r2, end_column=c2)
    c = ws.cell(row=r1, column=c1, value=value)
    if bg:
        c.fill = _fill(bg)
    c.font = _font(size, bold, fg)
    c.alignment = _align(align)
    return c


def rh(ws, rows: dict[int, float]) -> None:
    for r, h in rows.items():
        ws.row_dimensions[r].height = h


def cw(ws, cols: dict[str, float]) -> None:
    for col, width in cols.items():
        ws.column_dimensions[col].width = width


def add_table(ws, name: str, ref: str) -> None:
    style = TableStyleInfo(
        name="TableStyleMedium3",
        showFirstColumn=False,
        showLastColumn=False,
        showRowStripes=True,
        showColumnStripes=False,
    )
    t = Table(displayName=name, ref=ref)
    t.tableStyleInfo = style
    ws.add_table(t)


def dropdown(formula1: str, sqref: str,
             title: str = "Select", prompt: str = "Choose an option") -> DataValidation:
    v = DataValidation(type="list", formula1=formula1,
                       allow_blank=True, showDropDown=False)
    v.promptTitle = title
    v.prompt = prompt
    v.sqref = sqref
    return v


def section_header(ws, row: int, c1: int, c2: int,
                   text: str, bg: str | None = None) -> None:
    bg = bg or P["hot_pink"]
    ws.merge_cells(start_row=row, start_column=c1,
                   end_row=row, end_column=c2)
    c = ws.cell(row=row, column=c1, value=f"  {text}")
    c.fill = _fill(bg)
    c.font = _font(11, True, "FFFFFF")
    c.alignment = _align("left")
    ws.row_dimensions[row].height = 30


# ─────────────────────────────────────────────────────────────────────
# SHEET 1 — WELCOME
# ─────────────────────────────────────────────────────────────────────

def build_welcome(ws) -> None:
    ws.sheet_properties.tabColor = P["hot_pink"]
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 24, "C": 20, "D": 20, "E": 20, "F": 20, "G": 2})

    # Top accent strip
    for col in range(1, 8):
        ws.cell(row=1, column=col).fill = _fill(P["hot_pink"])
    rh(ws, {1: 6})

    # Title
    mg(ws, 2, 2, 3, 6,
       "✦  Bold & Balanced Wedding Bible  ✦",
       bg=P["hot_pink"], fg="FFFFFF", size=24, bold=True)
    mg(ws, 4, 2, 4, 6,
       "Modern Luxury Wedding Planning System",
       bg=P["dark_pink"], fg="FFFFFF", size=12, bold=False)
    rh(ws, {2: 50, 3: 8, 4: 28})

    # Yellow accent
    for col in range(1, 8):
        ws.cell(row=5, column=col).fill = _fill(P["yellow"])
    rh(ws, {5: 6})

    # Wedding details input
    section_header(ws, 6, 2, 6, "✦  OUR WEDDING DETAILS  ✦", P["pink"])
    rh(ws, {6: 30})
    input_rows = [
        (7,  "Bride's Name"),
        (8,  "Groom's Name"),
        (9,  "Wedding Date"),
        (10, "Ceremony Venue"),
        (11, "Reception Venue"),
        (12, "Wedding City & State"),
    ]
    for row, label in input_rows:
        w(ws, row, 2, label, bg=P["blush"], fg=P["black"],
          size=10, bold=True, align="right")
        ws.merge_cells(start_row=row, start_column=3,
                       end_row=row, end_column=5)
        inp = ws.cell(row=row, column=3)
        inp.fill = _fill(P["input"])
        inp.font = _font(10)
        inp.alignment = _align()
        inp.border = _border()
        rh(ws, {row: 26})

    ws.cell(row=9, column=3).number_format = "DD MMMM YYYY"

    # Gold spacer
    for col in range(1, 8):
        ws.cell(row=13, column=col).fill = _fill(P["light_gold"])
    rh(ws, {13: 6})

    # Countdown
    section_header(ws, 14, 2, 6, "✦  DAYS UNTIL YOUR BIG DAY  ✦", P["dark_pink"])
    ws.merge_cells(start_row=15, start_column=2, end_row=16, end_column=6)
    cd = ws.cell(row=15, column=2,
                 value='=IFERROR(C9-TODAY(),"✦  Enter your wedding date above  ✦")')
    cd.fill = _fill(P["light_pink"])
    cd.font = _font(40, True, P["hot_pink"])
    cd.alignment = _align("center")
    rh(ws, {14: 30, 15: 60, 16: 8})

    mg(ws, 17, 2, 17, 6,
       "days to go  —  You've got this, bride! 💍",
       bg=P["light_pink"], fg=P["dark_pink"], size=12, bold=False)
    rh(ws, {17: 28})

    for col in range(1, 8):
        ws.cell(row=18, column=col).fill = _fill(P["white"])
    rh(ws, {18: 8})

    # Quick stats
    section_header(ws, 19, 2, 6, "✦  QUICK STATS  ✦", P["gold"])
    rh(ws, {19: 30, 20: 30, 21: 44})

    stats = [
        ("B", "💰 Total Budget",
         "=IFERROR('Budget Detail'!B3,0)", '"$"#,##0', P["light_gold"]),
        ("D", "👥 Guests Invited",
         "=IFERROR(COUNTA('Guest List'!B:B)-1,0)", "0", P["light_pink"]),
        ("F", "✅ Tasks Done",
         '=IFERROR(COUNTIF(Checklist!D:D,"✓ Done"),0)', "0", P["green"]),
    ]
    for col_letter, label, formula, fmt, bg in stats:
        col_num = ord(col_letter) - ord("A") + 1
        lbl = ws.cell(row=20, column=col_num, value=label)
        lbl.fill = _fill(bg)
        lbl.font = _font(10, True, P["black"])
        lbl.alignment = _align("center")
        lbl.border = _border()
        ws.merge_cells(start_row=20, start_column=col_num,
                       end_row=20, end_column=col_num + 1)

        val = ws.cell(row=21, column=col_num, value=formula)
        val.fill = _fill(bg)
        val.font = _font(26, True, P["hot_pink"])
        val.alignment = _align("center")
        val.number_format = fmt
        val.border = _border()
        ws.merge_cells(start_row=21, start_column=col_num,
                       end_row=21, end_column=col_num + 1)

    for col in range(1, 8):
        ws.cell(row=22, column=col).fill = _fill(P["white"])
    rh(ws, {22: 8})

    # Navigation
    section_header(ws, 23, 2, 6, "✦  NAVIGATE YOUR PLANNER  ✦", P["hot_pink"])
    rh(ws, {23: 30})

    nav = [
        (24, "B", "📋  Wedding Overview",    "Overview"),
        (24, "D", "💰  Budget Dashboard",    "Budget Dashboard"),
        (24, "F", None, None),
        (25, "B", "👥  Guest List",          "Guest List"),
        (25, "D", "🤝  Vendor Tracker",      "Vendors"),
        (25, "F", None, None),
        (26, "B", "🕐  Day-of Timeline",     "Timeline"),
        (26, "D", "✅  Master Checklist",    "Checklist"),
        (26, "F", None, None),
        (27, "B", "💐  Bridal Party",        "Bridal Party"),
        (27, "D", "🪑  Seating Chart",       "Seating"),
        (27, "F", None, None),
        (28, "B", "🎁  Gift Registry",       "Registry"),
        (28, "D", "✈️  Honeymoon Planner",   "Honeymoon"),
        (28, "F", None, None),
    ]
    for row, col_letter, label, sheet in nav:
        if label is None:
            continue
        col_num = ord(col_letter) - ord("A") + 1
        c = ws.cell(row=row, column=col_num, value=label)
        c.fill = _fill(P["blush"])
        c.font = Font(name="Calibri", size=10, bold=True,
                      color=P["dark_pink"], underline="single")
        c.alignment = _align("center")
        c.border = _border()
        if sheet:
            c.hyperlink = f"#{sheet}!A1"
        ws.merge_cells(start_row=row, start_column=col_num,
                       end_row=row, end_column=col_num + 1)
        rh(ws, {row: 32})


# ─────────────────────────────────────────────────────────────────────
# SHEET 2 — OVERVIEW
# ─────────────────────────────────────────────────────────────────────

def build_overview(ws) -> None:
    ws.sheet_properties.tabColor = P["pink"]
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 24, "C": 30, "D": 24, "E": 30, "F": 2})

    mg(ws, 1, 2, 2, 5, "✦  WEDDING OVERVIEW  ✦",
       bg=P["hot_pink"], fg="FFFFFF", size=20, bold=True)
    mg(ws, 3, 2, 3, 5, "Your complete wedding details — fill in each section",
       bg=P["pink"], fg="FFFFFF", size=11, bold=False)
    rh(ws, {1: 44, 2: 8, 3: 26, 4: 8})

    left_blocks = [
        (5, "💍 THE COUPLE", [
            "Bride's Full Name", "Groom's Full Name",
            "Wedding Date", "Engagement Date", "Anniversary",
        ]),
        (12, "📍 CEREMONY", [
            "Ceremony Venue", "Address", "City / State",
            "Ceremony Time", "Ceremony End Time",
        ]),
        (19, "🍽️ RECEPTION", [
            "Reception Venue", "Address", "City / State",
            "Reception Start", "Reception End",
        ]),
        (26, "📞 KEY CONTACTS", [
            "Wedding Planner", "Planner Phone",
            "Officiant", "Officiant Phone",
            "Emergency Contact", "Emergency Phone",
        ]),
    ]

    right_blocks = [
        (5, "🎨 WEDDING STYLE", [
            "Wedding Theme", "Wedding Colors",
            "Wedding Season", "Dress Code",
            "Wedding Hashtag",
        ]),
        (12, "📅 IMPORTANT DATES", [
            "Save the Date Sent", "Invitations Sent",
            "RSVP Deadline", "Final Headcount Due",
            "Rehearsal Date",
        ]),
        (19, "💰 BUDGET SNAPSHOT", [
            "Total Budget",
            "Total Estimated",
            "Total Spent",
            "Total Paid",
            "Balance Remaining",
        ]),
        (26, "👰 WEDDING PARTY", [
            "Maid of Honor", "Best Man",
            "Flower Girl(s)", "Ring Bearer",
            "Total Bridesmaids", "Total Groomsmen",
        ]),
    ]

    budget_formulas = {
        "Total Budget":     "='Budget Detail'!B3",
        "Total Estimated":  "='Budget Detail'!B4",
        "Total Spent":      "='Budget Detail'!B5",
        "Total Paid":       "='Budget Detail'!B5",
        "Balance Remaining":"='Budget Detail'!B6",
    }

    for start, header, fields in left_blocks:
        section_header(ws, start, 2, 3, header, P["hot_pink"])
        rh(ws, {start: 30})
        for i, label in enumerate(fields, start=start + 1):
            w(ws, i, 2, label, bg=P["blush"], fg=P["black"],
              size=10, bold=True, align="right")
            c = ws.cell(row=i, column=3)
            c.fill = _fill(P["input"])
            c.font = _font(10)
            c.alignment = _align()
            c.border = _border()
            if label == "Wedding Date" or "Date" in label or "Sent" in label:
                c.number_format = "DD MMM YYYY"
            rh(ws, {i: 25})

    for start, header, fields in right_blocks:
        section_header(ws, start, 4, 5, header, P["dark_pink"])
        rh(ws, {start: 30})
        for i, label in enumerate(fields, start=start + 1):
            w(ws, i, 4, label, bg=P["light_pink"], fg=P["black"],
              size=10, bold=True, align="right")
            formula = budget_formulas.get(label)
            c = ws.cell(row=i, column=5,
                        value=formula if formula else None)
            c.fill = _fill(P["formula"] if formula else P["input"])
            c.font = _font(10)
            c.alignment = _align()
            c.border = _border()
            if formula:
                c.number_format = '"$"#,##0.00'
            rh(ws, {i: 25})


# ─────────────────────────────────────────────────────────────────────
# SHEET 3 — BUDGET DASHBOARD
# ─────────────────────────────────────────────────────────────────────

def build_budget_dashboard(ws) -> None:
    ws.sheet_properties.tabColor = P["gold"]
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 26, "C": 18, "D": 18, "E": 18, "F": 18, "G": 2})

    mg(ws, 1, 2, 2, 6, "✦  BUDGET DASHBOARD  ✦",
       bg=P["hot_pink"], fg="FFFFFF", size=20, bold=True)
    mg(ws, 3, 2, 3, 6,
       "Auto-updating totals and category breakdown — no manual entry needed",
       bg=P["gold"], fg="FFFFFF", size=11, bold=False)
    rh(ws, {1: 44, 2: 8, 3: 26, 4: 10})

    # ── Summary KPIs ─────────────────────────────────────────────
    section_header(ws, 5, 2, 6, "✦  BUDGET SUMMARY  ✦", P["dark_pink"])
    rh(ws, {5: 30})

    kpis = [
        ("B", "💰 Total Budget",    "=B8",   '"$"#,##0.00', P["light_gold"]),
        ("C", "📊 Estimated Total", "=C8",   '"$"#,##0.00', P["blush"]),
        ("D", "💳 Actual Spent",    "=D8",   '"$"#,##0.00', P["light_pink"]),
        ("E", "✅ Total Paid",      "=E8",   '"$"#,##0.00', P["green"]),
        ("F", "⚠️ Balance Due",     "=F8",   '"$"#,##0.00', P["orange"]),
    ]

    for col_letter, label, formula, fmt, bg in kpis:
        col_num = ord(col_letter) - ord("A") + 1
        lbl = ws.cell(row=6, column=col_num, value=label)
        lbl.fill = _fill(bg)
        lbl.font = _font(10, True, P["black"])
        lbl.alignment = _align("center")
        lbl.border = _border()

        val = ws.cell(row=7, column=col_num, value=formula)
        val.fill = _fill(bg)
        val.font = _font(18, True, P["dark_pink"])
        val.alignment = _align("center")
        val.number_format = fmt
        val.border = _border()

    rh(ws, {6: 28, 7: 44})

    # ── Category summary table (auto-calculated) ─────────────────
    # Row 8 = TOTALS row (referenced by KPIs above)
    # Rows 9-25 = per-category breakdown

    for col in range(1, 8):
        ws.cell(row=8, column=col).fill = _fill(P["white"])
    rh(ws, {8: 8})

    section_header(ws, 9, 2, 6, "✦  BUDGET BY CATEGORY  ✦", P["hot_pink"])
    rh(ws, {9: 30})

    cat_headers = ["Category", "Budget", "Estimated", "Actual Spent",
                   "Paid", "Balance Due"]
    for i, h in enumerate(cat_headers, start=2):
        w(ws, 10, i, h, bg=P["dark_pink"], fg="FFFFFF",
          size=10, bold=True, align="center")
    rh(ws, {10: 28})

    categories = [
        "Venue", "Catering", "Photography", "Videography",
        "Florals", "Music / DJ", "Attire & Beauty", "Transportation",
        "Stationery", "Rings", "Honeymoon", "Gifts & Favors",
        "Cake & Desserts", "Officiant", "Lighting & Decor", "Other",
    ]

    for i, cat in enumerate(categories, start=11):
        row_bg = P["blush"] if i % 2 == 0 else P["cream"]
        w(ws, i, 2, cat, bg=row_bg, fg=P["black"], size=10, bold=True)
        # SUMIFS pulling from Budget Detail sheet
        budget_f  = f"=IFERROR(SUMIF('Budget Detail'!A:A,B{i},'Budget Detail'!C:C),0)"
        est_f     = f"=IFERROR(SUMIF('Budget Detail'!A:A,B{i},'Budget Detail'!D:D),0)"
        actual_f  = f"=IFERROR(SUMIF('Budget Detail'!A:A,B{i},'Budget Detail'!E:E),0)"
        paid_f    = f"=IFERROR(SUMIF('Budget Detail'!A:A,B{i},'Budget Detail'!F:F),0)"
        balance_f = f"=IFERROR(D{i}-E{i},0)"
        for col, formula, fmt in [
            (3, budget_f,  '"$"#,##0.00'),
            (4, est_f,     '"$"#,##0.00'),
            (5, actual_f,  '"$"#,##0.00'),
            (6, paid_f,    '"$"#,##0.00'),
            (7, balance_f, '"$"#,##0.00'),
        ]:
            c = ws.cell(row=i, column=col, value=formula)
            c.fill = _fill(P["formula"])
            c.font = _font(10)
            c.alignment = _align("center")
            c.border = _border()
            c.number_format = fmt
        rh(ws, {i: 22})

    last_cat_row = 10 + len(categories)

    # Totals row
    totals_row = last_cat_row + 1
    w(ws, totals_row, 2, "TOTAL", bg=P["hot_pink"], fg="FFFFFF",
      size=11, bold=True, align="center")
    for col in range(3, 8):
        c = ws.cell(row=totals_row, column=col,
                    value=f"=SUM({get_column_letter(col)}11:{get_column_letter(col)}{last_cat_row})")
        c.fill = _fill(P["hot_pink"])
        c.font = _font(11, True, "FFFFFF")
        c.alignment = _align("center")
        c.border = _border()
        c.number_format = '"$"#,##0.00'
    rh(ws, {totals_row: 28})

    # Wire up the KPI summary row 8 that the KPIs at top reference
    ws.cell(row=8, column=2).value = f"=C{totals_row}"   # Budget (uses Estimated column)
    ws.cell(row=8, column=3).value = f"=D{totals_row}"   # Estimated
    ws.cell(row=8, column=4).value = f"=E{totals_row}"   # Actual
    ws.cell(row=8, column=5).value = f"=F{totals_row}"   # Paid
    ws.cell(row=8, column=6).value = f"=G{totals_row}"   # Balance

    # ── Pie Chart ────────────────────────────────────────────────
    chart = PieChart()
    chart.title = "Budget by Category"
    chart.style = 10
    chart.width = 16
    chart.height = 14

    labels = Reference(ws,
                       min_col=2, min_row=11,
                       max_col=2, max_row=last_cat_row)
    data   = Reference(ws,
                       min_col=3, min_row=10,
                       max_col=3, max_row=last_cat_row)
    chart.add_data(data, titles_from_data=True)
    chart.set_categories(labels)
    chart.dataLabels = None

    ws.add_chart(chart, f"B{totals_row + 2}")


# ─────────────────────────────────────────────────────────────────────
# SHEET 4 — BUDGET DETAIL
# ─────────────────────────────────────────────────────────────────────

def build_budget_detail(ws, sample: bool = True) -> None:
    ws.sheet_properties.tabColor = P["yellow"]
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 20, "C": 28, "D": 14, "E": 14, "F": 14, "G": 14,
            "H": 16, "I": 28})

    mg(ws, 1, 2, 2, 9, "✦  BUDGET DETAIL  ✦",
       bg=P["hot_pink"], fg="FFFFFF", size=20, bold=True)
    mg(ws, 3, 2, 3, 9,
       "Add every expense below — all totals update automatically",
       bg=P["yellow"], fg=P["black"], size=11, bold=False)
    rh(ws, {1: 44, 2: 8, 3: 26, 4: 10})

    # Summary box
    for row, label, formula, fmt in [
        (5, "Total Budget",     None,             '"$"#,##0.00'),
        (6, "Total Estimated",  "=SUM(E9:E2000)", '"$"#,##0.00'),
        (7, "Total Paid",       "=SUM(F9:F2000)", '"$"#,##0.00'),
        (8, "Balance Remaining","=B6-B7",         '"$"#,##0.00'),
    ]:
        w(ws, row, 2, label, bg=P["blush"], fg=P["black"],
          size=10, bold=True, align="right")
        c = ws.cell(row=row, column=3,
                    value=formula if formula else None)
        c.fill = _fill(P["formula"] if formula else P["input"])
        c.font = _font(12, True, P["dark_pink"])
        c.alignment = _align("center")
        c.border = _border()
        c.number_format = fmt
        rh(ws, {row: 24})

    # Column note
    w(ws, 5, 5, "← Enter your total budget in C5",
      bg=P["light_gold"], fg=P["gold"], size=9, italic=True, bdr=False)

    # Table headers
    headers = ["Category", "Item / Description", "Budget Allocated",
               "Estimated Cost", "Actual / Paid", "Balance",
               "Status", "Notes"]
    for i, h in enumerate(headers, start=2):
        w(ws, 9, i, h, bg=P["dark_pink"], fg="FFFFFF",
          size=10, bold=True, align="center")
    rh(ws, {9: 30})

    categories = [
        "Venue", "Catering", "Photography", "Videography",
        "Florals", "Music / DJ", "Attire & Beauty", "Transportation",
        "Stationery", "Rings", "Honeymoon", "Gifts & Favors",
        "Cake & Desserts", "Officiant", "Lighting & Decor", "Other",
    ]

    sample_rows = [
        ("Venue",            "Ceremony Venue Hire",         3500, 3500,  1750),
        ("Venue",            "Reception Hall Hire",         5000, 5200,  5200),
        ("Catering",         "Dinner Service (per head)",   8000, 8500,  4250),
        ("Catering",         "Wedding Cake",                600,  650,   650),
        ("Photography",      "Wedding Photographer",        3000, 2800,  2800),
        ("Photography",      "Photo Booth Rental",          500,  500,   250),
        ("Florals",          "Bridal Bouquet",              350,  375,   375),
        ("Florals",          "Ceremony Arrangements",       800,  820,   820),
        ("Florals",          "Reception Centrepieces",      1200, 1250,  625),
        ("Music / DJ",       "DJ Service",                  1800, 1800,  900),
        ("Attire & Beauty",  "Wedding Dress",               2500, 2800,  2800),
        ("Attire & Beauty",  "Bridesmaid Dresses (x4)",     1200, 1100,  1100),
        ("Attire & Beauty",  "Groom's Suit",                800,  850,   850),
        ("Transportation",   "Bridal Car / Limo",           600,  600,   300),
        ("Stationery",       "Invitations & Envelopes",     400,  380,   380),
        ("Rings",            "Wedding Bands (pair)",        1500, 1600,  1600),
        ("Honeymoon",        "Flights",                     2000, 2100,  2100),
        ("Honeymoon",        "Hotel / Accommodation",       3000, 3200,  1600),
    ]

    status_options = (
        '"Pending,Contracted,Deposit Paid,Fully Paid,Cancelled"'
    )
    cat_formula = f'"{",".join(categories)}"'

    start_data = 10
    n_rows = len(sample_rows) if sample else 50

    for i in range(n_rows):
        row = start_data + i
        bg = P["blush"] if i % 2 == 0 else P["cream"]

        if sample and i < len(sample_rows):
            cat, item, budget_alloc, estimated, paid = sample_rows[i]
            balance_f = f"=IFERROR(E{row}-F{row},0)"
            for col, val, fmt in [
                (2, cat,         "@"),
                (3, item,        "@"),
                (4, budget_alloc,'"$"#,##0.00'),
                (5, estimated,   '"$"#,##0.00'),
                (6, paid,        '"$"#,##0.00'),
                (7, balance_f,   '"$"#,##0.00'),
                (8, "Deposit Paid", "@"),
                (9, "",          "@"),
            ]:
                c = ws.cell(row=row, column=col, value=val)
                c.fill = _fill(bg)
                c.font = _font(10)
                c.alignment = _align("left" if col in (2, 3, 9) else "center")
                c.border = _border()
                c.number_format = fmt
        else:
            balance_f = f"=IFERROR(E{row}-F{row},0)"
            for col, fmt in [(2, "@"), (3, "@"),
                             (4, '"$"#,##0.00'), (5, '"$"#,##0.00'),
                             (6, '"$"#,##0.00'), (7, '"$"#,##0.00'),
                             (8, "@"), (9, "@")]:
                c = ws.cell(row=row, column=col,
                            value=balance_f if col == 7 else None)
                c.fill = _fill(P["input"] if col not in (7,) else P["formula"])
                c.font = _font(10)
                c.alignment = _align("center")
                c.border = _border()
                c.number_format = fmt
        rh(ws, {row: 22})

    last_row = start_data + n_rows - 1
    add_table(ws, "tblBudget", f"B9:I{last_row}")

    # Data validation
    ws.add_data_validation(dropdown(cat_formula, f"B{start_data}:B{last_row}",
                                    "Category", "Select a budget category"))
    ws.add_data_validation(dropdown(status_options, f"H{start_data}:H{last_row}",
                                    "Status", "Select payment status"))

    # Conditional formatting — colour the Status column
    for rule_value, bg, font_col in [
        ("Fully Paid",    P["green"],      P["green_dk"]),
        ("Deposit Paid",  P["yellow"],     P["black"]),
        ("Pending",       P["red_light"],  P["red_dk"]),
        ("Cancelled",     P["light_pink"], P["dark_pink"]),
    ]:
        diff = DifferentialStyle(
            fill=_fill(bg),
            font=_font(10, False, font_col),
        )
        from openpyxl.formatting.rule import Rule
        rule = Rule(type="containsText", operator="containsText",
                    text=rule_value, dxf=diff)
        rule.formula = [f'NOT(ISERROR(SEARCH("{rule_value}",H{start_data})))']
        ws.conditional_formatting.add(
            f"H{start_data}:H{last_row}", rule)


# ─────────────────────────────────────────────────────────────────────
# SHEET 5 — GUEST LIST
# ─────────────────────────────────────────────────────────────────────

def build_guest_list(ws, sample: bool = True) -> None:
    ws.sheet_properties.tabColor = P["pink"]
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 5,  "C": 16, "D": 16, "E": 16, "F": 8,  "G": 8,
            "H": 12, "I": 16, "J": 10, "K": 8,  "L": 22, "M": 14, "N": 8,
            "O": 8,  "P": 20, "Q": 2})

    mg(ws, 1, 2, 2, 16, "✦  GUEST LIST  ✦",
       bg=P["hot_pink"], fg="FFFFFF", size=20, bold=True)
    rh(ws, {1: 44, 2: 8, 3: 10})

    # Stats row
    stats = [
        ("B", "Total Invited",  '=IFERROR(COUNTA(C8:C2000),0)',            P["light_pink"]),
        ("D", "RSVP Yes",       '=IFERROR(COUNTIF(H8:H2000,"Yes"),0)',      P["green"]),
        ("F", "RSVP No",        '=IFERROR(COUNTIF(H8:H2000,"No"),0)',       P["red_light"]),
        ("H", "Pending",        '=IFERROR(COUNTIF(H8:H2000,"Pending"),0)',  P["yellow"]),
        ("J", "Total Adults",   '=IFERROR(SUM(F8:F2000),0)',                P["blush"]),
        ("L", "Total Children", '=IFERROR(SUM(G8:G2000),0)',                P["blush"]),
    ]
    rh(ws, {4: 28, 5: 36})
    for col_letter, label, formula, bg in stats:
        col_num = ord(col_letter) - ord("A") + 1
        lbl = ws.cell(row=4, column=col_num, value=label)
        lbl.fill = _fill(bg)
        lbl.font = _font(9, True, P["black"])
        lbl.alignment = _align("center")
        lbl.border = _border()
        ws.merge_cells(start_row=4, start_column=col_num,
                       end_row=4, end_column=col_num + 1)
        val = ws.cell(row=5, column=col_num, value=formula)
        val.fill = _fill(bg)
        val.font = _font(20, True, P["hot_pink"])
        val.alignment = _align("center")
        val.border = _border()
        ws.merge_cells(start_row=5, start_column=col_num,
                       end_row=5, end_column=col_num + 1)

    for col in range(1, 17):
        ws.cell(row=6, column=col).fill = _fill(P["white"])
    rh(ws, {6: 8})

    headers = ["#", "First Name", "Last Name", "Group", "Email",
               "Adults", "Children", "RSVP", "Meal Choice",
               "Table #", "+1?", "Phone / Notes",
               "Gift Received?", "Thank You?"]
    for i, h in enumerate(headers, start=2):
        w(ws, 7, i, h, bg=P["dark_pink"], fg="FFFFFF",
          size=10, bold=True, align="center")
    rh(ws, {7: 30})

    sample_guests = [
        ("Sarah",   "Johnson",  "Bride's Side",  "sarah@email.com",  2, 0, "Yes",     "Chicken",    "1",  "No"),
        ("Michael", "Williams", "Groom's Side",  "mike@email.com",   2, 2, "Yes",     "Beef",       "2",  "No"),
        ("Emma",    "Brown",    "Bride's Side",  "emma@email.com",   1, 0, "Yes",     "Vegetarian", "1",  "Yes"),
        ("James",   "Davis",    "Groom's Side",  "james@email.com",  2, 0, "No",      "",           "",   "No"),
        ("Olivia",  "Wilson",   "Bride's Side",  "liv@email.com",    2, 1, "Pending", "",           "",   "No"),
        ("Liam",    "Taylor",   "Both",          "liam@email.com",   2, 0, "Yes",     "Fish",       "3",  "No"),
        ("Sophia",  "Anderson", "Groom's Side",  "soph@email.com",   1, 0, "Yes",     "Chicken",    "3",  "No"),
        ("Noah",    "Thomas",   "Bride's Side",  "noah@email.com",   2, 2, "Pending", "",           "",   "No"),
    ]

    rsvp_dv    = dropdown('"Yes,No,Pending"',         "I8:I2000", "RSVP",  "Select RSVP status")
    meal_dv    = dropdown('"Chicken,Beef,Fish,Vegetarian,Vegan,Kids Meal"',
                          "J8:J2000", "Meal", "Select meal choice")
    group_dv   = dropdown("\"Bride's Side,Groom's Side,Both,Other\"",
                          "F8:F2000", "Group", "Select guest group")
    plusone_dv = dropdown('"Yes,No"', "L8:L2000", "+1?", "Bringing a plus one?")
    gift_dv    = dropdown('"Yes,No"', "N8:N2000", "Gift", "Gift received?")
    thanks_dv  = dropdown('"Yes,No"', "O8:O2000", "Thanks", "Thank you sent?")
    for dv_ in [rsvp_dv, meal_dv, group_dv, plusone_dv, gift_dv, thanks_dv]:
        ws.add_data_validation(dv_)

    n_rows = len(sample_guests) if sample else 100
    for i in range(n_rows):
        row = 8 + i
        bg = P["blush"] if i % 2 == 0 else P["cream"]
        w(ws, row, 2, str(i + 1), bg=bg, fg=P["black"], size=9, align="center")
        if sample and i < len(sample_guests):
            fn, ln, grp, email, adults, children, rsvp, meal, table, plusone = sample_guests[i]
            for col, val in [(3, fn), (4, ln), (5, grp), (6, email),
                             (7, adults), (8, children), (9, rsvp),
                             (10, meal), (11, table), (12, plusone),
                             (13, ""), (14, "No"), (15, "No")]:
                c = ws.cell(row=row, column=col, value=val)
                c.fill = _fill(bg)
                c.font = _font(10)
                c.alignment = _align("center")
                c.border = _border()
        else:
            for col in range(3, 16):
                c = ws.cell(row=row, column=col)
                c.fill = _fill(P["input"])
                c.font = _font(10)
                c.alignment = _align("center")
                c.border = _border()
        rh(ws, {row: 22})

    last_row = 7 + n_rows
    add_table(ws, "tblGuests", f"B7:O{last_row}")

    # Conditional formatting — RSVP column
    rsvp_col = "I"
    for val, bg, fc in [("Yes", P["green"], P["green_dk"]),
                         ("No",  P["red_light"], P["red_dk"]),
                         ("Pending", P["yellow"], P["black"])]:
        diff = DifferentialStyle(fill=_fill(bg), font=_font(10, False, fc))
        from openpyxl.formatting.rule import Rule
        rule = Rule(type="containsText", operator="containsText",
                    text=val, dxf=diff)
        rule.formula = [f'NOT(ISERROR(SEARCH("{val}",{rsvp_col}8)))']
        ws.conditional_formatting.add(f"{rsvp_col}8:{rsvp_col}{last_row}", rule)


# ─────────────────────────────────────────────────────────────────────
# SHEET 6 — VENDORS
# ─────────────────────────────────────────────────────────────────────

def build_vendors(ws, sample: bool = True) -> None:
    ws.sheet_properties.tabColor = P["rose_gold"]
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 18, "C": 22, "D": 16, "E": 20, "F": 16,
            "G": 12, "H": 12, "I": 12, "J": 14, "K": 12, "L": 22, "M": 2})

    mg(ws, 1, 2, 2, 12, "✦  VENDOR TRACKER  ✦",
       bg=P["hot_pink"], fg="FFFFFF", size=20, bold=True)
    mg(ws, 3, 2, 3, 12,
       "Track every vendor, contract, deposit, and balance in one place",
       bg=P["rose_gold"], fg="FFFFFF", size=11, bold=False)
    rh(ws, {1: 44, 2: 8, 3: 26, 4: 10})

    headers = ["Category", "Vendor / Company", "Contact Name",
               "Phone", "Email", "Website",
               "Contract?", "Deposit Paid", "Balance Due",
               "Total Cost", "Status", "Notes"]
    for i, h in enumerate(headers, start=2):
        w(ws, 5, i, h, bg=P["dark_pink"], fg="FFFFFF",
          size=10, bold=True, align="center")
    rh(ws, {5: 30})

    sample_vendors = [
        ("Venue",         "The Grand Ballroom",   "Maria Smith",  "555-0101", "info@grandbr.com",     "grandbr.com",       "Yes", 2500,  2500,  5000,  "Fully Paid"),
        ("Catering",      "Delish Catering Co.",  "Chef Tony",    "555-0102", "tony@delish.com",      "delish.com",        "Yes", 4000,  4000,  8000,  "Deposit Paid"),
        ("Photography",   "Moments by Lily",      "Lily Chen",    "555-0103", "lily@moments.com",     "moments.com",       "Yes", 1500,  1300,  2800,  "Fully Paid"),
        ("Florals",       "Bloom & Blossom",      "Rose Kim",     "555-0104", "rose@bloom.com",       "bloom.com",         "Yes", 500,   1750,  2250,  "Deposit Paid"),
        ("Music / DJ",    "DJ Max Entertainment", "Max Power",    "555-0105", "max@djmax.com",        "djmax.com",         "Yes", 900,   900,   1800,  "Deposit Paid"),
        ("Cake",          "Sugar & Dreams Bakery","Patty Cakes",  "555-0106", "patty@sugar.com",      "sugardreams.com",   "No",  0,     650,   650,   "Contracted"),
        ("Transportation","Elite Limo Service",   "James Driver", "555-0107", "james@elitelimo.com",  "elitelimo.com",     "Yes", 300,   300,   600,   "Deposit Paid"),
        ("Hair & Makeup", "Glam Squad Studio",    "Bella Noir",   "555-0108", "bella@glam.com",       "glamsquad.com",     "Yes", 400,   400,   800,   "Fully Paid"),
    ]

    status_dv = dropdown(
        '"Researching,Contacted,Contracted,Deposit Paid,Fully Paid,Cancelled"',
        "L6:L2000", "Status", "Select vendor status")
    cat_dv = dropdown(
        '"Venue,Catering,Photography,Videography,Florals,Music / DJ,'
        'Cake,Transportation,Hair & Makeup,Officiant,Stationery,Rings,Other"',
        "B6:B2000", "Category", "Select vendor category")
    contract_dv = dropdown('"Yes,No,Pending"', "H6:H2000",
                           "Contract", "Contract signed?")
    ws.add_data_validation(status_dv)
    ws.add_data_validation(cat_dv)
    ws.add_data_validation(contract_dv)

    n_rows = len(sample_vendors) if sample else 30
    for i in range(n_rows):
        row = 6 + i
        bg = P["blush"] if i % 2 == 0 else P["cream"]
        if sample and i < len(sample_vendors):
            cat, company, contact, phone, email, web, contract, deposit, balance, total, status = sample_vendors[i]
            vals = [cat, company, contact, phone, email, web,
                    contract, deposit, balance, total, status, ""]
            for col, val in enumerate(vals, start=2):
                fmt = '"$"#,##0.00' if col in (9, 10, 11) else "@"
                w(ws, row, col, val, bg=bg, fmt=fmt,
                  align="center" if col not in (3, 4, 7) else "left")
        else:
            for col in range(2, 14):
                c = ws.cell(row=row, column=col)
                c.fill = _fill(P["input"])
                c.font = _font(10)
                c.alignment = _align("center")
                c.border = _border()
                if col in (9, 10, 11):
                    c.number_format = '"$"#,##0.00'
        rh(ws, {row: 22})

    last_row = 5 + n_rows
    add_table(ws, "tblVendors", f"B5:M{last_row}")


# ─────────────────────────────────────────────────────────────────────
# SHEET 7 — DAY-OF TIMELINE
# ─────────────────────────────────────────────────────────────────────

def build_timeline(ws, sample: bool = True) -> None:
    ws.sheet_properties.tabColor = P["dark_pink"]
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 12, "C": 30, "D": 22, "E": 22, "F": 18, "G": 24, "H": 2})

    mg(ws, 1, 2, 2, 7, "✦  DAY-OF TIMELINE  ✦",
       bg=P["hot_pink"], fg="FFFFFF", size=20, bold=True)
    mg(ws, 3, 2, 3, 7,
       "Your complete minute-by-minute wedding day schedule",
       bg=P["dark_pink"], fg="FFFFFF", size=11, bold=False)
    rh(ws, {1: 44, 2: 8, 3: 26, 4: 10})

    headers = ["Time", "Event / Activity", "Location",
               "Responsible Person", "Vendor / Contact", "Notes"]
    for i, h in enumerate(headers, start=2):
        w(ws, 5, i, h, bg=P["dark_pink"], fg="FFFFFF",
          size=10, bold=True, align="center")
    rh(ws, {5: 30})

    sample_timeline = [
        ("6:00 AM",  "Bride & Bridesmaids Wake Up",      "Bridal Suite",           "Bride",             "Glam Squad",         "Breakfast delivered"),
        ("7:00 AM",  "Hair & Makeup Begins — Bridesmaids","Bridal Suite",           "Bella Noir",        "Glam Squad Studio",  "Start with bridesmaids"),
        ("9:00 AM",  "Bride's Hair & Makeup",             "Bridal Suite",           "Bella Noir",        "Glam Squad Studio",  ""),
        ("10:30 AM", "Photographer Arrives",              "Bridal Suite",           "Lily Chen",         "Moments by Lily",    "Getting-ready shots"),
        ("11:00 AM", "Bride Gets Dressed",                "Bridal Suite",           "Maid of Honor",     "",                   "Mom helps with veil"),
        ("11:30 AM", "First Look Photos",                 "Garden / Courtyard",     "Lily Chen",         "Moments by Lily",    "Private moment"),
        ("12:00 PM", "Wedding Party Photos",              "Venue Grounds",          "Lily Chen",         "Moments by Lily",    ""),
        ("1:30 PM",  "Guests Begin Arriving",             "Ceremony Venue",         "Ushers",            "",                   "Program handout"),
        ("2:00 PM",  "CEREMONY BEGINS",                   "Ceremony Venue",         "Officiant",         "Rev. John Smith",    "✦ BIG MOMENT ✦"),
        ("2:45 PM",  "Ceremony Ends — Recessional",       "Ceremony Venue",         "DJ Max",            "DJ Max Entertainment","Cue recessional song"),
        ("3:00 PM",  "Cocktail Hour",                     "Garden / Foyer",         "Catering Team",     "Delish Catering",    "Canapés & drinks"),
        ("4:00 PM",  "Couple Portraits",                  "Venue Grounds",          "Lily Chen",         "Moments by Lily",    "Golden hour shots"),
        ("5:00 PM",  "Reception Doors Open",              "Grand Ballroom",         "Venue Coordinator", "The Grand Ballroom", ""),
        ("5:30 PM",  "Grand Entrance",                    "Grand Ballroom",         "DJ Max",            "DJ Max Entertainment","Announce wedding party"),
        ("5:45 PM",  "First Dance",                       "Dance Floor",            "DJ Max",            "DJ Max Entertainment","✦ Special Moment ✦"),
        ("6:00 PM",  "Welcome Speech & Dinner Service",   "Grand Ballroom",         "Best Man",          "Delish Catering",    ""),
        ("7:30 PM",  "Speeches & Toasts",                 "Grand Ballroom",         "Best Man / MOH",    "",                   "Keep to 5 min each"),
        ("8:00 PM",  "Cake Cutting",                      "Cake Table",             "Couple",            "Sugar & Dreams",     ""),
        ("8:30 PM",  "Dancing Begins",                    "Dance Floor",            "DJ Max",            "DJ Max Entertainment","Open dance floor"),
        ("10:30 PM", "Bouquet Toss",                      "Dance Floor",            "Bride",             "",                   ""),
        ("11:00 PM", "Last Dance",                        "Dance Floor",            "DJ Max",            "DJ Max Entertainment",""),
        ("11:30 PM", "Farewell / Sparkler Exit",          "Venue Entrance",         "All Guests",        "",                   "Photographer on standby"),
        ("12:00 AM", "Venue Vacated",                     "The Grand Ballroom",     "Venue Coordinator", "",                   "Collect all belongings"),
    ]

    n_rows = len(sample_timeline) if sample else 40
    for i in range(n_rows):
        row = 6 + i
        bg = P["blush"] if i % 2 == 0 else P["cream"]
        if sample and i < len(sample_timeline):
            time_, event, location, responsible, vendor, notes = sample_timeline[i]
            highlight = P["light_gold"] if "✦" in event else bg
            for col, val in enumerate([time_, event, location, responsible, vendor, notes],
                                      start=2):
                w(ws, row, col, val, bg=highlight, align="center" if col == 2 else "left")
        else:
            for col in range(2, 8):
                c = ws.cell(row=row, column=col)
                c.fill = _fill(P["input"])
                c.font = _font(10)
                c.alignment = _align()
                c.border = _border()
        rh(ws, {row: 24})

    last_row = 5 + n_rows
    add_table(ws, "tblTimeline", f"B5:G{last_row}")


# ─────────────────────────────────────────────────────────────────────
# SHEET 8 — CHECKLIST
# ─────────────────────────────────────────────────────────────────────

def build_checklist(ws, sample: bool = True) -> None:
    ws.sheet_properties.tabColor = P["yellow"]
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 22, "C": 38, "D": 16, "E": 18, "F": 16, "G": 16, "H": 16, "I": 2})

    mg(ws, 1, 2, 2, 8, "✦  MASTER WEDDING CHECKLIST  ✦",
       bg=P["hot_pink"], fg="FFFFFF", size=20, bold=True)
    rh(ws, {1: 44, 2: 8})

    # Progress stats — B:C, D:E, F:G, H:I (non-overlapping pairs)
    rh(ws, {3: 28, 4: 40})
    stats = [
        ("B", "Total Tasks",  "=IFERROR(COUNTA(C7:C2000),0)",                P["blush"]),
        ("D", "Completed",    '=IFERROR(COUNTIF(D7:D2000,"✓ Done"),0)',       P["green"]),
        ("F", "In Progress",  '=IFERROR(COUNTIF(D7:D2000,"In Progress"),0)',  P["yellow"]),
        ("H", "% Complete",   '=IFERROR(D4/B4,0)',                            P["light_gold"]),
    ]
    for col_letter, label, formula, bg in stats:
        col_num = ord(col_letter) - ord("A") + 1
        lbl = ws.cell(row=3, column=col_num, value=label)
        lbl.fill = _fill(bg)
        lbl.font = _font(10, True, P["black"])
        lbl.alignment = _align("center")
        lbl.border = _border()
        val = ws.cell(row=4, column=col_num, value=formula)
        val.fill = _fill(bg)
        val.font = _font(22, True, P["hot_pink"])
        val.alignment = _align("center")
        val.number_format = "0%" if "%" in label else "0"
        val.border = _border()
        ws.merge_cells(start_row=3, start_column=col_num,
                       end_row=3, end_column=col_num + 1)
        ws.merge_cells(start_row=4, start_column=col_num,
                       end_row=4, end_column=col_num + 1)

    for col in range(1, 10):
        ws.cell(row=5, column=col).fill = _fill(P["white"])
    rh(ws, {5: 8})

    headers = ["Timeframe", "Task", "Status", "Due Date", "Assigned To", "Notes"]
    for i, h in enumerate(headers, start=2):
        w(ws, 6, i, h, bg=P["dark_pink"], fg="FFFFFF",
          size=10, bold=True, align="center")
    rh(ws, {6: 30})
    cw(ws, {"B": 22, "C": 38, "D": 16, "E": 18, "F": 18, "G": 22})

    tasks = [
        ("12+ Months Out", "Set your wedding budget",                          "✓ Done",     ""),
        ("12+ Months Out", "Create your guest list",                           "✓ Done",     ""),
        ("12+ Months Out", "Choose your wedding date",                         "✓ Done",     ""),
        ("12+ Months Out", "Book ceremony and reception venues",                "✓ Done",     ""),
        ("12+ Months Out", "Hire a wedding planner (optional)",                 "✓ Done",     ""),
        ("9–12 Months",    "Book photographer and videographer",                "✓ Done",     ""),
        ("9–12 Months",    "Book caterer",                                      "✓ Done",     ""),
        ("9–12 Months",    "Book florist",                                      "✓ Done",     ""),
        ("9–12 Months",    "Book DJ / live band",                               "✓ Done",     ""),
        ("9–12 Months",    "Send save-the-dates",                               "✓ Done",     ""),
        ("9–12 Months",    "Start dress shopping",                              "✓ Done",     ""),
        ("6–9 Months",     "Order wedding dress",                               "✓ Done",     ""),
        ("6–9 Months",     "Choose bridesmaids dresses",                        "In Progress",""),
        ("6–9 Months",     "Book hair & makeup artist",                         "✓ Done",     ""),
        ("6–9 Months",     "Plan honeymoon",                                    "In Progress",""),
        ("6–9 Months",     "Book honeymoon travel",                             "To Do",      ""),
        ("4–6 Months",     "Send wedding invitations",                          "To Do",      ""),
        ("4–6 Months",     "Order wedding cake",                                "In Progress",""),
        ("4–6 Months",     "Plan rehearsal dinner",                             "To Do",      ""),
        ("4–6 Months",     "Buy wedding rings",                                 "✓ Done",     ""),
        ("4–6 Months",     "Plan ceremony details with officiant",               "To Do",      ""),
        ("2–4 Months",     "Chase RSVPs",                                       "To Do",      ""),
        ("2–4 Months",     "Finalise menu with caterer",                        "To Do",      ""),
        ("2–4 Months",     "Arrange transportation",                            "To Do",      ""),
        ("2–4 Months",     "Create seating plan",                               "To Do",      ""),
        ("2–4 Months",     "Write vows",                                        "To Do",      ""),
        ("1–2 Months",     "Final dress fitting",                               "To Do",      ""),
        ("1–2 Months",     "Confirm all vendors",                               "To Do",      ""),
        ("1–2 Months",     "Prepare payments / tips for vendors",               "To Do",      ""),
        ("1–2 Months",     "Create day-of timeline and distribute",             "To Do",      ""),
        ("1 Week Out",     "Final headcount to caterer",                        "To Do",      ""),
        ("1 Week Out",     "Prepare wedding day emergency kit",                 "To Do",      ""),
        ("1 Week Out",     "Delegate roles to bridal party",                    "To Do",      ""),
        ("Wedding Day",    "Wake up early — eat breakfast! 🥐",                 "To Do",      ""),
        ("Wedding Day",    "Relax and enjoy every moment 💍",                   "To Do",      ""),
        ("After Wedding",  "Send thank-you cards",                              "To Do",      ""),
        ("After Wedding",  "Return any rentals",                                "To Do",      ""),
        ("After Wedding",  "Change name (if applicable)",                       "To Do",      ""),
    ]

    status_dv = dropdown(
        '"To Do,In Progress,✓ Done,On Hold,Delegated,Cancelled"',
        "D7:D2000", "Status", "Select task status")
    ws.add_data_validation(status_dv)

    n_rows = len(tasks) if sample else 60
    for i in range(n_rows):
        row = 7 + i
        bg = P["blush"] if i % 2 == 0 else P["cream"]
        if sample and i < len(tasks):
            timeframe, task, status, due = tasks[i]
            for col, val in [(2, timeframe), (3, task), (4, status),
                             (5, due), (6, ""), (7, "")]:
                c = ws.cell(row=row, column=col, value=val)
                c.fill = _fill(bg)
                c.font = _font(10)
                c.alignment = _align("left" if col == 3 else "center")
                c.border = _border()
                if col == 5:
                    c.number_format = "DD MMM YYYY"
        else:
            for col in range(2, 8):
                c = ws.cell(row=row, column=col)
                c.fill = _fill(P["input"])
                c.font = _font(10)
                c.alignment = _align("center")
                c.border = _border()
        rh(ws, {row: 22})

    last_row = 6 + n_rows
    add_table(ws, "tblChecklist", f"B6:G{last_row}")

    # Conditional formatting
    status_col = "D"
    for val, bg, fc in [
        ("✓ Done",      P["green"],      P["green_dk"]),
        ("In Progress", P["yellow"],     P["black"]),
        ("To Do",       P["light_pink"], P["dark_pink"]),
        ("Cancelled",   P["red_light"],  P["red_dk"]),
    ]:
        diff = DifferentialStyle(fill=_fill(bg), font=_font(10, False, fc))
        from openpyxl.formatting.rule import Rule
        rule = Rule(type="containsText", operator="containsText",
                    text=val, dxf=diff)
        rule.formula = [f'NOT(ISERROR(SEARCH("{val}",{status_col}7)))']
        ws.conditional_formatting.add(
            f"B7:H{last_row}", rule)


# ─────────────────────────────────────────────────────────────────────
# SHEET 9 — BRIDAL PARTY
# ─────────────────────────────────────────────────────────────────────

def build_bridal_party(ws, sample: bool = True) -> None:
    ws.sheet_properties.tabColor = P["light_pink"]
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 14, "C": 22, "D": 14, "E": 22, "F": 14,
            "G": 20, "H": 20, "I": 18, "J": 22, "K": 2})

    mg(ws, 1, 2, 2, 10, "✦  BRIDAL PARTY  ✦",
       bg=P["hot_pink"], fg="FFFFFF", size=20, bold=True)
    mg(ws, 3, 2, 3, 10, "Track your wedding party details, attire & measurements",
       bg=P["pink"], fg="FFFFFF", size=11, bold=False)
    rh(ws, {1: 44, 2: 8, 3: 26, 4: 10})

    headers = ["Role", "Full Name", "Phone", "Email",
               "Dress / Suit Colour", "Dress Size / Suit Size",
               "Attire Ordered?", "Fitting Date", "Notes"]
    for i, h in enumerate(headers, start=2):
        w(ws, 5, i, h, bg=P["dark_pink"], fg="FFFFFF",
          size=10, bold=True, align="center")
    rh(ws, {5: 30})

    sample_party = [
        ("Maid of Honor",    "Jessica Rose",   "555-1001", "jess@email.com",  "Dusty Rose",  "Size 10", "Yes", "15 Jan 2025", "Best friend"),
        ("Bridesmaid",       "Chloe James",    "555-1002", "chloe@email.com", "Dusty Rose",  "Size 8",  "Yes", "15 Jan 2025", ""),
        ("Bridesmaid",       "Mia Turner",     "555-1003", "mia@email.com",   "Dusty Rose",  "Size 12", "Yes", "15 Jan 2025", ""),
        ("Bridesmaid",       "Ava Parker",     "555-1004", "ava@email.com",   "Dusty Rose",  "Size 6",  "No",  "",            "Ordering next week"),
        ("Best Man",         "Chris Stone",    "555-2001", "chris@email.com", "Navy Blue",   "42R",     "Yes", "20 Jan 2025", "Groom's brother"),
        ("Groomsman",        "Jake Ryan",      "555-2002", "jake@email.com",  "Navy Blue",   "40R",     "Yes", "20 Jan 2025", ""),
        ("Groomsman",        "Tyler Banks",    "555-2003", "tyler@email.com", "Navy Blue",   "44L",     "Yes", "20 Jan 2025", ""),
        ("Flower Girl",      "Lily Johnson",   "555-3001", "",                "White",       "Age 6",   "Yes", "",            "Bride's niece"),
        ("Ring Bearer",      "Ethan Davis",    "555-3002", "",                "Navy Blue",   "Age 4",   "Yes", "",            "Groom's nephew"),
    ]

    role_dv = dropdown(
        '"Maid of Honor,Bridesmaid,Flower Girl,Best Man,Groomsman,Ring Bearer,'
        'Mother of Bride,Father of Bride,Mother of Groom,Father of Groom,Other"',
        "B6:B2000", "Role", "Select role in wedding party")
    ordered_dv = dropdown('"Yes,No,Pending"', "I6:I2000",
                          "Ordered?", "Attire ordered?")
    ws.add_data_validation(role_dv)
    ws.add_data_validation(ordered_dv)

    n_rows = len(sample_party) if sample else 20
    for i in range(n_rows):
        row = 6 + i
        bg = P["blush"] if i % 2 == 0 else P["cream"]
        if sample and i < len(sample_party):
            vals = list(sample_party[i])
            for col, val in enumerate(vals, start=2):
                c = ws.cell(row=row, column=col, value=val)
                c.fill = _fill(bg)
                c.font = _font(10)
                c.alignment = _align("center" if col not in (3, 5) else "left")
                c.border = _border()
                if col == 8:
                    c.number_format = "DD MMM YYYY"
        else:
            for col in range(2, 11):
                c = ws.cell(row=row, column=col)
                c.fill = _fill(P["input"])
                c.border = _border()
        rh(ws, {row: 22})

    last_row = 5 + n_rows
    add_table(ws, "tblBridalParty", f"B5:J{last_row}")


# ─────────────────────────────────────────────────────────────────────
# SHEET 10 — SEATING CHART
# ─────────────────────────────────────────────────────────────────────

def build_seating(ws, sample: bool = True) -> None:
    ws.sheet_properties.tabColor = P["rose_gold"]
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 12, "C": 22, "D": 22, "E": 22, "F": 22,
            "G": 22, "H": 22, "I": 2})

    mg(ws, 1, 2, 2, 8, "✦  SEATING CHART PLANNER  ✦",
       bg=P["hot_pink"], fg="FFFFFF", size=20, bold=True)
    mg(ws, 3, 2, 3, 8,
       "Assign guests to tables — update as RSVPs come in",
       bg=P["rose_gold"], fg="FFFFFF", size=11, bold=False)
    rh(ws, {1: 44, 2: 8, 3: 26, 4: 10})

    # Note
    mg(ws, 5, 2, 5, 8,
       "💡 TIP: Enter guest names in the columns below each table number",
       bg=P["light_gold"], fg=P["black"], size=10, bold=False)
    rh(ws, {5: 26})

    # Table blocks — 2 tables per row, 5 tables total
    tables = [
        (1, "Head Table — Bridal Party",
         ["Bride & Groom", "Maid of Honor", "Best Man",
          "Bridesmaid 1", "Groomsman 1", "Bridesmaid 2", "Groomsman 2", "—"]),
        (2, "Table 2 — Immediate Family",
         ["Mother of Bride", "Father of Bride",
          "Mother of Groom", "Father of Groom",
          "Sibling 1", "Sibling 2", "Sibling 3", "Sibling 4"]),
        (3, "Table 3 — Bride's Friends",
         ["Sarah Johnson", "Emma Brown", "Olivia Wilson",
          "—", "—", "—", "—", "—"]),
        (4, "Table 4 — Groom's Friends",
         ["Michael Williams", "James Davis", "Liam Taylor",
          "—", "—", "—", "—", "—"]),
        (5, "Table 5",
         ["—", "—", "—", "—", "—", "—", "—", "—"]),
        (6, "Table 6", ["—"] * 8),
        (7, "Table 7", ["—"] * 8),
        (8, "Table 8", ["—"] * 8),
    ]

    col_positions = [2, 5]  # 2 tables per row, starting cols
    row_start = 7

    for idx, (table_num, table_name, guests) in enumerate(tables):
        col = col_positions[idx % 2]
        if idx % 2 == 0 and idx > 0:
            row_start += 14  # move down after 2 tables

        # Table header
        ws.merge_cells(start_row=row_start, start_column=col,
                       end_row=row_start, end_column=col + 2)
        hdr = ws.cell(row=row_start, column=col,
                      value=f"  🪑 {table_name}")
        hdr.fill = _fill(P["hot_pink"] if table_num == 1 else P["dark_pink"])
        hdr.font = _font(11, True, "FFFFFF")
        hdr.alignment = _align("left")
        rh(ws, {row_start: 28})

        # Sub-header
        ws.merge_cells(start_row=row_start + 1, start_column=col,
                       end_row=row_start + 1, end_column=col + 2)
        sub = ws.cell(row=row_start + 1, column=col,
                      value=f"  Seats {len(guests)}")
        sub.fill = _fill(P["pink"])
        sub.font = _font(9, False, "FFFFFF", italic=True)
        sub.alignment = _align("left")
        rh(ws, {row_start + 1: 20})

        # Guest rows
        sample_data = guests if sample else [""] * len(guests)
        for j, guest in enumerate(sample_data):
            row = row_start + 2 + j
            bg = P["blush"] if j % 2 == 0 else P["cream"]
            # Seat number
            seat_cell = ws.cell(row=row, column=col, value=j + 1)
            seat_cell.fill = _fill(P["blush"])
            seat_cell.font = _font(9, True, P["dark_pink"])
            seat_cell.alignment = _align("center")
            seat_cell.border = _border()
            # Guest name
            ws.merge_cells(start_row=row, start_column=col + 1,
                           end_row=row, end_column=col + 2)
            name_cell = ws.cell(row=row, column=col + 1,
                                value=guest if (sample and guest != "—") else "")
            name_cell.fill = _fill(P["input"])
            name_cell.font = _font(10)
            name_cell.alignment = _align()
            name_cell.border = _border()
            rh(ws, {row: 22})


# ─────────────────────────────────────────────────────────────────────
# SHEET 11 — REGISTRY
# ─────────────────────────────────────────────────────────────────────

def build_registry(ws, sample: bool = True) -> None:
    ws.sheet_properties.tabColor = P["hot_pink"]
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 22, "C": 16, "D": 14, "E": 14, "F": 12,
            "G": 14, "H": 18, "I": 12, "J": 12, "K": 22, "L": 2})

    mg(ws, 1, 2, 2, 11, "✦  GIFT REGISTRY TRACKER  ✦",
       bg=P["hot_pink"], fg="FFFFFF", size=20, bold=True)
    mg(ws, 3, 2, 3, 11,
       "Track registry items, purchases, and thank-you cards",
       bg=P["pink"], fg="FFFFFF", size=11, bold=False)
    rh(ws, {1: 44, 2: 8, 3: 26, 4: 10})

    # Stats
    rh(ws, {5: 28, 6: 36})
    reg_stats = [
        ("B", "Total Items",    "=IFERROR(COUNTA(C8:C2000),0)",              P["light_pink"]),
        ("D", "Purchased",      '=IFERROR(COUNTIF(G8:G2000,"Yes"),0)',        P["green"]),
        ("F", "Total Value",    "=IFERROR(SUM(D8:D2000),0)",                  P["light_gold"]),
        ("H", "Thank Yous Sent",'=IFERROR(COUNTIF(J8:J2000,"Yes"),0)',        P["blush"]),
    ]
    for col_letter, label, formula, bg in reg_stats:
        col_num = ord(col_letter) - ord("A") + 1
        lbl = ws.cell(row=5, column=col_num, value=label)
        lbl.fill = _fill(bg)
        lbl.font = _font(10, True, P["black"])
        lbl.alignment = _align("center")
        lbl.border = _border()
        ws.merge_cells(start_row=5, start_column=col_num,
                       end_row=5, end_column=col_num + 1)
        val = ws.cell(row=6, column=col_num, value=formula)
        val.fill = _fill(bg)
        val.font = _font(20, True, P["hot_pink"])
        val.alignment = _align("center")
        val.number_format = '"$"#,##0.00' if "Value" in label else "0"
        val.border = _border()
        ws.merge_cells(start_row=6, start_column=col_num,
                       end_row=6, end_column=col_num + 1)

    for col in range(1, 13):
        ws.cell(row=7, column=col).fill = _fill(P["white"])
    rh(ws, {7: 8})

    headers = ["Item / Gift", "Store / Registry", "Price",
               "Qty Wanted", "Qty Received", "Purchased?",
               "Received From", "Date Received", "Thank You?", "Notes"]
    for i, h in enumerate(headers, start=2):
        w(ws, 8, i, h, bg=P["dark_pink"], fg="FFFFFF",
          size=10, bold=True, align="center")
    rh(ws, {8: 30})

    sample_registry = [
        ("KitchenAid Stand Mixer",        "Williams Sonoma", 499.00, 1, 1, "Yes", "Emma Brown",     "15 Nov", "Yes", ""),
        ("Dyson Vacuum Cleaner",           "Target",          349.00, 1, 1, "Yes", "Michael & Sarah","18 Nov", "Yes", ""),
        ("Le Creuset Dutch Oven Set",      "Williams Sonoma", 389.00, 1, 0, "No",  "",               "",       "No",  ""),
        ("Egyptian Cotton Sheet Set (Q)", "Bed Bath Beyond", 120.00, 2, 1, "Yes", "James Davis",    "20 Nov", "No",  ""),
        ("Instant Pot Duo 7-in-1",        "Amazon",           89.00, 1, 1, "Yes", "Liam Taylor",    "22 Nov", "Yes", ""),
        ("Ninja Air Fryer XL",             "Target",          129.00, 1, 0, "No",  "",               "",       "No",  ""),
        ("Vitamix Blender",                "Williams Sonoma", 399.00, 1, 0, "No",  "",               "",       "No",  ""),
        ("Set of 6 Wine Glasses",          "Crate & Barrel",   79.00, 2, 2, "Yes", "Olivia Wilson",  "23 Nov", "No",  ""),
    ]

    purchased_dv = dropdown('"Yes,No,Pending"',  "H9:H2000",
                            "Purchased?", "Has this been purchased?")
    thanks_dv    = dropdown('"Yes,No"',          "K9:K2000",
                            "Thank You?", "Has thank-you been sent?")
    ws.add_data_validation(purchased_dv)
    ws.add_data_validation(thanks_dv)

    n_rows = len(sample_registry) if sample else 50
    for i in range(n_rows):
        row = 9 + i
        bg = P["blush"] if i % 2 == 0 else P["cream"]
        if sample and i < len(sample_registry):
            item, store, price, qty_w, qty_r, purch, giver, date, thanks, notes = sample_registry[i]
            for col, val, fmt in [
                (2, item,   "@"),  (3, store,  "@"),
                (4, price,  '"$"#,##0.00'), (5, qty_w, "0"),
                (6, qty_r,  "0"),  (7, purch,  "@"),
                (8, giver,  "@"),  (9, date,   "@"),
                (10, thanks,"@"), (11, notes, "@"),
            ]:
                c = ws.cell(row=row, column=col, value=val)
                c.fill = _fill(bg)
                c.font = _font(10)
                c.alignment = _align("center" if col not in (2, 3, 8, 11) else "left")
                c.border = _border()
                c.number_format = fmt
        else:
            for col in range(2, 12):
                c = ws.cell(row=row, column=col)
                c.fill = _fill(P["input"])
                c.font = _font(10)
                c.alignment = _align("center")
                c.border = _border()
        rh(ws, {row: 22})

    last_row = 8 + n_rows
    add_table(ws, "tblRegistry", f"B8:K{last_row}")


# ─────────────────────────────────────────────────────────────────────
# SHEET 12 — HONEYMOON
# ─────────────────────────────────────────────────────────────────────

def build_honeymoon(ws, sample: bool = True) -> None:
    ws.sheet_properties.tabColor = P["gold"]
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 18, "C": 26, "D": 16, "E": 14, "F": 14,
            "G": 16, "H": 16, "I": 20, "J": 2})

    mg(ws, 1, 2, 2, 9, "✦  HONEYMOON PLANNER  ✦",
       bg=P["hot_pink"], fg="FFFFFF", size=20, bold=True)
    mg(ws, 3, 2, 3, 9,
       "Plan your perfect honeymoon — itinerary, budget & packing",
       bg=P["gold"], fg="FFFFFF", size=11, bold=False)
    rh(ws, {1: 44, 2: 8, 3: 26, 4: 10})

    # Destination details
    section_header(ws, 5, 2, 9, "✦  DESTINATION & DETAILS  ✦", P["dark_pink"])
    rh(ws, {5: 30})
    honey_fields = [
        ("Destination",      ""),
        ("Departure Date",   ""),
        ("Return Date",      ""),
        ("Number of Nights", ""),
        ("Hotel / Resort",   ""),
        ("Confirmation #",   ""),
        ("Total Budget",     ""),
    ]
    for i, (label, val) in enumerate(honey_fields, start=6):
        w(ws, i, 2, label, bg=P["blush"], fg=P["black"],
          size=10, bold=True, align="right")
        c = ws.cell(row=i, column=3, value=val if val else None)
        c.fill = _fill(P["input"])
        c.font = _font(10)
        c.alignment = _align()
        c.border = _border()
        ws.merge_cells(start_row=i, start_column=3, end_row=i, end_column=4)
        if "Date" in label:
            c.number_format = "DD MMM YYYY"
        if "Budget" in label:
            c.number_format = '"$"#,##0.00'
        rh(ws, {i: 24})

    for col in range(1, 11):
        ws.cell(row=13, column=col).fill = _fill(P["white"])
    rh(ws, {13: 8})

    # Itinerary table
    section_header(ws, 14, 2, 9, "✦  DAILY ITINERARY  ✦", P["hot_pink"])
    rh(ws, {14: 30})
    itin_headers = ["Day #", "Day", "Activity / Plan", "Location",
                    "Booking Ref.", "Cost", "Date", "Notes"]
    for i, h in enumerate(itin_headers, start=2):
        w(ws, 15, i, h, bg=P["dark_pink"], fg="FFFFFF",
          size=10, bold=True, align="center")
    rh(ws, {15: 28})

    sample_itinerary = [
        (1, "Day 1",  "Arrival — check in & spa",         "Maldives Resort",    "CONF-001", 0,   "Complimentary welcome drinks"),
        (2, "Day 2",  "Snorkelling & beach day",           "North Atoll",        "",         120, "Snorkel tour booked"),
        (3, "Day 3",  "Sunset dolphin cruise",             "Ocean",              "TOUR-22",  180, ""),
        (4, "Day 4",  "Couples massage & pool day",        "Resort Spa",         "SPA-88",   250, "Pre-booked"),
        (5, "Day 5",  "Island hopping tour",               "Multiple Islands",   "TOUR-33",  150, ""),
        (6, "Day 6",  "Romantic beach dinner",             "Private Beach",      "DIN-01",   300, "Pre-arranged surprise"),
        (7, "Day 7",  "Watersports day",                   "Water Sports Centre","",         90,  ""),
        (8, "Day 8",  "Relax — spa & pool",                "Resort",             "",         0,   "Pack in evening"),
        (9, "Day 9",  "Departure — farewell breakfast",    "Resort",             "",         0,   "Check out by 11am"),
    ]

    n_rows = len(sample_itinerary) if sample else 14
    for i in range(n_rows):
        row = 16 + i
        bg = P["blush"] if i % 2 == 0 else P["cream"]
        if sample and i < len(sample_itinerary):
            _, day_lbl, activity, location, ref, cost, notes = sample_itinerary[i]
            for col, val, fmt in [
                (2, i+1,      "0"),
                (3, day_lbl,  "@"),
                (4, activity, "@"),
                (5, location, "@"),
                (6, ref,      "@"),
                (7, cost,     '"$"#,##0.00'),
                (8, "",       "DD MMM YYYY"),
                (9, notes,    "@"),
            ]:
                c = ws.cell(row=row, column=col, value=val)
                c.fill = _fill(bg)
                c.font = _font(10)
                c.alignment = _align("center" if col in (2, 6, 7, 8) else "left")
                c.border = _border()
                c.number_format = fmt
        else:
            for col in range(2, 10):
                c = ws.cell(row=row, column=col)
                c.fill = _fill(P["input"])
                c.font = _font(10)
                c.alignment = _align("center")
                c.border = _border()
        rh(ws, {row: 22})

    last_itin_row = 15 + n_rows
    add_table(ws, "tblItinerary", f"B15:I{last_itin_row}")

    # Budget summary below
    for col in range(1, 11):
        ws.cell(row=last_itin_row + 1, column=col).fill = _fill(P["white"])
    rh(ws, {last_itin_row + 1: 10})
    section_header(ws, last_itin_row + 2, 2, 9,
                   "✦  HONEYMOON BUDGET SUMMARY  ✦", P["gold"])
    rh(ws, {last_itin_row + 2: 28})
    honey_budget = [
        ("Flights",              0),
        ("Accommodation",        0),
        ("Activities & Tours",   0),
        ("Food & Dining",        0),
        ("Shopping",             0),
        ("Travel Insurance",     0),
        ("Other",                0),
    ]
    bh_start = last_itin_row + 3
    for i, (cat, val) in enumerate(honey_budget):
        row = bh_start + i
        bg = P["blush"] if i % 2 == 0 else P["cream"]
        w(ws, row, 2, cat, bg=bg, fg=P["black"], size=10, bold=True)
        c = ws.cell(row=row, column=3,
                    value=val if sample else None)
        c.fill = _fill(P["input"])
        c.font = _font(10)
        c.alignment = _align("center")
        c.border = _border()
        c.number_format = '"$"#,##0.00'
        rh(ws, {row: 22})

    total_row = bh_start + len(honey_budget)
    w(ws, total_row, 2, "TOTAL SPEND", bg=P["hot_pink"],
      fg="FFFFFF", size=11, bold=True, align="center")
    total_c = ws.cell(row=total_row, column=3,
                      value=f"=SUM(C{bh_start}:C{total_row-1})")
    total_c.fill = _fill(P["hot_pink"])
    total_c.font = _font(12, True, "FFFFFF")
    total_c.alignment = _align("center")
    total_c.border = _border()
    total_c.number_format = '"$"#,##0.00'
    rh(ws, {total_row: 28})


# ─────────────────────────────────────────────────────────────────────
# MAIN BUILD FUNCTION
# ─────────────────────────────────────────────────────────────────────

def build_workbook(sample: bool = True) -> Workbook:
    wb = Workbook()

    sheet_defs = [
        ("Welcome",          build_welcome),
        ("Overview",         build_overview),
        ("Budget Dashboard", build_budget_dashboard),
        ("Budget Detail",    lambda ws: build_budget_detail(ws, sample)),
        ("Guest List",       lambda ws: build_guest_list(ws, sample)),
        ("Vendors",          lambda ws: build_vendors(ws, sample)),
        ("Timeline",         lambda ws: build_timeline(ws, sample)),
        ("Checklist",        lambda ws: build_checklist(ws, sample)),
        ("Bridal Party",     lambda ws: build_bridal_party(ws, sample)),
        ("Seating",          lambda ws: build_seating(ws, sample)),
        ("Registry",         lambda ws: build_registry(ws, sample)),
        ("Honeymoon",        lambda ws: build_honeymoon(ws, sample)),
    ]

    # Use the default sheet for the first tab
    ws0 = wb.active
    ws0.title = sheet_defs[0][0]
    sheet_defs[0][1](ws0)

    for name, builder in sheet_defs[1:]:
        ws = wb.create_sheet(title=name)
        builder(ws)

    return wb


def main() -> None:
    out_dir = Path(__file__).parent.parent.parent.parent.parent / "output"
    out_dir.mkdir(exist_ok=True)

    print("Building SAMPLE version …")
    wb_sample = build_workbook(sample=True)
    sample_path = out_dir / "Bold_Balanced_Wedding_Bible_SAMPLE.xlsx"
    wb_sample.save(sample_path)
    print(f"  ✓ Saved: {sample_path}")

    print("Building BLANK (customer) version …")
    wb_blank = build_workbook(sample=False)
    blank_path = out_dir / "Bold_Balanced_Wedding_Bible_BLANK.xlsx"
    wb_blank.save(blank_path)
    print(f"  ✓ Saved: {blank_path}")

    print("\nDone! Both files are ready.")


if __name__ == "__main__":
    main()
