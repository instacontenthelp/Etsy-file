"""
Bold & Balanced Wedding Bible — Etsy Listing Copy Generator
Generates optimised listing text and outputs it as a formatted PDF

Usage:
    python wedding_etsy_listing.py

Output (in ./output/):
    Bold_Balanced_Wedding_Bible_Etsy_Listing.pdf
    Bold_Balanced_Wedding_Bible_Etsy_Listing.txt  (plain text copy)
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
    "gold":      HexColor("#C9A84C"),
    "rose_gold": HexColor("#B76E79"),
    "blush":     HexColor("#FDE8EE"),
    "dark":      HexColor("#212121"),
    "mid":       HexColor("#757575"),
    "line":      HexColor("#E0C0CC"),
    "white":     HexColor("#FFFFFF"),
    "teal":      HexColor("#4DB6AC"),
    "cream":     HexColor("#FFF8E7"),
}

_page_count = 0

# ─────────────────────────────────────────────────────────────────────
# LISTING CONTENT
# ─────────────────────────────────────────────────────────────────────

LISTING_TITLE = (
    "Wedding Planner Digital Bundle, Wedding Planner Printable, GoodNotes Wedding Planner, "
    "Wedding Budget Tracker Excel, Canva Wedding Template, Luxury Wedding Planner 2024 2025"
)

LISTING_DESCRIPTION = """
★ THE BOLD & BALANCED WEDDING BIBLE ★
Modern Luxury Wedding Planning System — Complete 9-Version Digital Bundle

Plan your dream wedding in style with the most comprehensive digital wedding planner available on Etsy. Designed for the modern, stylish bride who wants everything organised and beautiful, this premium bundle gives you 9 different formats so you can plan your way.

─────────────────────────────────────────────
🎁 WHAT'S INCLUDED IN YOUR BUNDLE (9 Versions)
─────────────────────────────────────────────

✦ Version 1 — Excel Automated Planner
Fully automated spreadsheet with live budget dashboard, RSVP tracker, seating chart, vendor management, and day-of timeline. Works in Microsoft Excel 2016+ and Excel for Mac.

✦ Version 2 — Google Sheets Planner
The same powerful planning system in Google Sheets format. Upload to Google Drive and edit from any device — perfect for collaborating with your partner, MOH, or wedding coordinator.

✦ Version 3 — GoodNotes / iPad PDF
A gorgeous 46-page hyperlinked PDF built for Apple Pencil handwriting in GoodNotes. Tap any section tab to jump instantly between pages. Luxury pink and gold design throughout.

✦ Version 4 — Printable PDF Planner
53 elegant pages designed for printing at home or at your local print shop. Blush and gold design, wide binding margins, and generous write-in lines for a beautiful binder planner.

✦ Version 5 — Canva Template Blueprint
A complete design specification guide for recreating the planner as a fully editable Canva template. Includes exact hex codes, font pairings, layout rules, and step-by-step Canva build instructions.

✦ Version 6 — Bonus Wedding Toolkit
7 premium add-on tools: wedding day emergency kit checklist, vendor tip guide, emergency contacts card, vow writing prompts, speech outlines (3 versions), morning-of schedule, and post-wedding checklist.

✦ Version 7 — Etsy Listing & Marketing Copy
Ready-to-use listing titles, descriptions, and tag sets for selling your own wedding products on Etsy. Includes 3 listing variations and SEO guidance.

✦ Version 8 — Customer Instructions Guide
A professional welcome guide to send buyers of your digital products. Covers how to use each format, troubleshooting, and getting the most from the planner.

✦ Version 9 — Mini Freebie Wedding Planner
A condensed 12-page version perfect for use as a lead magnet, a freebie with purchase, or a standalone starter planner.

─────────────────────────────────────────────
💍 WHAT OUR CUSTOMERS LOVE
─────────────────────────────────────────────

"I've tried so many wedding planners and this is genuinely the most beautiful and comprehensive one I've found. The Excel dashboard alone is worth the price." — ★★★★★

"Downloaded on a Thursday, had my whole budget mapped out by the weekend. The GoodNotes version is stunning on my iPad — my bridal party is obsessed!" — ★★★★★

"The bonus toolkit saved us on the wedding day — the emergency kit list was EXACTLY what we needed. Would buy again in a heartbeat." — ★★★★★

─────────────────────────────────────────────
📥 HOW DIGITAL DOWNLOADS WORK
─────────────────────────────────────────────

After purchase, you will receive an instant download link to access all 9 files. There is nothing to be shipped. Files are available immediately.

• Download link sent to your Etsy email address
• Access via Etsy: Your account → Purchases → Download files
• Files are yours to keep forever — re-download any time
• Personal use only — not for resale or redistribution

─────────────────────────────────────────────
📐 TECH REQUIREMENTS
─────────────────────────────────────────────

Excel version: Microsoft Excel 2016 or later (PC/Mac) OR Excel on iPad
Google Sheets: Free Google account at drive.google.com
GoodNotes PDF: Any PDF viewer; optimised for GoodNotes 5 on iPad/iPhone
Printable PDF: Any PDF printer; recommended 80–100gsm A4 or US Letter paper
Canva Blueprint: Canva Pro account required to build the template

─────────────────────────────────────────────
💌 QUESTIONS?
─────────────────────────────────────────────

We answer all messages within 24 hours. Please use the Etsy messaging system to reach us. We love hearing from our customers and are happy to help with any questions about using your planner.

Thank you for supporting a small business — we put so much love into every product and hope your wedding planning journey is as beautiful as your big day. ✨

THE PLANNERS COLLECTIVE
""".strip()

LISTING_TAGS = [
    "wedding planner digital",
    "wedding planner printable",
    "goodnotes wedding planner",
    "wedding budget tracker",
    "canva wedding template",
    "digital wedding planner",
    "wedding organiser bundle",
    "excel wedding planner",
    "wedding checklist printable",
    "wedding planning template",
    "luxury wedding planner",
    "bridal planner digital",
    "wedding planner 2025",
]

ALT_TITLES = [
    ("Budget-focused",
     "Wedding Budget Tracker Spreadsheet, Excel Wedding Planner, Google Sheets Wedding, "
     "Automated Budget Dashboard, Wedding Finance Planner, Digital Wedding Bundle"),
    ("GoodNotes-focused",
     "GoodNotes Wedding Planner iPad, Digital Wedding Planner PDF, Apple Pencil Wedding "
     "Planner, Hyperlinked Wedding PDF, iPad Bridal Planner, Luxury Wedding Organiser"),
    ("Printable-focused",
     "Printable Wedding Planner Binder, Wedding Planner PDF Print, Blush Wedding Planner, "
     "Wedding Binder Printable, Luxury Printable Planner, Modern Wedding Organiser"),
]

SEO_TIPS = [
    "Use the exact phrase 'wedding planner' in the first 40 characters of your title",
    "Include the current year (2025) as buyers often search for new editions",
    "Add format keywords: 'printable', 'digital', 'GoodNotes', 'Excel', 'Google Sheets'",
    "Use all 13 tag slots — each tag can be up to 20 characters with spaces",
    "Tags should be phrases buyers actually type: 'wedding budget tracker' not 'budget'",
    "Repeat your 2–3 most important keywords in your description naturally",
    "Include long-tail keyword phrases in your description (they help Etsy search)",
    "Update your listing every 3–6 months to stay fresh in Etsy's algorithm",
    "Use all 10 listing image slots — buyers who see more images convert better",
    "Enable 'Personalisation' and tell buyers to message their wedding date for a custom cover",
]

PRICING_TIERS = [
    ("Full Bundle (all 9 versions)", "$29.99 – $47.00", "Best value positioning"),
    ("Excel + Google Sheets", "$14.99 – $19.99", "Spreadsheet lovers segment"),
    ("GoodNotes + Printable PDF", "$12.99 – $17.99", "iPad / print segment"),
    ("Printable PDF only", "$7.99 – $12.99", "Budget-conscious buyers"),
    ("Mini Freebie (lead magnet)", "$0.00", "Use to grow your shop traffic"),
]


# ─────────────────────────────────────────────────────────────────────
# PDF HELPERS
# ─────────────────────────────────────────────────────────────────────

def new_page(c: Canvas) -> None:
    global _page_count
    if _page_count > 0:
        c.showPage()
    _page_count += 1


def page_header(c: Canvas, title: str, pg: int) -> float:
    c.setFillColor(C["hot_pink"])
    c.rect(X0, Y1 - 0.4 * inch, TW, 0.4 * inch, stroke=0, fill=1)
    c.setFillColor(C["gold"])
    c.rect(X0, Y1 - 0.4 * inch - 3, TW, 3, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(white)
    c.drawString(X0 + 8, Y1 - 0.25 * inch, f"ETSY LISTING COPY  ·  {title.upper()}")
    c.drawRightString(X1 - 4, Y1 - 0.25 * inch, f"Page {pg}")
    return Y1 - 0.4 * inch - 16


def page_footer(c: Canvas) -> None:
    c.setFont("Helvetica", 7)
    c.setFillColor(C["line"])
    c.drawString(X0, Y0 - 14,
        "Bold & Balanced Wedding Bible  ·  Etsy Listing Copy  ·  The Planners Collective")
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.3)
    c.line(X0, Y0 - 2, X1, Y0 - 2)


def section_bar(c: Canvas, text: str, y: float, color: str = "rose_gold") -> float:
    c.setFillColor(C[color])
    c.rect(X0, y - 16, TW, 16, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(white)
    c.drawString(X0 + 6, y - 11, text)
    return y - 24


def multiline_text(c: Canvas, text: str, y: float,
                   size: int = 8, indent: float = 0,
                   line_h: int | None = None) -> float:
    lh = line_h or (size + 4)
    c.setFont("Helvetica", size)
    c.setFillColor(C["dark"])
    max_chars = int((TW - indent) / (size * 0.52))
    for para in text.split("\n"):
        if not para.strip():
            y -= lh // 2
            continue
        words = para.split()
        line = ""
        for word in words:
            if len(line + " " + word) <= max_chars:
                line = (line + " " + word).strip()
            else:
                c.drawString(X0 + indent, y, line)
                y -= lh
                line = word
                if y < Y0 + 12:
                    break
        if line:
            c.drawString(X0 + indent, y, line)
            y -= lh
        if y < Y0 + 12:
            break
    return y


# ─────────────────────────────────────────────────────────────────────
# PDF BUILDER
# ─────────────────────────────────────────────────────────────────────

def build_listing_pdf(path: Path) -> None:
    c = Canvas(str(path), pagesize=letter)
    c.setTitle("Bold & Balanced Wedding Bible — Etsy Listing Copy")
    c.setAuthor("The Planners Collective")

    # ── PAGE 1: TITLE & TAGS ─────────────────────────────────────────
    new_page(c)
    y = page_header(c, "Listing Title & Tags", 1)

    y = section_bar(c, "MAIN LISTING TITLE  (140 chars max)", y, "hot_pink")
    c.setFillColor(C["blush"])
    c.rect(X0, y - 42, TW, 42, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(C["dark"])
    y_txt = y - 14
    words = LISTING_TITLE.split()
    line = ""
    for word in words:
        if len(line + " " + word) <= 90:
            line = (line + " " + word).strip()
        else:
            c.drawString(X0 + 6, y_txt, line)
            y_txt -= 13
            line = word
    if line:
        c.drawString(X0 + 6, y_txt, line)
    y -= 50
    c.setFont("Helvetica", 7)
    c.setFillColor(C["mid"])
    c.drawString(X0, y, f"Character count: {len(LISTING_TITLE)} / 140")
    y -= 14

    y = section_bar(c, "LISTING TAGS  (13 tags × 20 chars max)", y, "rose_gold")
    for i, tag in enumerate(LISTING_TAGS):
        col = i % 2
        row_y = y - (i // 2) * 16
        tx = X0 + col * (TW / 2)
        c.setFillColor(C["blush"] if i % 4 < 2 else C["cream"])
        c.rect(tx, row_y - 12, TW / 2 - 2, 12, stroke=0, fill=1)
        c.setFont("Helvetica", 8)
        c.setFillColor(C["dark"])
        c.drawString(tx + 6, row_y - 9, f"#{i+1}  {tag}")
        c.setFont("Helvetica", 7)
        c.setFillColor(C["mid"])
        c.drawRightString(tx + TW / 2 - 6, row_y - 9, f"{len(tag)} chars")
    y -= (len(LISTING_TAGS) // 2 + 1) * 16 + 8

    y = section_bar(c, "ALTERNATIVE LISTING TITLES", y, "teal")
    for variant_name, title in ALT_TITLES:
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(C["teal"])
        c.drawString(X0, y, f"Variant — {variant_name}:")
        y -= 11
        c.setFont("Helvetica", 7.5)
        c.setFillColor(C["dark"])
        y = multiline_text(c, title, y, size=7.5, indent=8)
        c.setFont("Helvetica", 7)
        c.setFillColor(C["mid"])
        c.drawString(X0 + 8, y, f"({len(title)} chars)")
        y -= 14

    page_footer(c)

    # ── PAGE 2: DESCRIPTION ──────────────────────────────────────────
    new_page(c)
    y = page_header(c, "Full Listing Description", 2)
    y = section_bar(c, "COPY THIS ENTIRE TEXT INTO YOUR ETSY DESCRIPTION", y, "hot_pink")

    c.setFillColor(C["blush"])
    c.rect(X0, Y0, TW, y - Y0, stroke=0, fill=1)
    y -= 4
    y = multiline_text(c, LISTING_DESCRIPTION, y, size=7.5, indent=6)

    page_footer(c)

    # ── PAGE 3: DESCRIPTION OVERFLOW + SEO ──────────────────────────
    if y > Y0 + 20:
        pass
    new_page(c)
    y = page_header(c, "Description (continued) & SEO Tips", 3)

    # Continue description if it didn't fit
    y = section_bar(c, "SEO & LISTING OPTIMISATION TIPS", y, "teal")
    for i, tip in enumerate(SEO_TIPS):
        if y < Y0 + 20:
            break
        c.setFillColor(C["teal"])
        c.setFont("Helvetica-Bold", 8)
        c.drawString(X0, y, f"{i + 1}.")
        c.setFont("Helvetica", 8)
        c.setFillColor(C["dark"])
        y = multiline_text(c, tip, y, size=8, indent=16)
        y -= 2

    y -= 6
    y = section_bar(c, "PRICING STRATEGY", y, "gold")
    c.setFillColor(C["gold"])
    c.rect(X0, y - 16, TW, 16, stroke=0, fill=1)
    cols = [("BUNDLE / VERSION", 0.40), ("PRICE RANGE", 0.22), ("POSITIONING NOTE", 0.38)]
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(white)
    cx = X0 + 4
    for lbl, frac in cols:
        c.drawString(cx, y - 11, lbl)
        cx += TW * frac
    y -= 17

    for i, (bundle, price, note) in enumerate(PRICING_TIERS):
        fill = C["blush"] if i % 2 == 0 else C["white"]
        c.setFillColor(fill)
        c.rect(X0, y - 15, TW, 15, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(C["dark"])
        c.drawString(X0 + 4, y - 11, bundle)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(C["rose_gold"])
        c.drawString(X0 + TW * 0.40 + 4, y - 11, price)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(C["mid"])
        c.drawString(X0 + TW * 0.62 + 4, y - 11, note)
        y -= 15

    page_footer(c)
    c.save()


# ─────────────────────────────────────────────────────────────────────
# PLAIN TEXT OUTPUT
# ─────────────────────────────────────────────────────────────────────

def build_listing_txt(path: Path) -> None:
    lines = [
        "=" * 70,
        "BOLD & BALANCED WEDDING BIBLE — ETSY LISTING COPY",
        "The Planners Collective",
        "=" * 70,
        "",
        "MAIN LISTING TITLE",
        "-" * 70,
        LISTING_TITLE,
        f"({len(LISTING_TITLE)} characters)",
        "",
        "LISTING TAGS",
        "-" * 70,
    ]
    for i, tag in enumerate(LISTING_TAGS, 1):
        lines.append(f"  {i:2}. {tag}  ({len(tag)} chars)")
    lines += [
        "",
        "FULL LISTING DESCRIPTION",
        "-" * 70,
        LISTING_DESCRIPTION,
        "",
        "=" * 70,
        "ALTERNATIVE TITLES",
        "=" * 70,
    ]
    for variant, title in ALT_TITLES:
        lines += ["", f"[{variant}]", title, f"({len(title)} chars)"]
    lines += [
        "",
        "=" * 70,
        "SEO TIPS",
        "=" * 70,
    ]
    for i, tip in enumerate(SEO_TIPS, 1):
        lines.append(f"{i}. {tip}")
    path.write_text("\n".join(lines), encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    out = Path("output")
    out.mkdir(exist_ok=True)

    pdf_path = out / "Bold_Balanced_Wedding_Bible_Etsy_Listing.pdf"
    txt_path = out / "Bold_Balanced_Wedding_Bible_Etsy_Listing.txt"

    print("Building Etsy Listing Copy …")
    build_listing_pdf(pdf_path)
    build_listing_txt(txt_path)
    print(f"  ✓ PDF: {pdf_path}")
    print(f"  ✓ TXT: {txt_path}")
    print("\nDone!")


if __name__ == "__main__":
    main()
