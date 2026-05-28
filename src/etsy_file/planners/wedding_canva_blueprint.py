"""
Bold & Balanced Wedding Bible — Canva Editable Template Blueprint
Generated with Python reportlab

This document is a complete design specification and build guide for creating
the Canva template version of the Bold & Balanced Wedding Bible. It covers:
  - Canva page-by-page layout specifications
  - Exact hex colour values and font pairings
  - Element dimensions and spacing rules
  - Instructions for making elements editable
  - How to share as a Canva template link for Etsy delivery

Usage:
    pip install reportlab
    python wedding_canva_blueprint.py

Output (in ./output/):
    Bold_Balanced_Wedding_Bible_Canva_Blueprint.pdf
"""

from __future__ import annotations

from pathlib import Path

from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas

W, H = letter   # 8.5 × 11 inches

C = {
    "hot_pink":   HexColor("#E91E8C"),
    "pink":       HexColor("#F48FB1"),
    "blush":      HexColor("#FDE8EE"),
    "gold":       HexColor("#C9A84C"),
    "light_gold": HexColor("#FFF9C4"),
    "rose_gold":  HexColor("#B76E79"),
    "dark":       HexColor("#212121"),
    "mid":        HexColor("#5D4037"),
    "light_gray": HexColor("#F5F5F5"),
    "border":     HexColor("#E0C0CC"),
    "white":      HexColor("#FFFFFF"),
    "teal":       HexColor("#4DB6AC"),
    "cream":      HexColor("#FFF8E7"),
    "section_bg": HexColor("#FCE4EC"),
}

M  = 0.65 * inch   # outer margin
TW = W - 2 * M     # text width
X0 = M
X1 = W - M
Y0 = 0.55 * inch
Y1 = H - 0.55 * inch

# ─────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────

def new_page(c: Canvas) -> None:
    c.showPage()


def title_bar(c: Canvas, text: str, y: float, fill: HexColor,
              text_color: HexColor = white) -> None:
    c.setFillColor(fill)
    c.rect(X0, y - 4, TW, 22, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(text_color)
    c.drawString(X0 + 8, y + 4, text)


def section_heading(c: Canvas, text: str, y: float) -> None:
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(C["hot_pink"])
    c.drawString(X0, y, text)
    c.setStrokeColor(C["gold"])
    c.setLineWidth(0.6)
    c.line(X0, y - 3, X1, y - 3)


def body(c: Canvas, text: str, y: float, indent: float = 0,
         size: int = 8, color: str = "dark") -> float:
    c.setFont("Helvetica", size)
    c.setFillColor(C[color])
    # word-wrap at ~95 chars
    words = text.split()
    line = ""
    max_w = TW - indent - 6
    char_w = size * 0.52
    max_chars = int(max_w / char_w)
    lines = []
    for word in words:
        if len(line) + len(word) + 1 <= max_chars:
            line = (line + " " + word).strip()
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    for ln in lines:
        c.drawString(X0 + indent, y, ln)
        y -= 13
    return y


def bullet(c: Canvas, text: str, y: float, indent: float = 12) -> float:
    c.setFont("Helvetica", 8)
    c.setFillColor(C["rose_gold"])
    c.drawString(X0 + indent - 8, y, "•")
    c.setFillColor(C["dark"])
    return body(c, text, y, indent=indent)


def kv(c: Canvas, key: str, value: str, y: float,
       key_w: float = 140) -> float:
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(C["rose_gold"])
    c.drawString(X0, y, key)
    c.setFont("Helvetica", 8)
    c.setFillColor(C["dark"])
    c.drawString(X0 + key_w, y, value)
    return y - 13


def color_swatch(c: Canvas, hex_code: str, label: str,
                 x: float, y: float) -> None:
    c.setFillColor(HexColor(hex_code))
    c.rect(x, y, 30, 18, stroke=0, fill=1)
    c.setStrokeColor(C["border"])
    c.setLineWidth(0.4)
    c.rect(x, y, 30, 18, fill=0)
    c.setFont("Helvetica", 6.5)
    c.setFillColor(C["dark"])
    c.drawString(x, y - 10, f"{label}")
    c.drawString(x, y - 19, hex_code)


def page_header(c: Canvas, page_title: str, page_num: int) -> float:
    # top bar
    c.setFillColor(C["hot_pink"])
    c.rect(0, H - 0.42 * inch, W, 0.42 * inch, stroke=0, fill=1)
    c.setFillColor(C["gold"])
    c.rect(0, H - 0.42 * inch - 3, W, 3, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(white)
    c.drawString(M, H - 0.28 * inch, "Bold & Balanced Wedding Bible  —  Canva Template Blueprint")
    c.setFont("Helvetica", 9)
    c.drawRightString(X1, H - 0.28 * inch, f"Page {page_num}")
    # page title
    y = Y1 - 14
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(C["dark"])
    c.drawString(X0, y, page_title)
    c.setStrokeColor(C["gold"])
    c.setLineWidth(1)
    y -= 6
    c.line(X0, y, X1, y)
    return y - 14


def page_footer(c: Canvas) -> None:
    c.setFont("Helvetica", 7)
    c.setFillColor(C["border"])
    c.drawString(X0, Y0 - 10,
        "© Marigold Bride  ·  For internal use and Canva template development only")
    c.setStrokeColor(C["border"])
    c.setLineWidth(0.3)
    c.line(X0, Y0 - 2, X1, Y0 - 2)


# ─────────────────────────────────────────────────────────────────────
# PAGE BUILDERS
# ─────────────────────────────────────────────────────────────────────

def build_cover_page(c: Canvas) -> None:
    # Full blush background
    c.setFillColor(C["blush"])
    c.rect(0, 0, W, H, stroke=0, fill=1)

    # Gold top stripe
    c.setFillColor(C["gold"])
    c.rect(0, H - 1.1 * inch, W, 1.1 * inch, stroke=0, fill=1)

    # Main title block
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(C["dark"])
    t1 = "Bold & Balanced"
    t1w = c.stringWidth(t1, "Helvetica-Bold", 30)
    c.drawString((W - t1w) / 2, H * 0.70, t1)

    c.setFont("Helvetica-Bold", 22)
    t2 = "Wedding Bible"
    t2w = c.stringWidth(t2, "Helvetica-Bold", 22)
    c.drawString((W - t2w) / 2, H * 0.63, t2)

    c.setStrokeColor(C["gold"])
    c.setLineWidth(1.5)
    c.line(W * 0.18, H * 0.61, W * 0.82, H * 0.61)
    c.line(W * 0.18, H * 0.72, W * 0.82, H * 0.72)

    c.setFont("Helvetica", 13)
    c.setFillColor(C["rose_gold"])
    sub = "Canva Editable Template Blueprint"
    subw = c.stringWidth(sub, "Helvetica", 13)
    c.drawString((W - subw) / 2, H * 0.57, sub)

    c.setFont("Helvetica", 10)
    c.setFillColor(C["mid"])
    sub2 = "Design Specification & Build Guide for Canva Designers"
    sub2w = c.stringWidth(sub2, "Helvetica", 10)
    c.drawString((W - sub2w) / 2, H * 0.52, sub2)

    # Info box
    box_y = H * 0.34
    c.setFillColor(white)
    c.roundRect(M, box_y, TW, H * 0.15, 8, stroke=0, fill=1)
    c.setStrokeColor(C["border"])
    c.setLineWidth(0.8)
    c.roundRect(M, box_y, TW, H * 0.15, 8, fill=0)

    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(C["rose_gold"])
    c.drawString(M + 12, box_y + H * 0.13, "INCLUDED IN THIS BLUEPRINT:")
    c.setFont("Helvetica", 8)
    c.setFillColor(C["dark"])
    items = [
        "  • Complete page-by-page layout specifications",
        "  • Exact colour palette (hex codes) and font pairings",
        "  • Element dimensions, spacing, and alignment rules",
        "  • Step-by-step Canva build instructions",
        "  • How to set up template sharing for Etsy delivery",
    ]
    iy = box_y + H * 0.115
    for item in items:
        c.drawString(M + 12, iy, item)
        iy -= 12

    # Bottom branding
    c.setFillColor(C["hot_pink"])
    c.rect(0, 0, W, 0.55 * inch, stroke=0, fill=1)
    c.setFont("Helvetica", 9)
    c.setFillColor(white)
    brand = "THE PLANNERS COLLECTIVE  ·  Canva Blueprint Edition"
    bw = c.stringWidth(brand, "Helvetica", 9)
    c.drawString((W - bw) / 2, 0.18 * inch, brand)


def build_overview_page(c: Canvas, pg: int) -> None:
    y = page_header(c, "Blueprint Overview", pg)

    y = body(c,
        "This blueprint is your complete guide to building the Bold & Balanced "
        "Wedding Bible as a fully editable Canva template. Follow these specifications "
        "exactly to match the luxury aesthetic of the other bundle versions.", y)
    y -= 8

    section_heading(c, "WHAT YOU WILL BUILD IN CANVA", y)
    y -= 18
    specs = [
        ("Total pages:", "52 pages (US Letter 8.5×11 in)"),
        ("Canva document type:", "Presentation (8.5×11) or Custom Size"),
        ("File format for delivery:", "Canva Template Link (share as template)"),
        ("Editable elements:", "All text fields, colours, images, icons"),
        ("Non-editable:", "Decorative borders and background patterns"),
    ]
    for k, v in specs:
        y = kv(c, k, v, y, key_w=150)
    y -= 10

    section_heading(c, "CANVA ACCOUNT REQUIREMENTS", y)
    y -= 18
    for item in [
        "Canva Pro account (required for Brand Kit and Template sharing)",
        "Brand Kit set up with the exact colours from this blueprint",
        "Custom fonts uploaded (or use the free Canva font alternatives listed)",
        "Template sharing enabled: Settings → Share a Template → Copy link",
    ]:
        y = bullet(c, item, y)
    y -= 10

    section_heading(c, "DELIVERY METHOD FOR ETSY BUYERS", y)
    y -= 18
    steps = [
        "1. Build your Canva template using this blueprint",
        "2. Click Share → More → Template link",
        "3. Copy the 'Use as template' link",
        "4. Paste the link into your Etsy listing's digital download (as a PDF or TXT file)",
        "   OR include it in a welcome PDF that downloads automatically",
        "5. When buyers click the link, they get their own editable copy — "
           "they cannot edit your master",
    ]
    for step in steps:
        y = body(c, step, y, indent=8 if step.startswith("   ") else 0)
    y -= 10

    section_heading(c, "DOCUMENT STRUCTURE SUMMARY", y)
    y -= 18
    pages = [
        ("Pages 1",    "Cover Page (personalisation fields)"),
        ("Pages 2–3",  "Welcome & How To Use"),
        ("Pages 4–6",  "Wedding Details & Vision"),
        ("Pages 7–10", "Budget Dashboard & Detail"),
        ("Pages 11–14","Guest List & RSVPs"),
        ("Pages 15–18","Vendor Tracker Cards"),
        ("Pages 19–21","Day-of Timeline"),
        ("Pages 22–25","Master Checklist"),
        ("Pages 26–28","Bridal Party"),
        ("Pages 29–32","Seating Chart"),
        ("Pages 33–36","Gift Registry & Tracker"),
        ("Pages 37–40","Notes & Inspiration"),
        ("Pages 41–44","Honeymoon Planning"),
        ("Pages 45–52","Blank lined notes pages"),
    ]
    for pg_range, desc in pages:
        y = kv(c, pg_range, desc, y, key_w=90)

    page_footer(c)


def build_colours_page(c: Canvas, pg: int) -> None:
    y = page_header(c, "Colour Palette & Brand Identity", pg)

    y = body(c,
        "Use these exact hex values in your Canva Brand Kit. Every page element "
        "in the template references one of these colours.", y)
    y -= 12

    section_heading(c, "PRIMARY PALETTE", y)
    y -= 30

    swatches = [
        ("#E91E8C", "Hot Pink"),
        ("#F48FB1", "Pink"),
        ("#FDE8EE", "Blush"),
        ("#C9A84C", "Gold"),
        ("#B76E79", "Rose Gold"),
        ("#212121", "Near Black"),
    ]
    sx = X0
    for hex_code, label in swatches:
        color_swatch(c, hex_code, label, sx, y)
        sx += 76
    y -= 38

    section_heading(c, "SECONDARY / SUPPORT PALETTE", y)
    y -= 30
    support = [
        ("#FFF8E7", "Cream"),
        ("#FFF9C4", "Lt Gold"),
        ("#FCE4EC", "Lt Pink"),
        ("#4DB6AC", "Teal"),
        ("#F3E5F5", "Lavender"),
        ("#5D4037", "Warm Brown"),
    ]
    sx = X0
    for hex_code, label in support:
        color_swatch(c, hex_code, label, sx, y)
        sx += 76
    y -= 38

    section_heading(c, "TYPOGRAPHY", y)
    y -= 18
    fonts = [
        ("Main Heading (H1)", "Canva: Playfair Display Bold, 28–36pt",
         "Free alt: EB Garamond Bold"),
        ("Sub Heading (H2)", "Canva: Playfair Display Regular, 18–22pt",
         "Free alt: EB Garamond"),
        ("Section Labels", "Canva: Montserrat Bold, 10–12pt",
         "Free alt: Poppins Bold"),
        ("Body / Field Labels", "Canva: Montserrat Regular, 8–9pt",
         "Free alt: Poppins Regular"),
        ("Accent / Italics", "Canva: Playfair Display Italic, 9–11pt",
         "Free alt: EB Garamond Italic"),
        ("Numbers / Stats", "Canva: Montserrat Bold, 16–24pt",
         "Free alt: Poppins Bold"),
    ]
    for role, primary, alt in fonts:
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(C["rose_gold"])
        c.drawString(X0, y, role)
        y -= 12
        c.setFont("Helvetica", 8)
        c.setFillColor(C["dark"])
        c.drawString(X0 + 16, y, f"Primary: {primary}")
        y -= 11
        c.setFont("Helvetica", 7.5)
        c.setFillColor(C["mid"])
        c.drawString(X0 + 16, y, f"Alternative: {alt}")
        y -= 16

    section_heading(c, "COLOUR USAGE RULES", y)
    y -= 18
    rules = [
        "Hot Pink (#E91E8C) — section divider backgrounds, primary buttons, cover accent",
        "Gold (#C9A84C) — all horizontal rules, table headers, premium accents",
        "Rose Gold (#B76E79) — sub-headings, field labels, secondary emphasis",
        "Blush (#FDE8EE) — page backgrounds, card fills, alternating row fills",
        "Near Black (#212121) — all body text, primary headings",
        "White (#FFFFFF) — text on coloured backgrounds, white space",
    ]
    for rule in rules:
        y = bullet(c, rule, y)

    page_footer(c)


def build_layout_rules_page(c: Canvas, pg: int) -> None:
    y = page_header(c, "Layout Rules & Spacing System", pg)

    section_heading(c, "CANVA PAGE SETUP", y)
    y -= 18
    for k, v in [
        ("Document size:", "8.5 × 11 inches (US Letter)"),
        ("Bleed:", "0.125 in each side (for print products)"),
        ("Safe zone:", "0.25 in from all edges — keep all text inside this"),
        ("Left margin:", "0.75 in (wider — allows for hole-punching / binding)"),
        ("Right margin:", "0.5 in"),
        ("Top margin:", "0.6 in"),
        ("Bottom margin:", "0.5 in"),
        ("Grid:", "Enable Canva grid: 0.125 in spacing"),
    ]:
        y = kv(c, k, v, y, key_w=130)
    y -= 10

    section_heading(c, "HEADER ZONE (every content page)", y)
    y -= 18
    y = body(c,
        "Each content page has a thin header stripe at the top containing the "
        "section label and a gold horizontal rule beneath it.", y, indent=8)
    for k, v in [
        ("Header stripe height:", "0.45 in from top of safe zone"),
        ("Stripe fill:", "Hot Pink (#E91E8C)"),
        ("Left accent block:", "4pt wide × full stripe height, Gold (#C9A84C)"),
        ("Section label font:", "Montserrat Bold, 9pt, White"),
        ("Label format:", "\"02  ·  WEDDING DETAILS\" (number · name in CAPS)"),
        ("Gold rule below stripe:", "0.5pt stroke, Gold (#C9A84C), full page width"),
    ]:
        y = kv(c, k, v, y, key_w=175)
    y -= 10

    section_heading(c, "FOOTER ZONE (every content page)", y)
    y -= 18
    for k, v in [
        ("Footer rule:", "0.4pt, Light Pink (#E0C0CC), 0.5 in from bottom edge"),
        ("Left footer text:", "Bold & Balanced Wedding Bible  ·  Marigold Bride"),
        ("Right footer:", "Page number (auto-number in Canva)"),
        ("Footer font:", "Montserrat Regular, 7pt, #E0C0CC"),
    ]:
        y = kv(c, k, v, y, key_w=140)
    y -= 10

    section_heading(c, "SECTION DIVIDER PAGES", y)
    y -= 18
    for k, v in [
        ("Background fill:", "Blush (#FDE8EE) — full page bleed"),
        ("Outer border:", "1.2pt stroke, #C0A0A8, inset 0.35 in from edge"),
        ("Inner border:", "0.4pt stroke, same colour, inset 0.42 in"),
        ("Corner accents:", "Small diamond shapes, Gold (#C9A84C), at each corner"),
        ("Section number:", "Playfair Display, 36pt, Gold, centred at 58% page height"),
        ("Gold rules:", "Horizontal rules above/below number, 0.8pt, Gold"),
        ("Section name:", "Playfair Display Bold, 18pt, Near Black, centred at 48%"),
        ("Sub-line:", "Montserrat, 9pt, Rose Gold, centred"),
    ]:
        y = kv(c, k, v, y, key_w=145)

    page_footer(c)


def build_page_specs(c: Canvas, pg: int) -> None:
    y = page_header(c, "Page-by-Page Specifications", pg)

    pages_spec = [
        ("COVER PAGE (Page 1)", [
            ("Background:", "Blush (#FDE8EE) full bleed"),
            ("Top bar:", "Gold, full width, 12% page height"),
            ("Title line 1:", '"Bold & Balanced" — Playfair Display Bold, 26pt, Near Black'),
            ("Title line 2:", '"Wedding Bible" — Playfair Display Bold, 22pt, Near Black'),
            ("Gold rules:", "1.2pt horizontal rules above and below title block"),
            ("Sub-title:", '"Modern Luxury Wedding Planning System" — Playfair Italic, 11pt, Rose Gold'),
            ("Fields (4):", "Bride, Groom, Date, Venue — Montserrat 8pt label, gold underline"),
            ("Bottom bar:", "Hot Pink, full width, 6% page height, brand text in white"),
        ]),
        ("WELCOME PAGE (Page 2)", [
            ("Background:", "White"),
            ("Header zone:", "Standard header — Section 01 · INTRODUCTION"),
            ("Welcome text:", "Playfair Display Italic, 18pt, Near Black, centred"),
            ("Body text:", "Montserrat Regular, 8.5pt, Near Black, left-aligned"),
            ("Intro paragraphs:", "3 paragraphs with 10pt spacing between"),
            ("How To Use box:", "Blush fill, Rose Gold border, Montserrat Bold 9pt heading"),
            ("Bullet points:", "Rose Gold dot (•), Montserrat Regular 8pt"),
        ]),
        ("TABLE OF CONTENTS (Page 3)", [
            ("Two columns:", "Section numbers (left) and section names (right)"),
            ("Gold dot-leaders:", "Connect section numbers to page numbers"),
            ("Section names:", "Montserrat Regular, 9pt, Near Black"),
            ("Section numbers:", "Montserrat Bold, 9pt, Hot Pink"),
            ("Page numbers:", "Montserrat Regular, 9pt, right-aligned"),
        ]),
        ("WEDDING DETAILS (Pages 4–6)", [
            ("Page 4:", "Personal info fields — 6 full-width fields stacked"),
            ("Page 5:", "Wedding day details — 2-column layout (5 rows × 2 fields)"),
            ("Page 6:", "Vision/inspiration — decorative prompt + ruled lines"),
            ("Field style:", "Label: Montserrat 7pt Rose Gold, Line: 0.5pt Gold underline"),
            ("2-col gap:", "0.2 in gutter between left and right columns"),
        ]),
        ("BUDGET PAGES (Pages 7–10)", [
            ("Page 7:", "Budget summary — 4 KPI boxes + instructions"),
            ("Page 8:", "Category table — 20 rows × 5 columns with gold header"),
            ("Page 9:", "Item detail table — 46 rows × 8 columns"),
            ("Page 10:", "Budget notes — ruled lines page"),
            ("KPI box style:", "Coloured fill, Montserrat Bold 16pt stat, 8pt label"),
            ("Table header:", "Gold (#C9A84C) fill, white Montserrat Bold 8pt"),
            ("Row stripes:", "Alternating Blush and White"),
        ]),
    ]

    for heading, items in pages_spec:
        if y < Y0 + 80:
            page_footer(c)
            new_page(c)
            y = page_header(c, "Page-by-Page Specifications (continued)", pg)

        title_bar(c, heading, y, C["rose_gold"])
        y -= 22
        for k, v in items:
            c.setFont("Helvetica-Bold", 7.5)
            c.setFillColor(C["rose_gold"])
            c.drawString(X0 + 8, y, k)
            c.setFont("Helvetica", 7.5)
            c.setFillColor(C["dark"])
            c.drawString(X0 + 110, y, v)
            y -= 12
        y -= 8

    page_footer(c)


def build_canva_instructions(c: Canvas, pg: int) -> None:
    y = page_header(c, "Step-by-Step Canva Build Instructions", pg)

    steps_groups = [
        ("STEP 1: SET UP YOUR CANVA DOCUMENT", [
            "Log in to Canva Pro",
            "Click 'Create a design' → 'Custom size'",
            "Enter width: 8.5 in, height: 11 in, click 'Create new design'",
            "In the design, go to File → Page Setup and confirm the dimensions",
            "Turn on the grid: View → Show rulers and guides",
            "Add margin guides: 0.75 in left, 0.5 in right/top/bottom",
        ]),
        ("STEP 2: SET UP YOUR BRAND KIT (Canva Pro)", [
            "Go to Brand Hub → Brand Kits → New Brand Kit",
            "Name it 'Wedding Bible — Luxury'",
            "Add all 12 palette colours (hex codes on the Colours page of this blueprint)",
            "Upload fonts OR select the free Canva alternatives listed on the Typography page",
            "Save the Brand Kit — it will appear in the left panel when designing",
        ]),
        ("STEP 3: BUILD THE COVER PAGE FIRST", [
            "Add a background rectangle, fill Blush (#FDE8EE), full page",
            "Add top bar rectangle: full width, 1.1 in tall, fill Gold",
            "Add main title text box: Playfair Display Bold 26pt, type 'Bold & Balanced'",
            "Add second title: Playfair Display Bold 22pt, type 'Wedding Bible'",
            "Add two thin horizontal lines (Line element), 1.2pt, Gold colour",
            "Add sub-title: Playfair Italic 11pt, Rose Gold, 'Modern Luxury...'",
            "Add 4 text fields for personalisation (label + underline each)",
            "Add bottom bar: full width, 0.55 in, Hot Pink, brand text centred",
            "Group all cover elements once finalized",
        ]),
        ("STEP 4: CREATE A MASTER HEADER COMPONENT", [
            "On page 2, add the header stripe rectangle",
            "Add the gold left-accent block (4pt wide inside the stripe)",
            "Add the section label text box",
            "Add the gold rule below the stripe",
            "Group these 4 elements → right-click → Group",
            "Copy this group to every content page and update the section label",
            "Note: in Canva, you cannot create true 'master' elements — "
            "copy/paste and update manually",
        ]),
        ("STEP 5: BUILD SECTION DIVIDER PAGES", [
            "Add Blush full-page background",
            "Add outer border rectangle (stroke only, 1.2pt, #C0A0A8)",
            "Add inner border rectangle (stroke only, 0.4pt, same colour)",
            "Add 4 diamond shapes at corners (use Canva Diamond element, Gold fill)",
            "Add section number text: Playfair Display 36pt, Gold, centred",
            "Add two thin gold horizontal rules",
            "Add section name: Playfair Display Bold 18pt, Near Black, centred",
            "Add sub-line: Montserrat 9pt, Rose Gold",
            "Duplicate this page for each of the 12 sections, updating text only",
        ]),
        ("STEP 6: BUILD TABLE PAGES", [
            "Use Canva's 'Table' element (Elements → Tables)",
            "Set table width to fill content area",
            "Header row: Gold fill, White Montserrat Bold 8pt text",
            "Data rows: alternate Blush and White fills",
            "Column borders: 0.3pt, Light Pink (#F2DCE4)",
            "Outer border: 0.6pt, Border Pink (#E0C0CC)",
            "For each table type, set column widths as specified on the Layout page",
        ]),
        ("STEP 7: MAKE TEXT FIELDS EDITABLE", [
            "In Canva templates, all text is editable by default for the recipient",
            "Add instructional placeholder text so buyers know what to type",
            "Use light grey italic text for placeholder labels (e.g. 'Type partner name here')",
            "Consider locking decorative elements: right-click → Lock",
            "Do NOT lock text fields — buyers need to type in them",
            "Test the template yourself by using the template link first",
        ]),
        ("STEP 8: SHARE AS A TEMPLATE", [
            "When your design is complete, click 'Share' (top right)",
            "Select 'More' at the bottom of the share panel",
            "Click 'Template link'",
            "Copy the link — this is what you deliver to Etsy buyers",
            "Create a simple PDF or TXT file containing the link and instructions",
            "Upload that PDF/TXT as the digital download in your Etsy listing",
            "Buyers click the link → 'Use template' → get their own editable copy",
        ]),
    ]

    for group_title, steps in steps_groups:
        if y < Y0 + 60:
            page_footer(c)
            new_page(c)
            y = page_header(c, "Canva Build Instructions (continued)", pg)

        title_bar(c, group_title, y, C["teal"])
        y -= 22
        for i, step in enumerate(steps, 1):
            if y < Y0 + 20:
                page_footer(c)
                new_page(c)
                y = page_header(c, "Canva Build Instructions (continued)", pg)
            c.setFont("Helvetica-Bold", 8)
            c.setFillColor(C["teal"])
            c.drawString(X0 + 8, y, f"{i}.")
            c.setFont("Helvetica", 8)
            c.setFillColor(C["dark"])
            # simple word wrap
            words = step.split()
            line = ""
            lines_out = []
            for word in words:
                if len(line + " " + word) < 95:
                    line = (line + " " + word).strip()
                else:
                    lines_out.append(line)
                    line = word
            if line:
                lines_out.append(line)
            for j, ln in enumerate(lines_out):
                c.drawString(X0 + 22, y, ln)
                y -= 12
            y -= 2
        y -= 8

    page_footer(c)


def build_etsy_delivery_page(c: Canvas, pg: int) -> None:
    y = page_header(c, "Etsy Listing & Customer Delivery Guide", pg)

    section_heading(c, "WHAT TO INCLUDE IN YOUR ETSY LISTING", y)
    y -= 18
    for item in [
        "Main listing image: Mockup of the planner open on a laptop or tablet",
        "Images 2–4: Screenshots of key pages (Budget dashboard, Guest list, Timeline)",
        "Image 5: 'Delivered as a Canva template — get your own editable copy' graphic",
        "Image 6: Before/after — blank template vs. filled-in example",
        "Image 7: Device compatibility mockup (laptop, tablet, phone)",
    ]:
        y = bullet(c, item, y)
    y -= 10

    section_heading(c, "LISTING TITLE (recommended)", y)
    y -= 18
    c.setFont("Helvetica", 8.5)
    c.setFillColor(C["dark"])
    title_text = ("Wedding Planner Canva Template, Editable Wedding Planner, Bridal Planner, "
                  "Wedding Organiser, Digital Wedding Planner, Wedding Planning Canva")
    y = body(c, title_text, y, indent=8)
    y -= 10

    section_heading(c, "KEY LISTING TAGS", y)
    y -= 18
    tags = [
        "wedding planner canva", "editable wedding planner", "digital wedding planner",
        "bridal planner", "wedding organiser", "canva wedding template",
        "luxury wedding planner", "modern wedding planner", "wedding planning kit",
        "etsy wedding template", "printable wedding binder", "wedding checklist",
        "budget tracker wedding", "guest list tracker", "wedding countdown",
    ]
    y = body(c, " · ".join(tags), y, indent=8, size=8)
    y -= 10

    section_heading(c, "DIGITAL DOWNLOAD FILE TO DELIVER", y)
    y -= 18
    for item in [
        "Create a single PDF file called 'YOUR_TEMPLATE_ACCESS.pdf'",
        "Include the Canva template link in large, clear text",
        "Include 3-step instructions: 1) Click link  2) Select 'Use template'  "
        "3) Customise and download",
        "Include your branding and a note about contacting you for support",
        "Upload this PDF as the digital download in your Etsy listing",
    ]:
        y = bullet(c, item, y)
    y -= 10

    section_heading(c, "CUSTOMER INSTRUCTIONS SUMMARY", y)
    y -= 18
    y = body(c,
        "Include the following instructions in your template access PDF:", y)
    instructions = [
        "1. Click the Canva template link included in this file",
        "2. Sign up for a free Canva account if you don't have one",
        "3. Click 'Use template' — this creates YOUR personal editable copy",
        "4. Customise all text, colours, and images to suit your wedding",
        "5. Download as PDF for printing, or keep it in Canva to edit on any device",
        "6. The template link never expires — bookmark it for easy access",
        "Note: You are editing YOUR copy. No one else can see your changes.",
    ]
    for inst in instructions:
        y = body(c, inst, y, indent=16)
    y -= 10

    section_heading(c, "PRICING GUIDANCE", y)
    y -= 18
    for item in [
        "Canva template only: $9.99 – $14.99 USD",
        "As part of the full 9-version bundle: $27 – $47 USD",
        "Canva + Printable PDF bundle: $16.99 – $22.99 USD",
        "Canva + Excel + GoodNotes 3-pack: $24.99 – $34.99 USD",
    ]:
        y = bullet(c, item, y)

    page_footer(c)


# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    out = Path("output")
    out.mkdir(exist_ok=True)
    path = out / "Bold_Balanced_Wedding_Bible_Canva_Blueprint.pdf"

    print("Building Canva Blueprint PDF …")
    c = Canvas(str(path), pagesize=letter)
    c.setTitle("Bold & Balanced Wedding Bible — Canva Template Blueprint")
    c.setAuthor("Marigold Bride")

    build_cover_page(c)
    c.showPage()

    pg = 2
    build_overview_page(c, pg); c.showPage(); pg += 1
    build_colours_page(c, pg); c.showPage(); pg += 1
    build_layout_rules_page(c, pg); c.showPage(); pg += 1
    build_page_specs(c, pg); c.showPage(); pg += 1
    build_canva_instructions(c, pg); c.showPage(); pg += 1
    build_etsy_delivery_page(c, pg); c.showPage(); pg += 1

    c.save()
    print(f"  ✓ Saved: {path}")
    print("\nDone!")


if __name__ == "__main__":
    main()
