"""
Bold & Balanced Wedding Bible — Google Sheets Automated Planner
Generated with Python openpyxl (import the .xlsx into Google Drive → Google Sheets)

Features:
  - Live budget dashboard with SUMIF formulas
  - RSVP auto-counter (COUNTIF)
  - Vendor tracker with booking-status highlights
  - Master checklist with progress bar
  - Day-of timeline with sortable columns
  - Subtle pastel palette optimised for Google Sheets rendering
  - Single output: Bold_Balanced_Wedding_Bible_GoogleSheets.xlsx

Usage:
    pip install openpyxl
    python wedding_sheets_generator.py

Output (in ./output/):
    Bold_Balanced_Wedding_Bible_GoogleSheets.xlsx
"""

from __future__ import annotations

from pathlib import Path

import openpyxl
from openpyxl import Workbook
from openpyxl.chart import PieChart, Reference
from openpyxl.chart.series import DataPoint
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import (
    Alignment,
    Border,
    Font,
    GradientFill,
    PatternFill,
    Side,
)
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.table import Table, TableStyleInfo

# ─────────────────────────────────────────────────────────────────────
# PALETTE  — Google Sheets-friendly pastels
# ─────────────────────────────────────────────────────────────────────
P = {
    "hot_pink":    "E91E8C",
    "pink":        "F48FB1",
    "light_pink":  "FCE4EC",
    "blush":       "FDE8EE",
    "mauve":       "CE93D8",
    "lavender":    "F3E5F5",
    "gold":        "C9A84C",
    "light_gold":  "FFF9C4",
    "cream":       "FFFDE7",
    "white":       "FFFFFF",
    "dark":        "212121",
    "mid_gray":    "616161",
    "light_gray":  "F5F5F5",
    "rose_gold":   "B76E79",
    "teal":        "4DB6AC",
    "light_teal":  "E0F2F1",
    "green":       "66BB6A",
    "light_green": "E8F5E9",
    "red":         "EF5350",
    "light_red":   "FFEBEE",
    "amber":       "FFA726",
    "light_amber": "FFF3E0",
    "border":      "E0C0CC",
}


# ─────────────────────────────────────────────────────────────────────
# STYLE HELPERS
# ─────────────────────────────────────────────────────────────────────

def _fill(hex_color: str) -> PatternFill:
    return PatternFill("solid", fgColor=hex_color)


def _font(size: int = 10, bold: bool = False, color: str = "212121",
          italic: bool = False) -> Font:
    return Font(size=size, bold=bold, color=color, italic=italic,
                name="Calibri")


def _align(h: str = "left", v: str = "center",
           wrap: bool = False) -> Alignment:
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)


def _border(style: str = "thin", color: str = "E0C0CC") -> Border:
    s = Side(style=style, color=color)
    return Border(left=s, right=s, top=s, bottom=s)


def _bottom_border(color: str = "E0C0CC") -> Border:
    s = Side(style="thin", color=color)
    return Border(bottom=s)


def w(ws, row: int, col: int, value,
      fill: str | None = None, font: Font | None = None,
      align: Alignment | None = None, border: Border | None = None) -> None:
    cell = ws.cell(row=row, column=col, value=value)
    if fill:
        cell.fill = _fill(fill)
    if font:
        cell.font = font
    if align:
        cell.alignment = align
    if border:
        cell.border = border


def mg(ws, row: int, col_start: int, col_end: int, value,
       fill: str | None = None, font: Font | None = None,
       align: Alignment | None = None) -> None:
    ws.merge_cells(start_row=row, start_column=col_start,
                   end_row=row, end_column=col_end)
    cell = ws.cell(row=row, column=col_start, value=value)
    if fill:
        cell.fill = _fill(fill)
    if font:
        cell.font = font
    cell.alignment = align or _align("center", "center")


def rh(ws, heights: dict[int, float]) -> None:
    for row_idx, ht in heights.items():
        ws.row_dimensions[row_idx].height = ht


def cw(ws, widths: dict[int | str, float]) -> None:
    for col, wd in widths.items():
        letter = col if isinstance(col, str) else get_column_letter(col)
        ws.column_dimensions[letter].width = wd


def add_table(ws, ref: str, name: str,
              style: str = "TableStyleMedium6") -> None:
    tbl = Table(displayName=name, ref=ref)
    tbl.tableStyleInfo = TableStyleInfo(
        name=style, showFirstColumn=False,
        showLastColumn=False, showRowStripes=True, showColumnStripes=False,
    )
    ws.add_table(tbl)


def dropdown(ws, cells: str, formula: str, title: str = "",
             prompt: str = "") -> None:
    dv = DataValidation(type="list", formula1=formula,
                        showDropDown=False, allow_blank=True)
    dv.sqref = cells
    if title:
        dv.promptTitle = title
        dv.prompt = prompt
        dv.showInputMessage = True
    ws.add_data_validation(dv)


# ─────────────────────────────────────────────────────────────────────
# SHEET BUILDERS
# ─────────────────────────────────────────────────────────────────────

def build_welcome(wb: Workbook) -> None:
    ws = wb.active
    ws.title = "🏠 Welcome"
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = None

    cw(ws, {"A": 2, "B": 3, "C": 28, "D": 18, "E": 18, "F": 18, "G": 3})
    rh(ws, {1: 8, 2: 70, 3: 10, 4: 28, 5: 24, 6: 24, 7: 24, 8: 24, 9: 28,
            10: 20, 11: 20, 12: 20, 13: 20, 14: 20, 15: 20,
            16: 20, 17: 20, 18: 20, 19: 20, 20: 20})

    # Banner
    mg(ws, 2, 2, 6, "Bold & Balanced Wedding Bible",
       fill=P["hot_pink"],
       font=_font(28, bold=True, color="FFFFFF"),
       align=_align("center", "center"))

    mg(ws, 4, 2, 6, "Modern Luxury Wedding Planning System  ·  Google Sheets Edition",
       fill=P["blush"],
       font=_font(12, italic=True, color=P["rose_gold"]),
       align=_align("center", "center"))

    # Personalisation fields
    row = 6
    for label, col in [("Bride / Partner 1:", "C"), ("Groom / Partner 2:", "D"),
                        ("Wedding Date:", "E"), ("Venue:", "F")]:
        ws[f"B{row}"] = label
        ws[f"B{row}"].font = _font(9, bold=True, color=P["rose_gold"])
        ws[f"B{row}"].alignment = _align("right", "center")
        ws[f"{col}{row}"].border = _bottom_border(P["gold"])
        row += 1 if col == "F" else 0
        if col == "F":
            row += 1

    # Actually just make them stacked in col C
    ws["B6"].value = "Bride / Partner 1:"
    ws["B6"].font = _font(9, bold=True, color=P["rose_gold"])
    ws["B6"].alignment = _align("right", "center")
    ws["C6"].border = _bottom_border(P["gold"])

    ws["B7"].value = "Groom / Partner 2:"
    ws["B7"].font = _font(9, bold=True, color=P["rose_gold"])
    ws["B7"].alignment = _align("right", "center")
    ws["C7"].border = _bottom_border(P["gold"])

    ws["E6"].value = "Wedding Date:"
    ws["E6"].font = _font(9, bold=True, color=P["rose_gold"])
    ws["E6"].alignment = _align("right", "center")
    ws["F6"].border = _bottom_border(P["gold"])

    ws["E7"].value = "Venue:"
    ws["E7"].font = _font(9, bold=True, color=P["rose_gold"])
    ws["E7"].alignment = _align("right", "center")
    ws["F7"].border = _bottom_border(P["gold"])

    # Quick-nav section
    mg(ws, 9, 2, 6, "QUICK NAVIGATION",
       fill=P["gold"],
       font=_font(11, bold=True, color="FFFFFF"),
       align=_align("center", "center"))

    nav_items = [
        ("📊 Budget Dashboard",    "💍 Budget Detail"),
        ("👥 Guest List & RSVPs",  "🏢 Vendor Tracker"),
        ("⏰ Day-of Timeline",     "✅ Master Checklist"),
        ("💐 Bridal Party",        "🪑 Seating Chart"),
        ("🎁 Gift Registry",       "✈️ Honeymoon"),
    ]
    r = 10
    for left, right in nav_items:
        ws[f"C{r}"] = left
        ws[f"C{r}"].font = _font(10, color=P["hot_pink"])
        ws[f"C{r}"].alignment = _align("left", "center")
        ws[f"E{r}"] = right
        ws[f"E{r}"].font = _font(10, color=P["hot_pink"])
        ws[f"E{r}"].alignment = _align("left", "center")
        r += 1

    # Tab colour
    ws.sheet_properties.tabColor = P["hot_pink"]


def build_budget_dashboard(wb: Workbook) -> None:
    ws = wb.create_sheet("📊 Budget Dashboard")
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 3, "C": 26, "D": 14, "E": 14, "F": 14, "G": 14, "H": 3})
    rh(ws, {1: 8, 2: 40, 3: 10, 4: 28, 5: 22, 6: 22, 7: 22, 8: 22, 9: 22, 10: 22})

    # Header
    mg(ws, 2, 2, 7, "BUDGET DASHBOARD",
       fill=P["gold"],
       font=_font(18, bold=True, color="FFFFFF"),
       align=_align("center", "center"))

    # KPI row — references Budget Detail sheet
    kpi_labels = [
        ("Total Budget", "='💍 Budget Detail'!D3"),
        ("Total Spent",  "=SUMIF('💍 Budget Detail'!C8:C50,\"<>\",\"'💍 Budget Detail'!E8:E50\")"),
        ("Remaining",    "='📊 Budget Dashboard'!D5-'📊 Budget Dashboard'!E5"),
        ("% Used",       "=IF('📊 Budget Dashboard'!D5>0,'📊 Budget Dashboard'!E5/'📊 Budget Dashboard'!D5,0)"),
    ]
    for i, (label, formula) in enumerate(kpi_labels):
        col = 4 + i  # D, E, F, G
        ws.cell(row=4, column=col, value=label).font = _font(8, bold=True, color=P["mid_gray"])
        ws.cell(row=4, column=col).alignment = _align("center", "center")
        ws.cell(row=4, column=col).fill = _fill(P["light_gold"])

    # KPI cells with light background
    kpi_fills = [P["light_teal"], P["light_red"], P["light_green"], P["lavender"]]
    kpi_fonts = [P["teal"], P["red"], P["green"], P["mauve"]]
    for i, (label, formula) in enumerate(kpi_labels):
        col = 4 + i
        cell = ws.cell(row=5, column=col, value=formula)
        cell.font = _font(16, bold=True, color=kpi_fonts[i])
        cell.alignment = _align("center", "center")
        cell.fill = _fill(kpi_fills[i])
        if i == 3:
            cell.number_format = "0%"
        else:
            cell.number_format = '"$"#,##0.00'

    # Section breakdown table — references Budget Detail
    mg(ws, 7, 2, 7, "SPENDING BY CATEGORY",
       fill=P["rose_gold"],
       font=_font(11, bold=True, color="FFFFFF"),
       align=_align("center", "center"))

    headers = ["CATEGORY", "BUDGETED", "ACTUAL", "DIFFERENCE", "% OF BUDGET"]
    for i, hdr in enumerate(headers):
        col = 3 + i
        ws.cell(row=8, column=col, value=hdr).font = _font(8, bold=True, color="FFFFFF")
        ws.cell(row=8, column=col).fill = _fill(P["hot_pink"])
        ws.cell(row=8, column=col).alignment = _align("center", "center")

    categories = [
        "Venue", "Catering", "Photography", "Videography",
        "Flowers", "Music", "Cake", "Hair & Make-Up",
        "Attire", "Stationery", "Transport", "Honeymoon",
        "Miscellaneous",
    ]
    for i, cat in enumerate(categories):
        r = 9 + i
        fill_c = P["light_pink"] if i % 2 == 0 else P["white"]
        ws.cell(row=r, column=3, value=cat).fill = _fill(fill_c)
        ws.cell(row=r, column=3).font = _font(9, bold=True)
        # Budgeted — SUMIF from Detail sheet
        ws.cell(row=r, column=4,
                value=f"=IFERROR(SUMIF('💍 Budget Detail'!C:C,C{r},'💍 Budget Detail'!D:D),0)"
                ).number_format = '"$"#,##0.00'
        ws.cell(row=r, column=4).fill = _fill(fill_c)
        # Actual
        ws.cell(row=r, column=5,
                value=f"=IFERROR(SUMIF('💍 Budget Detail'!C:C,C{r},'💍 Budget Detail'!E:E),0)"
                ).number_format = '"$"#,##0.00'
        ws.cell(row=r, column=5).fill = _fill(fill_c)
        # Difference
        cell_diff = ws.cell(row=r, column=6, value=f"=D{r}-E{r}")
        cell_diff.number_format = '"$"#,##0.00'
        cell_diff.fill = _fill(fill_c)
        # % of budget
        ws.cell(row=r, column=7,
                value=f"=IFERROR(E{r}/D5,0)"
                ).number_format = "0.0%"
        ws.cell(row=r, column=7).fill = _fill(fill_c)

    # Conditional formatting on difference column
    from openpyxl.formatting.rule import ColorScaleRule
    ws.conditional_formatting.add(
        "F9:F21",
        ColorScaleRule(
            start_type="num", start_value=-500, start_color="EF5350",
            mid_type="num", mid_value=0, mid_color="FFFFFF",
            end_type="num", end_value=500, end_color="66BB6A",
        ),
    )

    ws.sheet_properties.tabColor = P["gold"]


def build_budget_detail(wb: Workbook) -> None:
    ws = wb.create_sheet("💍 Budget Detail")
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 4, "C": 22, "D": 14, "E": 14, "F": 14,
            "G": 18, "H": 22, "I": 3})
    rh(ws, {1: 8, 2: 40, 3: 28, 4: 8, 5: 8, 6: 8, 7: 26})

    mg(ws, 2, 2, 8, "BUDGET DETAIL",
       fill=P["gold"],
       font=_font(18, bold=True, color="FFFFFF"),
       align=_align("center", "center"))

    # Total budget input cell
    ws["B3"] = "Total Wedding Budget:"
    ws["B3"].font = _font(10, bold=True, color=P["rose_gold"])
    ws["B3"].alignment = _align("right", "center")
    ws["D3"].font = _font(14, bold=True, color=P["gold"])
    ws["D3"].number_format = '"$"#,##0.00'
    ws["D3"].fill = _fill(P["light_gold"])
    ws["D3"].border = _border()

    headers = ["#", "CATEGORY", "ITEM DESCRIPTION",
               "BUDGETED ($)", "ACTUAL ($)", "PAID ($)", "VENDOR", "NOTES"]
    col_fills = [P["hot_pink"]] * 8
    for i, hdr in enumerate(headers):
        cell = ws.cell(row=7, column=2 + i, value=hdr)
        cell.font = _font(9, bold=True, color="FFFFFF")
        cell.fill = _fill(P["hot_pink"])
        cell.alignment = _align("center", "center")
        cell.border = _border()

    categories = [
        ("Venue", ["Ceremony Hire", "Reception Hire", "Setup / Bump-in Fee"]),
        ("Catering", ["Food Per Head", "Staffing", "Equipment Hire"]),
        ("Photography", ["Full Day Coverage", "Second Shooter", "Album"]),
        ("Videography", ["Full Day Film", "Highlight Reel", "Raw Footage"]),
        ("Flowers", ["Bridal Bouquet", "Bridesmaid Bouquets", "Ceremony Arch",
                     "Table Centrepieces", "Button Holes"]),
        ("Music", ["Ceremony Musician", "Cocktail Hour", "DJ / Band Reception"]),
        ("Cake", ["Wedding Cake", "Dessert Table"]),
        ("Hair & Make-Up", ["Bride Hair", "Bride Make-Up", "Bridesmaid Hair",
                             "Bridesmaid Make-Up"]),
        ("Attire", ["Wedding Dress", "Alterations", "Bridal Accessories",
                    "Groom Suit", "Groomsmen Attire"]),
        ("Stationery", ["Invitations", "Save-the-Dates", "Menus & Programs",
                        "Place Cards", "Thank-You Cards"]),
        ("Transport", ["Bridal Car", "Guest Shuttle"]),
        ("Honeymoon", ["Flights", "Accommodation", "Activities", "Travel Insurance"]),
        ("Miscellaneous", ["Favours", "Decorations", "Photo Booth",
                           "Gifts — Bridal Party", "Contingency"]),
    ]

    row = 8
    for cat, items in categories:
        for item in items:
            fill_c = P["light_pink"] if row % 2 == 0 else P["white"]
            ws.cell(row=row, column=2, value=row - 7).fill = _fill(fill_c)
            ws.cell(row=row, column=2).font = _font(8, color=P["mid_gray"])
            ws.cell(row=row, column=2).alignment = _align("center", "center")
            ws.cell(row=row, column=3, value=cat).fill = _fill(fill_c)
            ws.cell(row=row, column=3).font = _font(9, bold=True)
            ws.cell(row=row, column=4, value=item).fill = _fill(fill_c)
            ws.cell(row=row, column=4).font = _font(9)
            for dc in range(5, 9):
                ws.cell(row=row, column=dc).fill = _fill(fill_c)
                if dc <= 7:
                    ws.cell(row=row, column=dc).number_format = '"$"#,##0.00'
            row += 1

    # Table
    add_table(ws, f"B7:I{row - 1}", "tblBudgetDetail", "TableStyleMedium6")

    # Totals row
    ws.cell(row=row, column=2, value="TOTALS").font = _font(10, bold=True, color="FFFFFF")
    ws.cell(row=row, column=2).fill = _fill(P["hot_pink"])
    for dc, col_letter in [(5, "E"), (6, "F"), (7, "G")]:
        cell = ws.cell(row=row, column=dc,
                       value=f"=SUM({col_letter}8:{col_letter}{row - 1})")
        cell.font = _font(10, bold=True, color="FFFFFF")
        cell.fill = _fill(P["hot_pink"])
        cell.number_format = '"$"#,##0.00'

    ws.sheet_properties.tabColor = P["rose_gold"]


def build_guest_list(wb: Workbook) -> None:
    ws = wb.create_sheet("👥 Guest List")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "B8"
    cw(ws, {"A": 2, "B": 4, "C": 24, "D": 20, "E": 12, "F": 12,
            "G": 8, "H": 8, "I": 8, "J": 14, "K": 8, "L": 8,
            "M": 8, "N": 3})
    rh(ws, {1: 8, 2: 40, 3: 28, 4: 8, 5: 8, 6: 8, 7: 26})

    mg(ws, 2, 2, 13, "GUEST LIST & RSVP TRACKER",
       fill=P["pink"],
       font=_font(18, bold=True, color="FFFFFF"),
       align=_align("center", "center"))

    # Stats row
    stats = [
        ("Total Invited",  "=COUNTA(C8:C500)"),
        ("Attending",      "=COUNTIF(G8:G500,\"Yes\")"),
        ("Declined",       "=COUNTIF(G8:G500,\"No\")"),
        ("Awaiting RSVP",  "=COUNTIF(G8:G500,\"\")"),
    ]
    for i, (label, formula) in enumerate(stats):
        col = 2 + i * 3
        mg(ws, 3, col, col + 1, label,
           fill=P["blush"],
           font=_font(8, bold=True, color=P["rose_gold"]),
           align=_align("center", "center"))
        ws.cell(row=4, column=col, value=formula)
        ws.cell(row=4, column=col).font = _font(16, bold=True, color=P["hot_pink"])
        ws.cell(row=4, column=col).alignment = _align("center", "center")
        ws.merge_cells(start_row=4, start_column=col,
                       end_row=4, end_column=col + 1)

    headers = [
        "#", "FULL NAME", "EMAIL ADDRESS", "PHONE",
        "SIDE (B/G)", "TABLE #", "RSVP", "MEAL CHOICE",
        "DIETARY", "GIFT RECEIVED?", "THANK YOU SENT?", "NOTES",
    ]
    for i, hdr in enumerate(headers):
        cell = ws.cell(row=7, column=2 + i, value=hdr)
        cell.font = _font(9, bold=True, color="FFFFFF")
        cell.fill = _fill(P["pink"])
        cell.alignment = _align("center", "center")
        cell.border = _border()

    for r in range(8, 108):
        fill_c = P["light_pink"] if r % 2 == 0 else P["white"]
        for col in range(2, 14):
            ws.cell(row=r, column=col).fill = _fill(fill_c)
        ws.cell(row=r, column=2, value=r - 7).font = _font(8, color=P["mid_gray"])
        ws.cell(row=r, column=2).alignment = _align("center", "center")

    add_table(ws, "B7:M107", "tblGuests", "TableStyleMedium9")
    dropdown(ws, "F8:F107", '"B (Bride),G (Groom),Both,Family,Friend"',
             "Side", "Select which side of the family")
    dropdown(ws, "H8:H107", '"Yes,No,Maybe"', "RSVP", "")
    dropdown(ws, "I8:I107",
             '"Standard,Vegetarian,Vegan,Gluten-Free,Halal,Kosher,Kids Meal"',
             "Meal", "")
    dropdown(ws, "K8:K107", '"Yes,No,Pending"', "Gift Received", "")
    dropdown(ws, "L8:L107", '"Yes,No,Pending"', "Thank You", "")

    # Highlight RSVP = Yes → green, No → red
    ws.conditional_formatting.add(
        "H8:H107",
        CellIsRule(operator="equal", formula=['"Yes"'],
                   fill=_fill(P["light_green"])),
    )
    ws.conditional_formatting.add(
        "H8:H107",
        CellIsRule(operator="equal", formula=['"No"'],
                   fill=_fill(P["light_red"])),
    )

    ws.sheet_properties.tabColor = P["pink"]


def build_vendors(wb: Workbook) -> None:
    ws = wb.create_sheet("🏢 Vendor Tracker")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "B8"
    cw(ws, {"A": 2, "B": 4, "C": 22, "D": 20, "E": 16, "F": 14,
            "G": 14, "H": 12, "I": 12, "J": 12, "K": 12, "L": 22, "M": 3})
    rh(ws, {1: 8, 2: 40, 3: 8, 4: 8, 5: 8, 6: 8, 7: 26})

    mg(ws, 2, 2, 12, "VENDOR TRACKER",
       fill=P["rose_gold"],
       font=_font(18, bold=True, color="FFFFFF"),
       align=_align("center", "center"))

    headers = [
        "#", "VENDOR TYPE", "COMPANY / NAME", "CONTACT PERSON",
        "PHONE", "EMAIL", "BOOKED?", "QUOTED ($)", "DEPOSIT ($)",
        "BALANCE ($)", "DUE DATE", "NOTES",
    ]
    for i, hdr in enumerate(headers):
        cell = ws.cell(row=7, column=2 + i, value=hdr)
        cell.font = _font(9, bold=True, color="FFFFFF")
        cell.fill = _fill(P["rose_gold"])
        cell.alignment = _align("center", "center")
        cell.border = _border()

    vendor_types = [
        "Venue — Ceremony", "Venue — Reception", "Photographer",
        "Videographer", "Caterer", "Bar / Beverages", "Florist",
        "DJ / Band", "Wedding Cake", "Hair Stylist", "Make-Up Artist",
        "Officiant", "Wedding Planner", "Transport", "Stationery",
        "Photo Booth", "Décor / Hire", "Accommodation",
    ]
    for i, vtype in enumerate(vendor_types):
        r = 8 + i
        fill_c = P["lavender"] if i % 2 == 0 else P["white"]
        for col in range(2, 14):
            ws.cell(row=r, column=col).fill = _fill(fill_c)
        ws.cell(row=r, column=2, value=i + 1).font = _font(8, color=P["mid_gray"])
        ws.cell(row=r, column=2).alignment = _align("center", "center")
        ws.cell(row=r, column=3, value=vtype).font = _font(9, bold=True)
        for dc in [9, 10, 11]:
            ws.cell(row=r, column=dc).number_format = '"$"#,##0.00'

    add_table(ws, "B7:M25", "tblVendors", "TableStyleMedium7")
    dropdown(ws, "H8:H25", '"Yes,No,Enquired,Deposit Paid,Fully Paid"',
             "Booking Status", "")

    ws.conditional_formatting.add(
        "H8:H25",
        CellIsRule(operator="equal", formula=['"Yes"'],
                   fill=_fill(P["light_green"])),
    )
    ws.conditional_formatting.add(
        "H8:H25",
        CellIsRule(operator="equal", formula=['"No"'],
                   fill=_fill(P["light_red"])),
    )
    ws.conditional_formatting.add(
        "H8:H25",
        CellIsRule(operator="equal", formula=['"Deposit Paid"'],
                   fill=_fill(P["light_amber"])),
    )

    ws.sheet_properties.tabColor = P["rose_gold"]


def build_timeline(wb: Workbook) -> None:
    ws = wb.create_sheet("⏰ Day-of Timeline")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "B8"
    cw(ws, {"A": 2, "B": 4, "C": 12, "D": 26, "E": 22, "F": 22,
            "G": 10, "H": 3})
    rh(ws, {1: 8, 2: 40, 3: 8, 4: 8, 5: 8, 6: 8, 7: 26})

    mg(ws, 2, 2, 7, "DAY-OF TIMELINE",
       fill=P["mauve"],
       font=_font(18, bold=True, color="FFFFFF"),
       align=_align("center", "center"))

    headers = ["TIME", "EVENT / ACTIVITY", "LOCATION", "PERSON RESPONSIBLE", "DONE?"]
    for i, hdr in enumerate(headers):
        cell = ws.cell(row=7, column=2 + i, value=hdr)
        cell.font = _font(9, bold=True, color="FFFFFF")
        cell.fill = _fill(P["mauve"])
        cell.alignment = _align("center", "center")
        cell.border = _border()

    default_events = [
        ("6:00 AM",  "Bride wakes up / morning routine",     "Bride's home",       "Bride"),
        ("7:00 AM",  "Hair & Make-Up begins — Bride",        "Salon / Getting-ready room", "Bride, MOH"),
        ("8:00 AM",  "Hair & Make-Up — Bridesmaids",         "Salon",              "MOH"),
        ("10:00 AM", "Photographer arrives for getting-ready shots", "Bride's room", "Photographer"),
        ("11:00 AM", "Bridal party dressed and ready",       "Getting-ready room", "MOH"),
        ("11:30 AM", "Bouquets delivered",                   "Ceremony venue",     "Florist"),
        ("12:00 PM", "Guests begin to arrive",               "Ceremony venue",     "Ushers"),
        ("12:30 PM", "Ceremony begins — processional",       "Ceremony venue",     "Officiant"),
        ("1:00 PM",  "Ceremony concludes — confetti exit",   "Ceremony venue",     "All guests"),
        ("1:15 PM",  "Couple & family photos",               "Garden / outdoors",  "Photographer"),
        ("2:00 PM",  "Cocktail hour begins",                 "Cocktail area",      "MC"),
        ("3:30 PM",  "Guests seated for reception",          "Reception room",     "MC"),
        ("3:45 PM",  "Couple introduced / first dance",      "Dance floor",        "DJ"),
        ("4:00 PM",  "Entrée served",                        "Reception room",     "Caterer"),
        ("4:30 PM",  "Welcome speeches",                     "Reception room",     "MC, Best Man"),
        ("5:00 PM",  "Main course served",                   "Reception room",     "Caterer"),
        ("5:30 PM",  "Speeches continue — Bride & Groom",    "Reception room",     "Bride, Groom"),
        ("6:00 PM",  "Wedding cake cutting",                 "Reception room",     "Couple"),
        ("6:15 PM",  "Dessert served",                       "Reception room",     "Caterer"),
        ("6:45 PM",  "Dancing begins / DJ sets",             "Dance floor",        "DJ"),
        ("10:00 PM", "Last dance",                           "Dance floor",        "DJ"),
        ("10:30 PM", "Reception concludes / farewell",       "Entrance",           "All"),
    ]

    for i, (time, event, loc, person) in enumerate(default_events):
        r = 8 + i
        fill_c = P["lavender"] if i % 2 == 0 else P["white"]
        ws.cell(row=r, column=2, value=time).fill = _fill(fill_c)
        ws.cell(row=r, column=2).font = _font(9, bold=True, color=P["mauve"])
        ws.cell(row=r, column=3, value=event).fill = _fill(fill_c)
        ws.cell(row=r, column=3).font = _font(9)
        ws.cell(row=r, column=4, value=loc).fill = _fill(fill_c)
        ws.cell(row=r, column=4).font = _font(9, italic=True, color=P["mid_gray"])
        ws.cell(row=r, column=5, value=person).fill = _fill(fill_c)
        ws.cell(row=r, column=5).font = _font(9)
        ws.cell(row=r, column=6).fill = _fill(fill_c)

    # extra blank rows
    for i in range(len(default_events), len(default_events) + 18):
        r = 8 + i
        fill_c = P["lavender"] if i % 2 == 0 else P["white"]
        for col in range(2, 8):
            ws.cell(row=r, column=col).fill = _fill(fill_c)

    last_r = 8 + len(default_events) + 17
    add_table(ws, f"B7:F{last_r}", "tblTimeline", "TableStyleMedium10")
    dropdown(ws, f"F8:F{last_r}", '"✅ Done,⏳ Pending,❌ Skipped"', "Done?", "")

    ws.sheet_properties.tabColor = P["mauve"]


def build_checklist(wb: Workbook) -> None:
    ws = wb.create_sheet("✅ Master Checklist")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "B8"
    cw(ws, {"A": 2, "B": 4, "C": 22, "D": 34, "E": 10, "F": 16, "G": 16, "H": 3})
    rh(ws, {1: 8, 2: 40, 3: 28, 4: 8, 5: 8, 6: 8, 7: 26})

    mg(ws, 2, 2, 7, "MASTER WEDDING CHECKLIST",
       fill=P["teal"],
       font=_font(18, bold=True, color="FFFFFF"),
       align=_align("center", "center"))

    # Progress stats
    ws["C3"] = "Total Tasks:"
    ws["C3"].font = _font(9, bold=True, color=P["mid_gray"])
    ws["D3"] = "=COUNTA(D8:D500)"
    ws["D3"].font = _font(14, bold=True, color=P["teal"])
    ws["E3"] = "Done:"
    ws["E3"].font = _font(9, bold=True, color=P["mid_gray"])
    ws["F3"] = "=COUNTIF(F8:F500,\"Done\")"
    ws["F3"].font = _font(14, bold=True, color=P["green"])
    ws["G3"] = "=IFERROR(F3/D3,0)"
    ws["G3"].number_format = "0%"
    ws["G3"].font = _font(14, bold=True, color=P["hot_pink"])

    headers = ["#", "TIMEFRAME", "TASK", "PRIORITY", "STATUS", "ASSIGNED TO", "NOTES"]
    for i, hdr in enumerate(headers):
        cell = ws.cell(row=7, column=2 + i, value=hdr)
        cell.font = _font(9, bold=True, color="FFFFFF")
        cell.fill = _fill(P["teal"])
        cell.alignment = _align("center", "center")
        cell.border = _border()

    timeline_tasks = [
        ("12+ Months", "Set overall wedding budget", "High"),
        ("12+ Months", "Choose wedding date", "High"),
        ("12+ Months", "Create initial guest list", "High"),
        ("12+ Months", "Book ceremony venue", "High"),
        ("12+ Months", "Book reception venue", "High"),
        ("12+ Months", "Hire wedding planner (if using)", "Medium"),
        ("12+ Months", "Start wedding dress shopping", "Medium"),
        ("12+ Months", "Book photographer", "High"),
        ("12+ Months", "Book videographer", "High"),
        ("9-12 Months", "Book caterer", "High"),
        ("9-12 Months", "Book florist", "High"),
        ("9-12 Months", "Book DJ / band", "High"),
        ("9-12 Months", "Book officiant", "High"),
        ("9-12 Months", "Send save-the-dates", "High"),
        ("9-12 Months", "Order wedding dress", "High"),
        ("9-12 Months", "Book hair & make-up", "Medium"),
        ("9-12 Months", "Book accommodation for guests", "Medium"),
        ("6-9 Months", "Order wedding cake", "Medium"),
        ("6-9 Months", "Book transportation", "Medium"),
        ("6-9 Months", "Plan and book honeymoon", "High"),
        ("6-9 Months", "Create wedding website", "Low"),
        ("6-9 Months", "Register for gifts", "Medium"),
        ("6-9 Months", "Plan rehearsal dinner", "Medium"),
        ("6-9 Months", "Order wedding invitations", "High"),
        ("3-6 Months", "Mail invitations (8–12 weeks out)", "High"),
        ("3-6 Months", "Order wedding rings", "High"),
        ("3-6 Months", "Schedule hair & make-up trial", "Medium"),
        ("3-6 Months", "Finalise rehearsal dinner", "Medium"),
        ("3-6 Months", "Purchase wedding favours", "Low"),
        ("3-6 Months", "Plan ceremony details with officiant", "High"),
        ("3-6 Months", "Finalise menu with caterer", "High"),
        ("3-6 Months", "Write personal vows", "High"),
        ("1-3 Months", "Chase outstanding RSVPs", "High"),
        ("1-3 Months", "Finalise seating chart", "High"),
        ("1-3 Months", "Confirm all vendor bookings", "High"),
        ("1-3 Months", "Break in wedding shoes", "Low"),
        ("1-3 Months", "Purchase gifts for wedding party", "Medium"),
        ("1-3 Months", "Create detailed day-of timeline", "High"),
        ("1-3 Months", "Apply for marriage licence", "High"),
        ("Final Weeks", "Final dress fitting", "High"),
        ("Final Weeks", "Deliver final guest numbers to caterer", "High"),
        ("Final Weeks", "Confirm final details with all vendors", "High"),
        ("Final Weeks", "Prepare vendor tip envelopes", "Medium"),
        ("Final Weeks", "Assign day-of coordinator", "High"),
        ("Final Weeks", "Pack overnight bag for wedding night", "Medium"),
        ("Final Weeks", "Confirm honeymoon travel details", "High"),
        ("Wedding Week", "Pick up wedding dress", "High"),
        ("Wedding Week", "Confirm vendor delivery schedule", "High"),
        ("Wedding Week", "Delegate tasks to wedding party", "High"),
        ("Wedding Week", "Relax and enjoy your rehearsal!", "High"),
    ]

    for i, (period, task, priority) in enumerate(timeline_tasks):
        r = 8 + i
        fill_c = P["light_teal"] if i % 2 == 0 else P["white"]
        ws.cell(row=r, column=2, value=i + 1).font = _font(8, color=P["mid_gray"])
        ws.cell(row=r, column=2).alignment = _align("center", "center")
        ws.cell(row=r, column=2).fill = _fill(fill_c)
        ws.cell(row=r, column=3, value=period).fill = _fill(fill_c)
        ws.cell(row=r, column=3).font = _font(9, bold=True, color=P["teal"])
        ws.cell(row=r, column=4, value=task).fill = _fill(fill_c)
        ws.cell(row=r, column=4).font = _font(9)
        ws.cell(row=r, column=5, value=priority).fill = _fill(fill_c)
        ws.cell(row=r, column=5).font = _font(9)
        ws.cell(row=r, column=6).fill = _fill(fill_c)
        ws.cell(row=r, column=7).fill = _fill(fill_c)
        ws.cell(row=r, column=8).fill = _fill(fill_c)

    last_r = 8 + len(timeline_tasks) - 1
    add_table(ws, f"B7:H{last_r}", "tblChecklist", "TableStyleMedium4")
    dropdown(ws, f"E8:E{last_r}", '"High,Medium,Low"', "Priority", "")
    dropdown(ws, f"F8:F{last_r}",
             '"Done,In Progress,Not Started,Waiting,Skipped"', "Status", "")

    ws.conditional_formatting.add(
        f"F8:F{last_r}",
        CellIsRule(operator="equal", formula=['"Done"'],
                   fill=_fill(P["light_green"])),
    )
    ws.conditional_formatting.add(
        f"F8:F{last_r}",
        CellIsRule(operator="equal", formula=['"In Progress"'],
                   fill=_fill(P["light_amber"])),
    )

    ws.sheet_properties.tabColor = P["teal"]


def build_bridal_party(wb: Workbook) -> None:
    ws = wb.create_sheet("💐 Bridal Party")
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 4, "C": 18, "D": 14, "E": 14, "F": 14,
            "G": 12, "H": 14, "I": 22, "J": 3})
    rh(ws, {1: 8, 2: 40, 3: 8, 4: 8, 5: 8, 6: 8, 7: 26})

    mg(ws, 2, 2, 9, "BRIDAL PARTY DETAILS",
       fill=P["pink"],
       font=_font(18, bold=True, color="FFFFFF"),
       align=_align("center", "center"))

    headers = [
        "#", "ROLE", "FULL NAME", "PHONE", "EMAIL",
        "ATTIRE SIZE", "COLOUR / STYLE", "GIFT GIVEN", "NOTES",
    ]
    for i, hdr in enumerate(headers):
        cell = ws.cell(row=7, column=2 + i, value=hdr)
        cell.font = _font(9, bold=True, color="FFFFFF")
        cell.fill = _fill(P["pink"])
        cell.alignment = _align("center", "center")
        cell.border = _border()

    default_roles = [
        "Bride", "Maid of Honour", "Bridesmaid 1", "Bridesmaid 2",
        "Bridesmaid 3", "Bridesmaid 4", "Flower Girl",
        "Groom", "Best Man", "Groomsman 1", "Groomsman 2",
        "Groomsman 3", "Groomsman 4", "Ring Bearer",
        "Mother of Bride", "Father of Bride",
        "Mother of Groom", "Father of Groom",
    ]
    for i, role in enumerate(default_roles):
        r = 8 + i
        fill_c = P["light_pink"] if i % 2 == 0 else P["white"]
        ws.cell(row=r, column=2, value=i + 1).fill = _fill(fill_c)
        ws.cell(row=r, column=2).font = _font(8, color=P["mid_gray"])
        ws.cell(row=r, column=2).alignment = _align("center", "center")
        ws.cell(row=r, column=3, value=role).fill = _fill(fill_c)
        ws.cell(row=r, column=3).font = _font(9, bold=True)
        for col in range(4, 11):
            ws.cell(row=r, column=col).fill = _fill(fill_c)

    add_table(ws, f"B7:J{8 + len(default_roles) - 1}", "tblBridalParty",
              "TableStyleMedium9")
    dropdown(ws, f"I8:I{8 + len(default_roles) - 1}", '"Yes,No,Pending"',
             "Gift Given", "")

    ws.sheet_properties.tabColor = P["pink"]


def build_seating(wb: Workbook) -> None:
    ws = wb.create_sheet("🪑 Seating Chart")
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 4, "C": 12, "D": 22, "E": 22, "F": 8, "G": 3})
    rh(ws, {1: 8, 2: 40, 3: 8, 4: 8, 5: 8, 6: 8, 7: 26})

    mg(ws, 2, 2, 6, "SEATING CHART",
       fill=P["blush"],
       font=_font(18, bold=True, color=P["rose_gold"]),
       align=_align("center", "center"))

    headers = ["TABLE #", "GUEST NAME", "DIETARY / MEAL", "SEAT #"]
    for i, hdr in enumerate(headers):
        cell = ws.cell(row=7, column=2 + i, value=hdr)
        cell.font = _font(9, bold=True, color="FFFFFF")
        cell.fill = _fill(P["rose_gold"])
        cell.alignment = _align("center", "center")
        cell.border = _border()

    for r in range(8, 208):
        fill_c = P["blush"] if r % 2 == 0 else P["white"]
        for col in range(2, 7):
            ws.cell(row=r, column=col).fill = _fill(fill_c)

    add_table(ws, "B7:E207", "tblSeating", "TableStyleMedium14")

    ws.sheet_properties.tabColor = P["blush"]


def build_registry(wb: Workbook) -> None:
    ws = wb.create_sheet("🎁 Gift Registry")
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "B8"
    cw(ws, {"A": 2, "B": 4, "C": 26, "D": 18, "E": 14, "F": 12,
            "G": 12, "H": 12, "I": 22, "J": 3})
    rh(ws, {1: 8, 2: 40, 3: 8, 4: 8, 5: 8, 6: 8, 7: 26})

    mg(ws, 2, 2, 9, "GIFT REGISTRY & TRACKER",
       fill=P["mauve"],
       font=_font(18, bold=True, color="FFFFFF"),
       align=_align("center", "center"))

    # Stats
    ws["C3"] = "Total Gifts:"
    ws["C3"].font = _font(9, bold=True, color=P["mid_gray"])
    ws["D3"] = "=COUNTA(C8:C500)"
    ws["D3"].font = _font(14, bold=True, color=P["mauve"])

    ws["F3"] = "Thank You Sent:"
    ws["F3"].font = _font(9, bold=True, color=P["mid_gray"])
    ws["G3"] = "=COUNTIF(H8:H500,\"Yes\")"
    ws["G3"].font = _font(14, bold=True, color=P["green"])

    headers = [
        "#", "GIFT DESCRIPTION", "FROM (GUEST NAME)", "DATE RECEIVED",
        "VALUE ($)", "STORE / REGISTRY", "THANK YOU SENT?", "NOTES",
    ]
    for i, hdr in enumerate(headers):
        cell = ws.cell(row=7, column=2 + i, value=hdr)
        cell.font = _font(9, bold=True, color="FFFFFF")
        cell.fill = _fill(P["mauve"])
        cell.alignment = _align("center", "center")
        cell.border = _border()

    for r in range(8, 108):
        fill_c = P["lavender"] if r % 2 == 0 else P["white"]
        for col in range(2, 11):
            ws.cell(row=r, column=col).fill = _fill(fill_c)
        ws.cell(row=r, column=2, value=r - 7).font = _font(8, color=P["mid_gray"])
        ws.cell(row=r, column=2).alignment = _align("center", "center")
        if r < 9:
            ws.cell(row=r, column=6).number_format = '"$"#,##0.00'

    add_table(ws, "B7:I107", "tblRegistry", "TableStyleMedium10")
    dropdown(ws, "H8:H107", '"Yes,No,Pending"', "Thank You Sent", "")

    ws.conditional_formatting.add(
        "H8:H107",
        CellIsRule(operator="equal", formula=['"Yes"'],
                   fill=_fill(P["light_green"])),
    )

    ws.sheet_properties.tabColor = P["mauve"]


def build_honeymoon(wb: Workbook) -> None:
    ws = wb.create_sheet("✈️ Honeymoon")
    ws.sheet_view.showGridLines = False
    cw(ws, {"A": 2, "B": 4, "C": 20, "D": 20, "E": 20, "F": 20, "G": 3})
    rh(ws, {1: 8, 2: 40, 3: 8, 4: 8, 5: 8, 6: 8,
            7: 26, 8: 20, 9: 20, 10: 20, 11: 20, 12: 20, 13: 20, 14: 20,
            15: 20, 16: 20, 17: 20, 18: 28, 19: 20, 20: 20, 21: 20, 22: 20,
            23: 20, 24: 20, 25: 20, 26: 20, 27: 20, 28: 20})

    mg(ws, 2, 2, 6, "HONEYMOON PLANNER",
       fill=P["gold"],
       font=_font(18, bold=True, color="FFFFFF"),
       align=_align("center", "center"))

    # Overview fields
    mg(ws, 4, 2, 6, "TRIP OVERVIEW",
       fill=P["light_gold"],
       font=_font(10, bold=True, color=P["gold"]),
       align=_align("left", "center"))

    overview_fields = [
        ("Destination", "B", "C"),
        ("Departure Date", "B", "C"),
        ("Return Date", "D", "E"),
        ("Total Budget ($)", "B", "C"),
        ("Amount Paid ($)", "D", "E"),
        ("Balance Due ($)", "B", "C"),
        ("Travel Insurance Ref", "D", "E"),
    ]
    row = 5
    used: set[int] = set()
    for label, lc, vc in overview_fields:
        if row in used:
            row += 1
        ws[f"{lc}{row}"] = label
        ws[f"{lc}{row}"].font = _font(9, bold=True, color=P["rose_gold"])
        ws[f"{lc}{row}"].alignment = _align("right", "center")
        ws[f"{vc}{row}"].border = _bottom_border(P["gold"])
        ws[f"{vc}{row}"].font = _font(9)
        row += 1

    # Flight / accommodation table
    mg(ws, 18, 2, 6, "FLIGHTS & ACCOMMODATION",
       fill=P["light_gold"],
       font=_font(10, bold=True, color=P["gold"]),
       align=_align("left", "center"))

    travel_headers = ["ITEM", "DETAIL", "CONFIRMATION #", "DATE / TIME", "NOTES"]
    for i, hdr in enumerate(travel_headers):
        cell = ws.cell(row=19, column=2 + i, value=hdr)
        cell.font = _font(9, bold=True, color="FFFFFF")
        cell.fill = _fill(P["gold"])
        cell.alignment = _align("center", "center")
        cell.border = _border()

    travel_rows = [
        "Outbound Flight", "Return Flight",
        "Hotel / Resort", "Transfer (Arrival)", "Transfer (Departure)",
        "Restaurant Reservation 1", "Restaurant Reservation 2",
        "Activity / Excursion 1", "Activity / Excursion 2",
    ]
    for i, item in enumerate(travel_rows):
        r = 20 + i
        fill_c = P["light_gold"] if i % 2 == 0 else P["cream"]
        ws.cell(row=r, column=2, value=item).fill = _fill(fill_c)
        ws.cell(row=r, column=2).font = _font(9, bold=True)
        for col in range(3, 7):
            ws.cell(row=r, column=col).fill = _fill(fill_c)

    add_table(ws, f"B19:F{20 + len(travel_rows) - 1}", "tblItinerary",
              "TableStyleMedium8")

    ws.sheet_properties.tabColor = P["gold"]


# ─────────────────────────────────────────────────────────────────────
# ASSEMBLE WORKBOOK
# ─────────────────────────────────────────────────────────────────────

def build_workbook() -> Workbook:
    wb = Workbook()
    build_welcome(wb)
    build_budget_dashboard(wb)
    build_budget_detail(wb)
    build_guest_list(wb)
    build_vendors(wb)
    build_timeline(wb)
    build_checklist(wb)
    build_bridal_party(wb)
    build_seating(wb)
    build_registry(wb)
    build_honeymoon(wb)
    return wb


def main() -> None:
    out = Path("output")
    out.mkdir(exist_ok=True)
    path = out / "Bold_Balanced_Wedding_Bible_GoogleSheets.xlsx"

    print("Building Google Sheets planner …")
    wb = build_workbook()
    wb.save(path)
    print(f"  ✓ Saved: {path}")
    print("\nDone! Upload to Google Drive → right-click → Open with Google Sheets.")


if __name__ == "__main__":
    main()
