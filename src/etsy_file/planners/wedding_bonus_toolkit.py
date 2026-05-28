"""
Bold & Balanced Wedding Bible — Bonus Wedding Toolkit
Generated with Python reportlab

Includes:
  1. Wedding Day Emergency Kit Checklist
  2. Vendor Tip & Gratuity Guide
  3. Wedding Day Emergency Contacts Card (print & carry)
  4. Vow Writing Prompts & Worksheet
  5. Wedding Speech Outline Templates (Best Man, Maid of Honour, Father/Mother of Bride)
  6. Wedding Morning Schedule (detailed hour-by-hour)
  7. Post-Wedding Checklist (name change, thank-you notes, etc.)

Usage:
    pip install reportlab
    python wedding_bonus_toolkit.py

Output (in ./output/):
    Bold_Balanced_Wedding_Bible_Bonus_Toolkit.pdf
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
    "hot_pink":   HexColor("#E91E8C"),
    "pink":       HexColor("#F48FB1"),
    "blush":      HexColor("#FDE8EE"),
    "gold":       HexColor("#C9A84C"),
    "light_gold": HexColor("#FFF9C4"),
    "rose_gold":  HexColor("#B76E79"),
    "dark":       HexColor("#212121"),
    "mid":        HexColor("#5D4037"),
    "line":       HexColor("#E0C0CC"),
    "white":      HexColor("#FFFFFF"),
    "cream":      HexColor("#FFF8E7"),
    "teal":       HexColor("#4DB6AC"),
    "light_teal": HexColor("#E0F2F1"),
    "green":      HexColor("#66BB6A"),
    "red":        HexColor("#EF5350"),
    "light_red":  HexColor("#FFEBEE"),
}

_page_count = 0


# ─────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────

def new_page(c: Canvas) -> None:
    global _page_count
    if _page_count > 0:
        c.showPage()
    _page_count += 1


def page_header(c: Canvas, section_num: str, section_title: str) -> float:
    c.setFillColor(C["hot_pink"])
    c.rect(X0, Y1 - 0.4 * inch, TW, 0.4 * inch, stroke=0, fill=1)
    c.setFillColor(C["gold"])
    c.rect(X0, Y1 - 0.4 * inch - 3, TW, 3, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(white)
    c.drawString(X0 + 8, Y1 - 0.25 * inch,
                 f"{section_num}  ·  {section_title.upper()}")
    y = Y1 - 0.4 * inch - 14
    return y


def page_footer(c: Canvas, page_num: int) -> None:
    c.setFont("Helvetica", 7)
    c.setFillColor(C["line"])
    c.drawString(X0, Y0 - 14, "Bold & Balanced Wedding Bible  ·  Bonus Toolkit  ·  Marigold Bride")
    c.drawRightString(X1, Y0 - 14, str(page_num))
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.4)
    c.line(X0, Y0 - 3, X1, Y0 - 3)


def section_divider(c: Canvas, number: str, title: str, subtitle: str = "") -> None:
    new_page(c)
    c.setFillColor(C["blush"])
    c.rect(0, 0, W, H, stroke=0, fill=1)
    pad = 0.4 * inch
    c.setStrokeColor(C["line"])
    c.setLineWidth(1.2)
    c.rect(pad, pad, W - 2 * pad, H - 2 * pad, fill=0)
    c.setLineWidth(0.4)
    pad2 = pad + 8
    c.rect(pad2, pad2, W - 2 * pad2, H - 2 * pad2, fill=0)
    # diamonds
    for cx, cy in [(pad, pad), (W - pad, pad), (pad, H - pad), (W - pad, H - pad)]:
        _diamond(c, cx, cy, 7)
    # number
    c.setFont("Helvetica-Bold", 40)
    c.setFillColor(C["gold"])
    nw = c.stringWidth(number, "Helvetica-Bold", 40)
    c.drawString((W - nw) / 2, H * 0.58, number)
    # rules
    c.setStrokeColor(C["gold"])
    c.setLineWidth(0.8)
    c.line(W * 0.22, H * 0.565, W * 0.78, H * 0.565)
    c.line(W * 0.22, H * 0.628, W * 0.78, H * 0.628)
    # title
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(C["dark"])
    tw = c.stringWidth(title.upper(), "Helvetica-Bold", 18)
    c.drawString((W - tw) / 2, H * 0.49, title.upper())
    if subtitle:
        c.setFont("Helvetica", 9)
        c.setFillColor(C["rose_gold"])
        sw = c.stringWidth(subtitle, "Helvetica", 9)
        c.drawString((W - sw) / 2, H * 0.45, subtitle)
    c.setFont("Helvetica", 8)
    c.setFillColor(C["gold"])
    brand = "Bold & Balanced Wedding Bible  ·  Bonus Toolkit"
    bw = c.stringWidth(brand, "Helvetica", 8)
    c.drawString((W - bw) / 2, H * 0.40, brand)


def _diamond(c: Canvas, cx: float, cy: float, r: float) -> None:
    p = c.beginPath()
    p.moveTo(cx, cy + r)
    p.lineTo(cx + r, cy)
    p.lineTo(cx, cy - r)
    p.lineTo(cx - r, cy)
    p.close()
    c.setFillColor(C["gold"])
    c.drawPath(p, stroke=0, fill=1)


def heading(c: Canvas, text: str, y: float, size: int = 11) -> float:
    c.setFont("Helvetica-Bold", size)
    c.setFillColor(C["rose_gold"])
    c.drawString(X0, y, text)
    c.setStrokeColor(C["gold"])
    c.setLineWidth(0.5)
    c.line(X0, y - 3, X1, y - 3)
    return y - 16


def checkbox_item(c: Canvas, text: str, y: float,
                  indent: float = 0, bold: bool = False) -> float:
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.6)
    c.rect(X0 + indent, y - 9, 10, 10, fill=0)
    font = "Helvetica-Bold" if bold else "Helvetica"
    c.setFont(font, 8)
    c.setFillColor(C["dark"])
    # word wrap
    words = text.split()
    line = ""
    lines = []
    for word in words:
        if len(line + " " + word) < 85:
            line = (line + " " + word).strip()
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    for i, ln in enumerate(lines):
        c.drawString(X0 + indent + 15, y - (i * 11), ln)
    return y - max(11 * len(lines), 14)


def ruled_line(c: Canvas, y: float, label: str = "",
               indent: float = 0, w: float | None = None) -> float:
    lw = w if w is not None else TW - indent
    if label:
        c.setFont("Helvetica", 7)
        c.setFillColor(C["mid"])
        c.drawString(X0 + indent, y, label)
        y -= 18
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.5)
    c.line(X0 + indent, y, X0 + indent + lw, y)
    return y - 8


def write_lines(c: Canvas, y: float, n: int = 8,
                line_h: float = 24) -> float:
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.4)
    for _ in range(n):
        y -= line_h
        c.line(X0, y, X1, y)
    return y


def body_text(c: Canvas, text: str, y: float,
              size: int = 8, indent: float = 0,
              color: str = "dark") -> float:
    c.setFont("Helvetica", size)
    c.setFillColor(C[color])
    words = text.split()
    line = ""
    max_chars = int((TW - indent) / (size * 0.52))
    lines = []
    for word in words:
        if len(line + " " + word) <= max_chars:
            line = (line + " " + word).strip()
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    for ln in lines:
        c.drawString(X0 + indent, y, ln)
        y -= size + 4
    return y


def highlight_box(c: Canvas, y: float, text: str,
                  fill: str = "light_gold", h: float = 28) -> float:
    c.setFillColor(C[fill])
    c.rect(X0, y - h + 8, TW, h, stroke=0, fill=1)
    c.setStrokeColor(C["gold"])
    c.setLineWidth(0.5)
    c.rect(X0, y - h + 8, TW, h, fill=0)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(C["dark"])
    c.drawString(X0 + 8, y - 4, text)
    return y - h


# ─────────────────────────────────────────────────────────────────────
# COVER
# ─────────────────────────────────────────────────────────────────────

def build_cover(c: Canvas) -> None:
    new_page(c)
    c.setFillColor(C["blush"])
    c.rect(0, 0, W, H, stroke=0, fill=1)

    c.setFillColor(C["gold"])
    c.rect(0, H - 1.1 * inch, W, 1.1 * inch, stroke=0, fill=1)

    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(C["dark"])
    t = "Bold & Balanced Wedding Bible"
    tw = c.stringWidth(t, "Helvetica-Bold", 24)
    c.drawString((W - tw) / 2, H * 0.72, t)

    c.setFont("Helvetica-Bold", 18)
    t2 = "Bonus Wedding Toolkit"
    t2w = c.stringWidth(t2, "Helvetica-Bold", 18)
    c.drawString((W - t2w) / 2, H * 0.65, t2)

    c.setStrokeColor(C["gold"])
    c.setLineWidth(1.5)
    c.line(W * 0.18, H * 0.63, W * 0.82, H * 0.63)
    c.line(W * 0.18, H * 0.74, W * 0.74, H * 0.74)

    c.setFont("Helvetica", 10)
    c.setFillColor(C["rose_gold"])
    sub = "7 Premium Add-On Tools for Your Wedding Day"
    sw = c.stringWidth(sub, "Helvetica", 10)
    c.drawString((W - sw) / 2, H * 0.59, sub)

    tools = [
        "Emergency Kit Checklist",
        "Vendor Tip & Gratuity Guide",
        "Emergency Contacts Card",
        "Vow Writing Prompts",
        "Speech Outline Templates (3)",
        "Wedding Morning Schedule",
        "Post-Wedding To-Do Checklist",
    ]
    c.setFont("Helvetica", 9)
    c.setFillColor(C["dark"])
    box_y = H * 0.40
    c.setFillColor(white)
    c.roundRect(M, box_y, TW, H * 0.16, 8, stroke=0, fill=1)
    c.setStrokeColor(C["line"])
    c.setLineWidth(0.6)
    c.roundRect(M, box_y, TW, H * 0.16, 8, fill=0)
    iy = box_y + H * 0.148
    for tool in tools:
        c.setFillColor(C["rose_gold"])
        c.drawString(M + 14, iy, "✦")
        c.setFillColor(C["dark"])
        c.setFont("Helvetica", 9)
        c.drawString(M + 28, iy, tool)
        iy -= 13

    c.setFillColor(C["hot_pink"])
    c.rect(0, 0, W, 0.5 * inch, stroke=0, fill=1)
    c.setFont("Helvetica", 8)
    c.setFillColor(white)
    brand = "THE PLANNERS COLLECTIVE  ·  Bonus Toolkit Edition"
    bw = c.stringWidth(brand, "Helvetica", 8)
    c.drawString((W - bw) / 2, 0.16 * inch, brand)


# ─────────────────────────────────────────────────────────────────────
# TOOL 1: EMERGENCY KIT CHECKLIST
# ─────────────────────────────────────────────────────────────────────

def build_emergency_kit(c: Canvas, pg: int) -> int:
    section_divider(c, "01", "Emergency Kit Checklist",
                    "Everything you need in your wedding day emergency bag")
    pg += 1

    new_page(c)
    y = page_header(c, "01", "Emergency Kit Checklist")
    y = heading(c, "THE ULTIMATE WEDDING DAY EMERGENCY KIT", y)
    y = body_text(c,
        "Pack these items in a small bag or box and assign someone in your bridal party "
        "to carry it on the day. Being prepared means small disasters stay small.", y)
    y -= 6

    categories = {
        "BEAUTY & GROOMING": [
            ("Safety pins (assorted sizes)", False),
            ("Double-sided fashion tape", False),
            ("Stain remover pen / tide pen", False),
            ("Clear nail polish (for snags / runs)", False),
            ("Spare pair of nude/nude-sheer tights", False),
            ("Blotting papers / pressed powder compact", False),
            ("Travel hairspray", False),
            ("Bobby pins and hair elastics (matching hair colour)", False),
            ("Travel deodorant (non-marking)", False),
            ("Lip gloss or lipstick touch-up (bridal colour)", False),
            ("Travel mirror", False),
            ("Tweezers", False),
            ("Nail file / nail glue for emergencies", False),
            ("Travel perfume / cologne (small bottle)", False),
        ],
        "HEALTH & COMFORT": [
            ("Pain relief tablets (paracetamol / ibuprofen)", False),
            ("Antacids / indigestion tablets", False),
            ("Allergy tablets (antihistamine)", False),
            ("Blister plasters / heel cushions", False),
            ("Spare flat shoes or flip-flops for reception", False),
            ("Travel sewing kit (needle, thread in dress colour)", False),
            ("Bandaids / plasters (various sizes)", False),
            ("Tissues / pocket handkerchiefs (for happy tears!)", False),
            ("Breath mints / mouthwash strips", False),
            ("Energy snacks (granola bar, nuts) — eat before ceremony!", False),
            ("Straws (to drink without smudging lipstick)", False),
            ("Small bottle of water", False),
        ],
        "PRACTICAL ESSENTIALS": [
            ("Rings (in a safe place — do not forget!)", True),
            ("Signed marriage licence paperwork", True),
            ("Vendor tip envelopes (labelled and sealed)", True),
            ("List of vendor contacts and phone numbers", True),
            ("Day-of timeline (printed copy)", True),
            ("Phone charger / portable power bank", False),
            ("Cash (small amount for tips / emergencies)", False),
            ("Spare pair of contact lenses / glasses", False),
            ("Travel umbrella (just in case!)", False),
            ("Spare vows (printed backup)", False),
            ("White chalk (to cover dirt marks on dress)", False),
            ("Clear button thread", False),
        ],
    }

    col_w = TW / 2 - 10
    for cat_name, items in categories.items():
        if y < Y0 + 40:
            page_footer(c, pg)
            pg += 1
            new_page(c)
            y = page_header(c, "01", "Emergency Kit Checklist")

        y = heading(c, cat_name, y, size=9)

        # Two-column checklist
        left_items = items[:len(items)//2 + len(items)%2]
        right_items = items[len(items)//2 + len(items)%2:]
        left_y = y
        right_y = y

        for text, bold in left_items:
            left_y = checkbox_item(c, text, left_y, indent=0, bold=bold)
            left_y -= 2

        # reset and draw right column
        for text, bold in right_items:
            # Use right column position
            c.setStrokeColor(C["line"])
            c.setLineWidth(0.6)
            c.rect(X0 + col_w + 16, right_y - 9, 10, 10, fill=0)
            font = "Helvetica-Bold" if bold else "Helvetica"
            c.setFont(font, 8)
            c.setFillColor(C["dark"])
            c.drawString(X0 + col_w + 32, right_y, text)
            right_y -= 14

        y = min(left_y, right_y) - 8

    page_footer(c, pg)
    return pg


# ─────────────────────────────────────────────────────────────────────
# TOOL 2: VENDOR TIP GUIDE
# ─────────────────────────────────────────────────────────────────────

def build_tip_guide(c: Canvas, pg: int) -> int:
    section_divider(c, "02", "Vendor Tip & Gratuity Guide",
                    "How much to tip each vendor — plus envelope tracking")
    pg += 1

    new_page(c)
    y = page_header(c, "02", "Vendor Tip & Gratuity Guide")
    y = heading(c, "TIPPING GUIDE FOR WEDDING VENDORS", y)
    y = body_text(c,
        "Tipping is optional but appreciated. These are general guidelines — adjust based "
        "on the quality of service and whether gratuity is included in your contract. "
        "Prepare tip envelopes in advance, labelled with each vendor's name.", y)
    y -= 8

    tip_data = [
        ("Officiant / Celebrant",    "$50–$100",
         "Often a flat donation to their ceremony fund; ask what they prefer"),
        ("Photographer",             "$50–$200 per photographer",
         "Usually given at the end of the night; note if 2nd shooter is present"),
        ("Videographer",             "$50–$150",
         "Similar to photographer — acknowledge both individuals if a team"),
        ("Caterer / Head Chef",      "$50–$200",
         "Give to head chef or catering manager to distribute to kitchen staff"),
        ("Wait Staff",               "15–20% of food & beverage total",
         "Check contract — some caterers include gratuity; don't double-tip"),
        ("Bar Staff",                "$20–$50 per bartender",
         "Ask venue if a tip jar is permitted; alternative is cash envelope"),
        ("DJ",                       "$50–$150",
         "Give at end of night; if a band, $25–$50 per band member"),
        ("Band / Musicians",         "$25–$50 per musician",
         "Prepare individual envelopes if a large band"),
        ("Hair Stylist",             "15–20% of total",
         "Per stylist — include any assistants who worked on your party"),
        ("Make-Up Artist",           "15–20% of total",
         "Per artist; if they run a team, give one tip to the lead to distribute"),
        ("Florist",                  "$50–$100",
         "If they do a full setup and breakdown; include delivery team"),
        ("Wedding Coordinator",      "$50–$200",
         "For day-of coordinator; if full planner, a gift may be more appropriate"),
        ("Transportation Driver",    "15–20% of total",
         "Per driver; if multiple vehicles, tip each driver separately"),
        ("Wedding Cake",             "$25–$50",
         "If they deliver and set up the cake at the venue"),
        ("Photo Booth Operator",     "$25–$50",
         "If they stay and operate the booth throughout the event"),
    ]

    # table
    hdr_cols = [("VENDOR", 0.28), ("SUGGESTED TIP", 0.18), ("NOTES", 0.54)]
    # header row
    x = X0
    c.setFillColor(C["gold"])
    c.rect(x, y - 16, TW, 16, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(white)
    cx = x + 4
    for label, frac in hdr_cols:
        c.drawString(cx, y - 11, label)
        cx += TW * frac
    y -= 17

    for i, (vendor, tip, note) in enumerate(tip_data):
        if y < Y0 + 18:
            page_footer(c, pg)
            pg += 1
            new_page(c)
            y = page_header(c, "02", "Vendor Tip Guide — continued")

        fill = C["light_gold"] if i % 2 == 0 else C["white"]
        c.setFillColor(fill)
        c.rect(X0, y - 15, TW, 15, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(C["dark"])
        c.drawString(X0 + 4, y - 11, vendor)
        c.setFont("Helvetica-Bold", 7.5)
        c.setFillColor(C["rose_gold"])
        c.drawString(X0 + TW * 0.28 + 4, y - 11, tip)
        c.setFont("Helvetica", 7)
        c.setFillColor(C["mid"])
        c.drawString(X0 + TW * 0.46 + 4, y - 11, note[:72])
        y -= 15

    # Envelope tracker
    y -= 10
    if y < Y0 + 120:
        page_footer(c, pg)
        pg += 1
        new_page(c)
        y = page_header(c, "02", "Vendor Tip — Envelope Tracker")

    y = heading(c, "TIP ENVELOPE TRACKER", y)
    y = body_text(c,
        "Use this table to prepare and track your tip envelopes before the wedding day.", y)
    y -= 6

    env_hdr = [("VENDOR", 0.28), ("AMOUNT $", 0.14), ("ENVELOPE LABELLED?", 0.18),
               ("WHO DELIVERS?", 0.20), ("DELIVERED?", 0.20)]
    c.setFillColor(C["rose_gold"])
    c.rect(X0, y - 16, TW, 16, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(white)
    cx = X0 + 4
    for label, frac in env_hdr:
        c.drawString(cx, y - 11, label)
        cx += TW * frac
    y -= 17

    for i in range(15):
        fill = C["blush"] if i % 2 == 0 else C["white"]
        c.setFillColor(fill)
        c.rect(X0, y - 16, TW, 16, stroke=0, fill=1)
        y -= 16

    page_footer(c, pg)
    return pg


# ─────────────────────────────────────────────────────────────────────
# TOOL 3: EMERGENCY CONTACTS CARD
# ─────────────────────────────────────────────────────────────────────

def build_contacts_card(c: Canvas, pg: int) -> int:
    section_divider(c, "03", "Emergency Contacts Card",
                    "Print and carry — give copies to your bridal party")
    pg += 1

    new_page(c)
    y = page_header(c, "03", "Emergency Contacts Card")
    y = body_text(c,
        "Print this page and cut along the dotted lines. Give one copy to your "
        "Maid of Honour and one to your Best Man. Keep one in your emergency kit.", y)
    y -= 6

    def card(c: Canvas, top: float) -> None:
        card_h = (Y1 - Y0 - 0.4 * inch - 40) / 2
        c.setFillColor(C["blush"])
        c.rect(X0, top - card_h, TW, card_h, stroke=0, fill=1)
        c.setStrokeColor(C["gold"])
        c.setLineWidth(0.8)
        c.rect(X0, top - card_h, TW, card_h, fill=0)
        # header
        c.setFillColor(C["hot_pink"])
        c.rect(X0, top - 18, TW, 18, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(white)
        c.drawString(X0 + 8, top - 13, "WEDDING DAY EMERGENCY CONTACTS")
        c.drawRightString(X1 - 8, top - 13, "Bold & Balanced Wedding Bible")

        contacts = [
            ("Bride", ""),
            ("Groom", ""),
            ("Maid of Honour", ""),
            ("Best Man", ""),
            ("Wedding Coordinator", ""),
            ("Venue — Main Contact", ""),
            ("Photographer", ""),
            ("Caterer", ""),
            ("DJ / Band", ""),
            ("Transport / Driver", ""),
            ("Florist", ""),
            ("Emergency — General", "000 / 911 / 112"),
        ]
        col_w = TW / 2 - 6
        cy = top - 30
        for i, (role, phone) in enumerate(contacts):
            col = i % 2
            cx = X0 + col * (col_w + 12)
            c.setFont("Helvetica-Bold", 6.5)
            c.setFillColor(C["rose_gold"])
            c.drawString(cx + 4, cy, role.upper())
            cy2 = cy - 14
            c.setStrokeColor(C["line"])
            c.setLineWidth(0.4)
            c.line(cx + 4, cy2, cx + col_w, cy2)
            if phone:
                c.setFont("Helvetica-Bold", 7)
                c.setFillColor(C["dark"])
                c.drawString(cx + 4, cy2 + 3, phone)
            if col == 1:
                cy -= 24

    card(c, y)
    y -= (Y1 - Y0 - 0.4 * inch - 40) / 2 + 12
    # dotted cut line
    c.setStrokeColor(C["line"])
    c.setDash(3, 3)
    c.setLineWidth(0.5)
    c.line(X0, y + 2, X1, y + 2)
    c.setDash()
    c.setFont("Helvetica", 7)
    c.setFillColor(C["mid"])
    c.drawCentredString(W / 2, y - 8, "✂  Cut here  ✂")
    y -= 18
    card(c, y)

    page_footer(c, pg)
    return pg


# ─────────────────────────────────────────────────────────────────────
# TOOL 4: VOW WRITING PROMPTS
# ─────────────────────────────────────────────────────────────────────

def build_vow_prompts(c: Canvas, pg: int) -> int:
    section_divider(c, "04", "Vow Writing Prompts",
                    "Guided worksheets to help you write heartfelt, personal vows")
    pg += 1

    new_page(c)
    y = page_header(c, "04", "Vow Writing Prompts & Worksheet")
    y = body_text(c,
        "Use these prompts to brainstorm and draft your personal wedding vows. "
        "There is no right or wrong length — write from the heart. Most vows run "
        "1–3 minutes when spoken aloud. Aim for 150–300 words.", y)
    y -= 8

    prompts = [
        ("The moment I knew:", "Describe when you first realised this was the person you wanted to marry."),
        ("What I love most:", "Name 3 specific qualities — not generic (kind, funny) but stories that show it."),
        ("Our story:", "One short memory that captures your relationship perfectly."),
        ("My promises:", "List 3–5 specific, personal commitments. Be concrete, not clichéd."),
        ("What our future looks like:", "Describe a moment you're looking forward to sharing together."),
        ("My closing words:", "A final sentence that captures everything you want them to know."),
    ]

    for prompt_title, prompt_text in prompts:
        if y < Y0 + 50:
            page_footer(c, pg)
            pg += 1
            new_page(c)
            y = page_header(c, "04", "Vow Writing Prompts")

        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(C["hot_pink"])
        c.drawString(X0, y, prompt_title)
        c.setFont("Helvetica", 7.5)
        c.setFillColor(C["mid"])
        c.drawString(X0 + 120, y, prompt_text)
        y -= 4
        y = write_lines(c, y, n=4, line_h=22)
        y -= 8

    # Final draft page
    page_footer(c, pg)
    pg += 1
    new_page(c)
    y = page_header(c, "04", "My Wedding Vows — Final Draft")
    y = heading(c, "MY WEDDING VOWS", y)
    y = body_text(c,
        "Write your final vows here. Practice reading aloud at least 5 times before the day. "
        "Bring this page or a printed card to the ceremony as your backup.", y)
    y -= 8
    y = write_lines(c, y, n=20, line_h=23)

    page_footer(c, pg)
    return pg


# ─────────────────────────────────────────────────────────────────────
# TOOL 5: SPEECH OUTLINES
# ─────────────────────────────────────────────────────────────────────

def _speech_page(c: Canvas, pg: int, role: str, structure: list) -> int:
    new_page(c)
    y = page_header(c, "05", f"Speech Outline — {role}")
    y = heading(c, f"{role.upper()} SPEECH OUTLINE", y)
    y = body_text(c,
        "Use this outline as a starting point. A good wedding speech runs 3–5 minutes "
        "(approximately 400–600 words). Practice out loud at least 3 times.", y)
    y -= 6
    y = highlight_box(c, y,
        f"Aim for: a warm opening → personal story → heartfelt tribute → toast",
        fill="light_gold", h=24)
    y -= 8

    for section_name, prompts in structure:
        if y < Y0 + 50:
            page_footer(c, pg)
            pg += 1
            new_page(c)
            y = page_header(c, "05", f"Speech — {role} (continued)")

        c.setFillColor(C["rose_gold"])
        c.rect(X0, y - 14, TW, 14, stroke=0, fill=1)
        c.setFont("Helvetica-Bold", 8)
        c.setFillColor(white)
        c.drawString(X0 + 6, y - 10, section_name.upper())
        y -= 18

        for prompt in prompts:
            c.setFont("Helvetica", 7.5)
            c.setFillColor(C["mid"])
            c.drawString(X0 + 8, y, prompt)
            y -= 4
            y = write_lines(c, y, n=3, line_h=20)
            y -= 4

    page_footer(c, pg)
    return pg


def build_speeches(c: Canvas, pg: int) -> int:
    section_divider(c, "05", "Speech Outline Templates",
                    "Best Man · Maid of Honour · Father or Mother of the Bride/Groom")
    pg += 1

    pg = _speech_page(c, pg, "Best Man", [
        ("OPENING (30 seconds)", [
            "Introduce yourself and how you know the groom:",
            "A self-deprecating line to get a laugh (optional but effective):",
        ]),
        ("THE GROOM — WHO HE IS", [
            "One story that perfectly captures his character:",
            "What makes him an exceptional person / partner:",
        ]),
        ("WHEN HE MET THE BRIDE", [
            "How you knew this was different (his face, his behaviour, his words):",
            "A funny or touching moment from when you first saw them together:",
        ]),
        ("THE BRIDE — YOUR MESSAGE TO HER", [
            "What you most appreciate about who she is:",
            "Your message / advice / promise to her (on behalf of the groom):",
        ]),
        ("CLOSING TOAST", [
            "Your final wish for the couple:",
            "Toast line (raise glasses): \"Ladies and gentlemen, please be upstanding...\"",
        ]),
    ])
    pg += 1

    pg = _speech_page(c, pg, "Maid of Honour", [
        ("OPENING", [
            "Introduce yourself and your relationship with the bride:",
            "A warm or funny opening line:",
        ]),
        ("THE BRIDE — YOUR TRIBUTE", [
            "The quality you admire most about her (with a story):",
            "A memory you two share that shows who she is:",
        ]),
        ("ABOUT THE COUPLE", [
            "How you saw the relationship change her / what you noticed:",
            "Why you know they are perfect together:",
        ]),
        ("MESSAGE TO THE GROOM", [
            "Your one important thing he must always remember about her:",
        ]),
        ("CLOSING TOAST", [
            "Your wish for their future:",
            "Toast line:",
        ]),
    ])
    pg += 1

    pg = _speech_page(c, pg, "Father / Mother of the Bride (or Groom)", [
        ("OPENING", [
            "Welcome guests and introduce yourself:",
            "A line that captures what this day means to you:",
        ]),
        ("ABOUT YOUR CHILD", [
            "A childhood memory that captures who they are:",
            "The moment you realised they had grown up:",
        ]),
        ("ABOUT THE PARTNER", [
            "What you saw that made you know they were the right person:",
            "When you truly welcomed them into the family:",
        ]),
        ("ADVICE FOR THE COUPLE", [
            "One piece of wisdom for a long, happy marriage:",
            "Your hope for their future:",
        ]),
        ("CLOSING TOAST", [
            "Final message to both of them today:",
            "Toast line:",
        ]),
    ])

    return pg


# ─────────────────────────────────────────────────────────────────────
# TOOL 6: WEDDING MORNING SCHEDULE
# ─────────────────────────────────────────────────────────────────────

def build_morning_schedule(c: Canvas, pg: int) -> int:
    section_divider(c, "06", "Wedding Morning Schedule",
                    "Hour-by-hour getting-ready timeline")
    pg += 1

    new_page(c)
    y = page_header(c, "06", "Wedding Morning Schedule")
    y = heading(c, "GETTING READY — DETAILED TIMELINE", y)
    y = body_text(c,
        "Fill in your own times below, working backwards from your ceremony start time. "
        "Share this with your bridal party and hair/make-up team at least 2 weeks before "
        "the wedding.", y)
    y -= 8

    ceremony_box_h = 30
    c.setFillColor(C["hot_pink"])
    c.rect(X0, y - ceremony_box_h, TW, ceremony_box_h, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(white)
    c.drawString(X0 + 8, y - 8, "Ceremony Start Time:")
    c.setStrokeColor(white)
    c.setLineWidth(0.8)
    c.line(X0 + 180, y - 8, X0 + 340, y - 8)
    c.setFont("Helvetica", 8)
    c.drawString(X0 + 360, y - 8, "Ceremony Venue:")
    c.line(X0 + 470, y - 8, X1 - 4, y - 8)
    y -= ceremony_box_h + 10

    time_slots = [
        ("Wake up / morning routine", "Bride"),
        ("Breakfast / light snack", "All bridal party"),
        ("Hair begins — Bride", "Hair stylist"),
        ("Hair continues — Bridesmaids", "Hair stylist"),
        ("Make-Up begins — Bride", "MUA"),
        ("Make-Up continues — Bridesmaids", "MUA"),
        ("Photographer arrives", "Photographer"),
        ("Getting-ready photos begin", "Bride, bridal party"),
        ("Dress on / final touches", "Bride, MOH"),
        ("Bouquets delivered", "Florist"),
        ("Bridal party fully dressed", "All"),
        ("First look (if applicable)", "Couple"),
        ("Pre-ceremony photos — couple", "Photographer"),
        ("Pre-ceremony photos — bridal party", "Photographer"),
        ("Transport departs for venue", "All"),
        ("Bridal party arrives at venue", "All"),
        ("Final prep / touch-ups", "Bride"),
        ("CEREMONY BEGINS", "All"),
    ]

    col_1_w = TW * 0.14
    col_2_w = TW * 0.40
    col_3_w = TW * 0.25

    # header
    c.setFillColor(C["gold"])
    c.rect(X0, y - 16, TW, 16, stroke=0, fill=1)
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(white)
    c.drawString(X0 + 4, y - 11, "TIME")
    c.drawString(X0 + col_1_w + 4, y - 11, "ACTIVITY")
    c.drawString(X0 + col_1_w + col_2_w + 4, y - 11, "RESPONSIBLE")
    c.drawString(X0 + col_1_w + col_2_w + col_3_w + 4, y - 11, "NOTES")
    y -= 17

    for i, (activity, responsible) in enumerate(time_slots):
        if y < Y0 + 18:
            page_footer(c, pg)
            pg += 1
            new_page(c)
            y = page_header(c, "06", "Wedding Morning Schedule — continued")

        is_ceremony = activity == "CEREMONY BEGINS"
        fill = C["hot_pink"] if is_ceremony else (C["blush"] if i % 2 == 0 else C["white"])
        text_color = white if is_ceremony else C["dark"]

        c.setFillColor(fill)
        c.rect(X0, y - 18, TW, 18, stroke=0, fill=1)
        font = "Helvetica-Bold" if is_ceremony else "Helvetica"
        c.setFont(font, 8)
        c.setFillColor(HexColor("#FFFFFF") if is_ceremony else C["dark"])
        c.drawString(X0 + col_1_w + 4, y - 13, activity)
        c.setFont("Helvetica", 8)
        c.setFillColor(HexColor("#FFFFFF") if is_ceremony else C["mid"])
        c.drawString(X0 + col_1_w + col_2_w + 4, y - 13, responsible)
        # time field — blank line
        c.setStrokeColor(C["gold"] if is_ceremony else C["line"])
        c.setLineWidth(0.5)
        c.line(X0 + 4, y - 13, X0 + col_1_w - 4, y - 13)
        y -= 18

    page_footer(c, pg)
    return pg


# ─────────────────────────────────────────────────────────────────────
# TOOL 7: POST-WEDDING CHECKLIST
# ─────────────────────────────────────────────────────────────────────

def build_post_wedding(c: Canvas, pg: int) -> int:
    section_divider(c, "07", "Post-Wedding Checklist",
                    "Everything to do after the big day")
    pg += 1

    new_page(c)
    y = page_header(c, "07", "Post-Wedding To-Do Checklist")
    y = body_text(c,
        "The wedding is over — congratulations! But there is still plenty to take care of. "
        "Use this checklist over the weeks following your wedding to make sure nothing "
        "is forgotten.", y)
    y -= 6

    post_tasks = {
        "WITHIN 24 HOURS": [
            "Return any borrowed items (gown steamer, etc.)",
            "Ensure all gifts are safely stored",
            "Pass bridal bouquet to a florist for preservation (if desired)",
            "Tip any vendors not tipped on the day",
            "Eat something and rest — you deserve it!",
        ],
        "WITHIN 1 WEEK": [
            "Write and send personalised thank-you notes (aim for all within 3 months)",
            "Return rental items (suits, tuxedos, décor hire)",
            "Collect wedding dress from venue / bridal party",
            "Begin wedding dress preservation (dry cleaning, boxing)",
            "Download and back up all digital photos",
            "Post a selection of photos to social media (optional)",
            "Submit wedding announcement to newspaper (if desired)",
            "Review and tip vendors where applicable",
            "Collect any personal items left at the venue",
        ],
        "WITHIN 1 MONTH": [
            "Send thank-you cards to all gift givers",
            "Begin name change process (if applicable — see below)",
            "Review vendor contracts and release final payments",
            "Write reviews for vendors on Google, Etsy, social media",
            "Organise and store wedding paperwork and marriage certificate",
            "Share wedding photos with family",
            "Schedule anniversary dinner / tradition to start",
        ],
        "NAME CHANGE CHECKLIST": [
            "Marriage certificate (certified copy from registry office)",
            "Passport",
            "Driver's licence",
            "Electoral roll / voter registration",
            "Bank accounts (all financial institutions)",
            "Credit cards and loans",
            "Medicare / health insurance",
            "Social media accounts",
            "Email address / email signature",
            "Workplace HR records",
            "Tax authority records",
            "Superannuation / pension / retirement accounts",
            "Property deeds / rental agreements",
            "Vehicle registration",
            "Doctor, dentist, and other health providers",
            "Subscriptions and memberships",
        ],
        "ANNIVERSARY PLANNING": [
            "Book a restaurant for your 1-month anniversary",
            "Plan a first anniversary trip or special experience",
            "Write a letter to each other to open on your 1st anniversary",
            "Create a scrapbook or photo book",
            "Plant a tree or start a wedding anniversary tradition",
        ],
    }

    for section_name, tasks in post_tasks.items():
        if y < Y0 + 50:
            page_footer(c, pg)
            pg += 1
            new_page(c)
            y = page_header(c, "07", "Post-Wedding Checklist")

        y = heading(c, section_name, y, size=9)

        for task in tasks:
            if y < Y0 + 20:
                page_footer(c, pg)
                pg += 1
                new_page(c)
                y = page_header(c, "07", "Post-Wedding Checklist")
            y = checkbox_item(c, task, y)
            y -= 2

        y -= 8

    page_footer(c, pg)
    return pg


# ─────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    out = Path("output")
    out.mkdir(exist_ok=True)
    path = out / "Bold_Balanced_Wedding_Bible_Bonus_Toolkit.pdf"

    print("Building Bonus Toolkit PDF …")
    c = Canvas(str(path), pagesize=letter)
    c.setTitle("Bold & Balanced Wedding Bible — Bonus Toolkit")
    c.setAuthor("Marigold Bride")

    global _page_count
    _page_count = 0

    build_cover(c)
    pg = 1

    pg = build_emergency_kit(c, pg)
    pg += 1
    pg = build_tip_guide(c, pg)
    pg += 1
    pg = build_contacts_card(c, pg)
    pg += 1
    pg = build_vow_prompts(c, pg)
    pg += 1
    pg = build_speeches(c, pg)
    pg += 1
    pg = build_morning_schedule(c, pg)
    pg += 1
    pg = build_post_wedding(c, pg)

    c.save()
    print(f"  ✓ Saved: {path}  ({_page_count} pages)")
    print("\nDone!")


if __name__ == "__main__":
    main()
