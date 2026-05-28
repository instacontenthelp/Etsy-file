"""
Bold & Balanced Wedding Bible — Customer Instructions Guide
A professional welcome guide to include with each Etsy order

Usage:
    pip install reportlab
    python wedding_customer_guide.py

Output (in ./output/):
    Bold_Balanced_Wedding_Bible_Customer_Guide.pdf
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
    "teal":      HexColor("#4DB6AC"),
    "cream":     HexColor("#FFF8E7"),
    "green":     HexColor("#66BB6A"),
    "light_green":HexColor("#E8F5E9"),
}

_pg = 0


def new_page(c: Canvas) -> None:
    global _pg
    if _pg > 0:
        c.showPage()
    _pg += 1


def page_header(c: Canvas, title: str) -> float:
    global _pg
    c.setFillColor(C["hot_pink"])
    c.rect(X0, Y1 - 0.4 * inch, TW, 0.4 * inch, stroke=0, fill=1)
    c.setFillColor(C["gold"])
    c.rect(X0, Y1 - 0.4 * inch - 3, TW, 3, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(white)
    c.drawString(X0 + 8, Y1 - 0.26 * inch,
                 f"BOLD & BALANCED WEDDING BIBLE  ·  {title.upper()}")
    c.drawRightString(X1 - 4, Y1 - 0.26 * inch, f"Page {_pg}")
    return Y1 - 0.4 * inch - 16


def page_footer(c: Canvas) -> None:
    c.setFont("Helvetica", 7)
    c.setFillColor(C["line"])
    c.drawString(X0, Y0 - 14,
        "Bold & Balanced Wedding Bible  ·  Marigold Bride  ·  hello@marigoldbride.com")
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.3)
    c.line(X0, Y0 - 2, X1, Y0 - 2)


def section_bar(c: Canvas, text: str, y: float, color: str = "rose_gold") -> float:
    c.setFillColor(C[color])
    c.rect(X0, y - 18, TW, 18, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(white)
    c.drawString(X0 + 8, y - 12, text)
    return y - 26


def heading(c: Canvas, text: str, y: float, size: int = 10) -> float:
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(C["rose_gold"])
    c.drawString(X0, y, text)
    c.setStrokeColor(C["gold"])
    c.setLineWidth(0.5)
    c.line(X0, y - 3, X1, y - 3)
    return y - 16


def body(c: Canvas, text: str, y: float, indent: float = 0,
         size: int = 8.5) -> float:
    c.setFont("Helvetica", size)
    c.setFillColor(C["dark"])
    max_chars = int((TW - indent) / (size * 0.52))
    for para in text.split("\n"):
        if not para.strip():
            y -= 6
            continue
        words = para.split()
        line = ""
        for word in words:
            if len(line + " " + word) <= max_chars:
                line = (line + " " + word).strip()
            else:
                c.drawString(X0 + indent, y, line)
                y -= size + 4
                line = word
        if line:
            c.drawString(X0 + indent, y, line)
            y -= size + 4
    return y


def step(c: Canvas, num: int, text: str, y: float) -> float:
    c.setFillColor(C["hot_pink"])
    c.circle(X0 + 8, y - 4, 8, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(white)
    c.drawCentredString(X0 + 8, y - 8, str(num))
    c.setFont("Helvetica", 8.5)
    c.setFillColor(C["dark"])
    return body(c, text, y, indent=22, size=8.5)


def info_box(c: Canvas, text: str, y: float,
             fill: str = "light_gold", height: float = 30) -> float:
    c.setFillColor(C[fill])
    c.rect(X0, y - height, TW, height, stroke=0, fill=1)
    c.setStrokeColor(C["gold"])
    c.setLineWidth(0.5)
    c.rect(X0, y - height, TW, height, fill=0)
    c.setFont("Helvetica", 8.5)
    c.setFillColor(C["dark"])
    y2 = y - 10
    for para in text.split("\n"):
        if para.strip():
            c.drawString(X0 + 8, y2, para)
            y2 -= 12
    return y - height - 8


# ─────────────────────────────────────────────────────────────────────
# COVER
# ─────────────────────────────────────────────────────────────────────

def build_cover(c: Canvas) -> None:
    new_page(c)
    c.setFillColor(C["blush"])
    c.rect(0, 0, W, H, stroke=0, fill=1)

    c.setFillColor(C["gold"])
    c.rect(0, H - 1.1 * inch, W, 1.1 * inch, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(white)
    c.drawCentredString(W / 2, H - 0.45 * inch,
                        "THE PLANNERS COLLECTIVE")

    # Main content
    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(C["dark"])
    t = "Welcome!"
    tw = c.stringWidth(t, "Helvetica-Bold", 28)
    c.drawString((W - tw) / 2, H * 0.73, t)

    c.setFont("Helvetica", 12)
    c.setFillColor(C["rose_gold"])
    sub = "Thank you for your purchase"
    sw = c.stringWidth(sub, "Helvetica", 12)
    c.drawString((W - sw) / 2, H * 0.67, sub)

    c.setStrokeColor(C["gold"])
    c.setLineWidth(1.2)
    c.line(W * 0.2, H * 0.65, W * 0.8, H * 0.65)

    # Welcome message box
    box_y = H * 0.57
    c.setFillColor(white)
    c.roundRect(M, box_y - H * 0.2, TW, H * 0.2, 8, stroke=0, fill=1)
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.8)
    c.roundRect(M, box_y - H * 0.2, TW, H * 0.2, 8, fill=0)

    msg = (
        "Congratulations on your engagement!\n\n"
        "You've just downloaded the Bold & Balanced Wedding Bible — "
        "the most comprehensive digital wedding planning system on Etsy. "
        "This guide will walk you through exactly how to use every version "
        "included in your bundle so you can start planning your dream wedding "
        "with confidence.\n\n"
        "If you need any help at all, please don't hesitate to message us "
        "on Etsy — we typically respond within 24 hours and love hearing "
        "from our customers!"
    )
    c.setFont("Helvetica", 8.5)
    c.setFillColor(C["dark"])
    my = box_y - 14
    for line in msg.split("\n"):
        if not line.strip():
            my -= 5
            continue
        words = line.split()
        ln = ""
        for word in words:
            if len(ln + " " + word) <= 88:
                ln = (ln + " " + word).strip()
            else:
                c.drawString(M + 12, my, ln)
                my -= 12
                ln = word
        if ln:
            c.drawString(M + 12, my, ln)
            my -= 12

    # Product name badge
    c.setFillColor(C["hot_pink"])
    c.rect(0, 0, W, 0.55 * inch, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(white)
    label = "Bold & Balanced Wedding Bible  ·  Customer Guide"
    lw = c.stringWidth(label, "Helvetica-Bold", 11)
    c.drawString((W - lw) / 2, 0.18 * inch, label)


# ─────────────────────────────────────────────────────────────────────
# HOW TO ACCESS YOUR FILES
# ─────────────────────────────────────────────────────────────────────

def build_download_guide(c: Canvas) -> None:
    new_page(c)
    y = page_header(c, "Accessing Your Files")

    y = section_bar(c, "HOW TO DOWNLOAD YOUR FILES", y, "hot_pink")
    for i, instruction in enumerate([
        "Check your Etsy email for a message with your purchase confirmation.",
        "Click the link in the email OR go to Etsy.com → Account → Purchases and reviews.",
        "Find this order and click 'Download files'.",
        "All 9 files will appear as individual download links. Click each one.",
        "Save each file to a folder on your device (e.g. 'My Wedding Planner').",
        "That's it! Your files are yours to keep forever — re-download any time.",
    ], 1):
        y = step(c, i, instruction, y)
        y -= 4

    y -= 8
    y = info_box(c,
        "TIP: Save your files to Google Drive, iCloud, or Dropbox so you can "
        "access them from any device at any time.",
        y, fill="light_gold", height=28)

    y -= 4
    y = section_bar(c, "WHAT'S IN YOUR DOWNLOAD (9 FILES)", y, "rose_gold")
    files = [
        ("Version 1", "Bold_Balanced_Wedding_Bible_Excel.xlsx",
         "Microsoft Excel automated planner"),
        ("Version 2", "Bold_Balanced_Wedding_Bible_GoogleSheets.xlsx",
         "Google Sheets version — upload to Google Drive"),
        ("Version 3", "Bold_Balanced_Wedding_Bible_GoodNotes_Letter.pdf",
         "GoodNotes iPad PDF — US Letter (8.5×11\")"),
        ("Version 3B", "Bold_Balanced_Wedding_Bible_GoodNotes_A4.pdf",
         "GoodNotes iPad PDF — A4"),
        ("Version 4", "Bold_Balanced_Wedding_Bible_Printable_Letter.pdf",
         "Printable PDF — US Letter (8.5×11\")"),
        ("Version 4B", "Bold_Balanced_Wedding_Bible_Printable_A4.pdf",
         "Printable PDF — A4"),
        ("Version 5", "Bold_Balanced_Wedding_Bible_Canva_Blueprint.pdf",
         "Canva template design guide"),
        ("Version 6", "Bold_Balanced_Wedding_Bible_Bonus_Toolkit.pdf",
         "Bonus toolkit — emergency kit, tip guide, vows, speeches"),
        ("Version 7", "Bold_Balanced_Wedding_Bible_Etsy_Listing.pdf/.txt",
         "Etsy listing copy and marketing guide"),
        ("Version 8", "Bold_Balanced_Wedding_Bible_Customer_Guide.pdf",
         "This file — customer instructions"),
        ("Version 9", "Bold_Balanced_Wedding_Bible_Mini_Freebie.pdf",
         "Mini starter planner — perfect for gifting"),
    ]
    for ver, filename, desc in files:
        row_y = y
        c.setFillColor(C["blush"] if files.index((ver, filename, desc)) % 2 == 0
                       else C["white"])
        c.rect(X0, row_y - 16, TW, 16, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(C["hot_pink"])
        c.drawString(X0 + 4, row_y - 11, ver)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(C["dark"])
        c.drawString(X0 + 60, row_y - 11, filename[:40])
        c.setFont("Helvetica", 7)
        c.setFillColor(C["mid"])
        c.drawString(X0 + 310, row_y - 11, desc[:52])
        y -= 16

    page_footer(c)


# ─────────────────────────────────────────────────────────────────────
# EXCEL GUIDE
# ─────────────────────────────────────────────────────────────────────

def build_excel_guide(c: Canvas) -> None:
    new_page(c)
    y = page_header(c, "Excel Planner Guide")

    y = section_bar(c, "VERSION 1: EXCEL AUTOMATED PLANNER", y, "hot_pink")
    y = body(c,
        "The Excel planner is a fully automated spreadsheet with live formulas, "
        "data validation dropdowns, conditional formatting, and budget charts. "
        "Here is how to get started.", y)
    y -= 6

    y = heading(c, "REQUIREMENTS", y)
    for req in [
        "Microsoft Excel 2016 or later (PC or Mac)",
        "Excel for iPad / iPhone (via Microsoft 365 app)",
        "NOT compatible with Numbers, LibreOffice, or OpenOffice",
    ]:
        c.setFont("Helvetica", 8.5)
        c.setFillColor(C["dark"])
        c.drawString(X0 + 16, y, f"•  {req}")
        y -= 13
    y -= 4

    y = heading(c, "GETTING STARTED — STEP BY STEP", y)
    steps_excel = [
        "Open the file: double-click 'Bold_Balanced_Wedding_Bible_Excel.xlsx'",
        "If prompted to 'Enable Editing', click the yellow banner at the top",
        "If prompted about macros, click 'Enable Content'",
        "Start on the 🏠 Welcome sheet — fill in your names, date, and venue",
        "Navigate between sheets using the tabs at the bottom of Excel",
        "Begin with 💍 Budget Detail — enter your budget items and amounts",
        "Watch the 📊 Budget Dashboard update automatically as you type",
        "Use 👥 Guest List to track invitations, RSVPs, and meal choices",
        "Fill in 🏢 Vendor Tracker with your confirmed supplier details",
        "The ⏰ Day-of Timeline comes pre-filled — customise for your day",
        "Print any sheet: File → Print, ensure 'Fit to page' is selected",
    ]
    for i, s in enumerate(steps_excel, 1):
        y = step(c, i, s, y)
        y -= 3

    y -= 6
    y = heading(c, "COMMON QUESTIONS", y)
    faqs = [
        ("The formulas show #REF! errors",
         "Ensure you haven't deleted any column headers. If so, re-download the file."),
        ("Drop-down menus don't appear",
         "This usually means macros are disabled. Click 'Enable Content' in the yellow bar."),
        ("The Budget Dashboard shows $0",
         "Enter your budget items in the 💍 Budget Detail sheet first."),
        ("Conditional formatting colours aren't showing",
         "Go to File → Info → Inspect Document and ensure you are in Edit mode."),
        ("The file won't open on my Mac",
         "Ensure you have Microsoft Excel installed. Numbers will not preserve all formatting."),
    ]
    for q, a in faqs:
        if y < Y0 + 30:
            break
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(C["rose_gold"])
        c.drawString(X0, y, f"Q: {q}")
        y -= 12
        c.setFont("Helvetica", 8)
        c.setFillColor(C["dark"])
        y = body(c, f"A: {a}", y, indent=12, size=8)
        y -= 6

    page_footer(c)


# ─────────────────────────────────────────────────────────────────────
# GOOGLE SHEETS GUIDE
# ─────────────────────────────────────────────────────────────────────

def build_sheets_guide(c: Canvas) -> None:
    new_page(c)
    y = page_header(c, "Google Sheets Guide")

    y = section_bar(c, "VERSION 2: GOOGLE SHEETS PLANNER", y, "teal")
    y = body(c,
        "The Google Sheets version works exactly like the Excel planner but lives "
        "in your Google Drive, so you can edit from any device and collaborate with "
        "your partner, MOH, or wedding coordinator in real time.", y)
    y -= 6

    y = heading(c, "HOW TO OPEN IN GOOGLE SHEETS", y)
    for i, s in enumerate([
        "Sign in to your Google account at drive.google.com",
        "Click the '+' button → 'File upload'",
        "Select 'Bold_Balanced_Wedding_Bible_GoogleSheets.xlsx' from your downloads",
        "Wait for the upload to complete",
        "Right-click the uploaded file → 'Open with' → 'Google Sheets'",
        "Google Sheets will convert the file — this takes about 10 seconds",
        "Click 'File → Save as Google Sheets' to save as a native Sheets file",
        "You can now edit from any device by going to drive.google.com",
        "Share with your partner: click 'Share' (top right) → enter their email",
    ], 1):
        y = step(c, i, s, y)
        y -= 3

    y -= 6
    y = info_box(c,
        "COLLABORATION TIP: Share the file with your wedding coordinator or MOH "
        "and set them as 'Editor' so they can update vendor details, "
        "RSVPs, and the timeline in real time.",
        y, fill="light_gold", height=36)

    y -= 4
    y = heading(c, "GOOGLE SHEETS — KNOWN DIFFERENCES FROM EXCEL", y)
    diffs = [
        "Drop-down menus: work identically — click any cell in a dropdown column",
        "Conditional formatting (colour-coding): fully preserved",
        "Charts: may appear slightly different but data is correct",
        "Formulas: all SUMIF, COUNTIF, and IFERROR formulas work correctly in Sheets",
        "Printing: File → Print → adjust margins and ensure 'Fit to width' is on",
    ]
    for diff in diffs:
        if y < Y0 + 20:
            break
        c.setFont("Helvetica", 8.5)
        c.setFillColor(C["dark"])
        c.drawString(X0 + 16, y, f"•  {diff}")
        y -= 14

    page_footer(c)


# ─────────────────────────────────────────────────────────────────────
# PDF & GOODNOTES GUIDE
# ─────────────────────────────────────────────────────────────────────

def build_pdf_guide(c: Canvas) -> None:
    new_page(c)
    y = page_header(c, "GoodNotes & Printable PDF Guide")

    y = section_bar(c, "VERSION 3: GOODNOTES / iPAD PDF", y, "hot_pink")
    y = body(c,
        "The GoodNotes PDF is a 46-page hyperlinked planner designed for writing "
        "with Apple Pencil in GoodNotes 5 on iPad. The coloured tabs on the right "
        "side of every page are live hyperlinks — tap any tab to jump to that section.", y)
    y -= 6

    y = heading(c, "HOW TO IMPORT INTO GOODNOTES", y)
    for i, s in enumerate([
        "Download the PDF file to your iPad",
        "Open the Files app and find the downloaded PDF",
        "Tap and hold the file → 'Share' → 'Open in GoodNotes'",
        "OR open GoodNotes → tap '+' → 'Import' → find the PDF",
        "Select 'Import as New Notebook' (not 'Import as New Page')",
        "The planner opens with all section tabs visible on the right",
        "Tap any coloured tab to jump instantly to that section",
        "Use Apple Pencil to write in any field — your writing is automatically saved",
    ], 1):
        y = step(c, i, s, y)
        y -= 3

    y -= 6
    y = info_box(c,
        "GOODNOTES TIP: Use the 'lasso' tool to select and move your handwritten "
        "text. Tap the fingerprint icon to convert handwriting to typed text.",
        y, fill="light_gold", height=28)

    y -= 8
    y = section_bar(c, "VERSION 4: PRINTABLE PDF", y, "rose_gold")
    y = body(c,
        "The Printable PDF is a 53-page print-ready planner with a blush and gold "
        "colour scheme. Print at home on 80–100gsm paper for the best result.", y)
    y -= 6

    y = heading(c, "PRINTING INSTRUCTIONS", y)
    tips = [
        "Open the PDF in Adobe Acrobat Reader (free) or any PDF viewer",
        "Go to File → Print",
        "Set paper size to US Letter (8.5×11\") OR A4 — download whichever matches your printer",
        "Under 'Page Sizing', select 'Fit' or 'Actual Size'",
        "For a double-sided binder: select 'Double-sided, flip on long edge'",
        "Print pages 1–2 first as a test before printing the full document",
        "Recommended paper weight: 80–100gsm (24lb bond) for best writing experience",
        "To bind: punch 3 holes on the left margin (we left extra space for this)",
        "OR take to a local print shop and ask for spiral or comb binding",
    ]
    for i, tip in enumerate(tips, 1):
        if y < Y0 + 20:
            break
        y = step(c, i, tip, y)
        y -= 3

    page_footer(c)


# ─────────────────────────────────────────────────────────────────────
# TROUBLESHOOTING & CONTACT
# ─────────────────────────────────────────────────────────────────────

def build_support_page(c: Canvas) -> None:
    new_page(c)
    y = page_header(c, "Troubleshooting & Support")

    y = section_bar(c, "COMMON ISSUES & SOLUTIONS", y, "hot_pink")

    issues = [
        ("I can't find my download files",
         "Go to Etsy.com → top-right menu → 'Purchases and reviews' → find this order "
         "→ 'Download files'. Check your spam folder for the confirmation email."),
        ("The Excel file won't open",
         "Ensure you have Microsoft Excel 2016 or later. The file is NOT compatible with "
         "Apple Numbers or Google Sheets opened directly (upload via Google Drive instead)."),
        ("My GoodNotes PDF tabs don't work as hyperlinks",
         "Make sure you imported as a 'New Notebook' not a single page. The hyperlinks "
         "work in GoodNotes 5+ and any PDF viewer that supports links (PDF Expert, etc.)."),
        ("The printable PDF looks blurry when printed",
         "You may have scaled the page during printing. Set 'Page sizing' to 'Actual size' "
         "in your print dialog, not 'Fit to page' (which can compress the resolution)."),
        ("I accidentally deleted content from the Excel file",
         "Close WITHOUT saving, then re-download from Etsy. Your Etsy purchase gives you "
         "unlimited downloads — the link never expires."),
        ("The Google Sheets formulas show errors",
         "After importing to Google Sheets, some cell references may need updating. "
         "Contact us via Etsy message and we'll help you fix it within 24 hours."),
        ("I downloaded the wrong size (Letter vs A4)",
         "Both Letter and A4 versions are included in your download. Check your Etsy "
         "downloads page for the second file."),
    ]

    for q, a in issues:
        if y < Y0 + 40:
            page_footer(c)
            new_page(c)
            y = page_header(c, "Troubleshooting (continued)")

        c.setFillColor(C["blush"])
        c.rect(X0, y - 13, TW, 13, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(C["hot_pink"])
        c.drawString(X0 + 6, y - 9, f"❓  {q}")
        y -= 16
        y = body(c, f"✅  {a}", y, indent=12, size=8)
        y -= 8

    page_footer(c)

    new_page(c)
    y = page_header(c, "Contact & Licence")

    y = section_bar(c, "CONTACT US", y, "gold")
    y = body(c,
        "We are here to help! If you have any questions or run into any issues with "
        "your files, please contact us via Etsy's messaging system. We typically respond "
        "within 24 hours, Monday to Friday.", y)
    y -= 8

    for icon, label, value in [
        ("📩", "Etsy Messages:", "etsy.com/shop/MarigoldBride — click 'Message' button"),
        ("✉️", "Email:", "hello@marigoldbride.com"),
        ("⭐", "Reviews:", "We'd love a 5-star review if you're enjoying your planner!"),
    ]:
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(C["rose_gold"])
        c.drawString(X0, y, f"{icon}  {label}")
        c.setFont("Helvetica", 9)
        c.setFillColor(C["dark"])
        c.drawString(X0 + 100, y, value)
        y -= 16

    y -= 10
    y = section_bar(c, "LICENCE & USAGE TERMS", y, "rose_gold")
    licence_text = (
        "Your purchase grants you a PERSONAL USE licence for this product. "
        "This means you may:\n"
        "  ✅  Use the planner for your own wedding planning\n"
        "  ✅  Print unlimited copies for personal use\n"
        "  ✅  Share the GoodNotes / iPad PDF with your own devices\n"
        "  ✅  Re-download from Etsy as many times as you need\n\n"
        "This licence does NOT allow you to:\n"
        "  ❌  Resell, redistribute, or share the digital files with others\n"
        "  ❌  Use the files to create your own products for sale\n"
        "  ❌  Upload the files to any file-sharing service\n"
        "  ❌  Remove or alter Marigold Bride branding\n\n"
        "Thank you for respecting the work that went into creating this product. "
        "If you'd like to purchase a commercial licence or bundle licence, "
        "please contact us via Etsy."
    )
    y = body(c, licence_text, y, size=8)

    y -= 16
    # Closing message
    c.setFillColor(C["blush"])
    c.rect(X0, y - 60, TW, 60, stroke=0, fill=1)
    c.setStrokeColor(C["gold"])
    c.setLineWidth(0.8)
    c.rect(X0, y - 60, TW, 60, fill=0)
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(C["hot_pink"])
    msg = "Wishing you the most beautiful wedding day! ✨"
    mw = c.stringWidth(msg, "Helvetica-Bold", 12)
    c.drawString((W - mw) / 2, y - 18, msg)
    c.setFont("Helvetica", 9)
    c.setFillColor(C["rose_gold"])
    brand = "With love, Marigold Bride"
    bw = c.stringWidth(brand, "Helvetica", 9)
    c.drawString((W - bw) / 2, y - 34, brand)
    c.setFont("Helvetica", 8)
    c.setFillColor(C["mid"])
    sub = "hello@marigoldbride.com"
    sw = c.stringWidth(sub, "Helvetica", 8)
    c.drawString((W - sw) / 2, y - 48, sub)

    page_footer(c)


# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    out = Path("output")
    out.mkdir(exist_ok=True)
    path = out / "Bold_Balanced_Wedding_Bible_Customer_Guide.pdf"

    print("Building Customer Guide PDF …")
    c = Canvas(str(path), pagesize=letter)
    c.setTitle("Bold & Balanced Wedding Bible — Customer Guide")
    c.setAuthor("Marigold Bride")

    global _pg
    _pg = 0

    build_cover(c)
    build_download_guide(c)
    build_excel_guide(c)
    build_sheets_guide(c)
    build_pdf_guide(c)
    build_support_page(c)

    c.save()
    print(f"  ✓ Saved: {path}  ({_pg} pages)")
    print("\nDone!")


if __name__ == "__main__":
    main()
