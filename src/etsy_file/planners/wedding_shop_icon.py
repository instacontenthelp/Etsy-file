"""Generates Marigold Bride Etsy shop icon (500×500px) — floral-free base for Canva editing."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ── Palette ───────────────────────────────────────────────────────────────────
BG_DARK   = (12, 9, 7)
BG_MID    = (32, 24, 14)
BG_WARM   = (44, 32, 16)

GOLD_BRIGHT = (255, 215, 80)
GOLD_MID    = (245, 168, 36)
GOLD_DEEP   = (190, 118, 10)
PETAL_TIP   = (255, 250, 200)

WHITE    = (255, 255, 255)
CREAM    = (255, 248, 228)
IVORY    = (255, 252, 240)
GOLD_RING  = (210, 158, 24)
GOLD_RING2 = (255, 230, 120)

SIZE     = 500
OUT_PATH = Path("output/Marigold_Bride_Shop_Icon.png")

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def _blend(c1: tuple, c2: tuple, t: float) -> tuple:
    return tuple(int(c1[i] + (c2[i] - c1[i]) * max(0.0, min(1.0, t))) for i in range(3))


# ── Background ────────────────────────────────────────────────────────────────

def make_background() -> Image.Image:
    img  = Image.new("RGB", (SIZE, SIZE), BG_DARK)
    draw = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    for r in range(cx, 0, -1):
        t   = (1 - r / cx) ** 1.6
        col = _blend(BG_DARK, BG_WARM, t)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    return img


# ── Ornate border ─────────────────────────────────────────────────────────────

def draw_border(draw: ImageDraw.ImageDraw) -> None:
    cx = cy = SIZE // 2
    r1 = SIZE // 2 - 8
    r2 = r1 - 6
    r3 = r2 - 10

    draw.ellipse([cx - r1, cy - r1, cx + r1, cy + r1], outline=GOLD_RING,  width=6)
    draw.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=GOLD_RING2, width=2)
    draw.ellipse([cx - r3, cy - r3, cx + r3, cy + r3], outline=(*GOLD_MID, 120), width=1)

    # Diamond ornaments at N/E/S/W
    for deg in [0, 90, 180, 270]:
        ar    = math.radians(deg - 90)
        mx, my = cx + math.cos(ar) * (r1 - 4), cy + math.sin(ar) * (r1 - 4)
        s     = 7
        draw.polygon([(int(mx), int(my - s)), (int(mx + s), int(my)),
                      (int(mx), int(my + s)), (int(mx - s), int(my))], fill=GOLD_RING)

    # Dot ornaments at 45° positions
    for deg in [45, 135, 225, 315]:
        ar    = math.radians(deg - 90)
        mx, my = cx + math.cos(ar) * (r1 - 5), cy + math.sin(ar) * (r1 - 5)
        draw.ellipse([mx - 3, my - 3, mx + 3, my + 3], fill=GOLD_MID)


# ── Text ──────────────────────────────────────────────────────────────────────

def draw_name(img: Image.Image) -> None:
    layer = img.convert("RGBA")
    draw  = ImageDraw.Draw(layer)
    cx    = SIZE // 2

    f_marigold = _font(FONT_BOLD, 62)
    f_bride    = _font(FONT_BOLD, 74)

    b1 = draw.textbbox((0, 0), "MARIGOLD", font=f_marigold)
    b2 = draw.textbbox((0, 0), "BRIDE",    font=f_bride)
    w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
    w2, h2 = b2[2] - b2[0], b2[3] - b2[1]

    # Vertically centre the text block in the lower half (y 260–460)
    block_h = h1 + 10 + h2
    ty1 = (260 + 460 - block_h) // 2
    ty2 = ty1 + h1 + 10
    tx1 = cx - w1 // 2
    tx2 = cx - w2 // 2

    # Rule above MARIGOLD
    ry  = ty1 - 16
    hw  = 80
    draw.line([(cx - hw - 20, ry), (cx - 12, ry)], fill=(*GOLD_MID, 200), width=1)
    draw.line([(cx + 12, ry), (cx + hw + 20, ry)], fill=(*GOLD_MID, 200), width=1)
    s = 5
    draw.polygon([(cx, ry - s), (cx + s, ry), (cx, ry + s), (cx - s, ry)],
                 fill=(*GOLD_MID, 200))

    # "MARIGOLD" — gold shimmer
    for ox, oy, a in [(2, 3, 70), (1, 2, 90)]:
        draw.text((tx1 + ox, ty1 + oy), "MARIGOLD", font=f_marigold, fill=(0, 0, 0, a))
    draw.text((tx1 + 2, ty1 + 2), "MARIGOLD", font=f_marigold, fill=(*GOLD_DEEP,   220))
    draw.text((tx1 - 1, ty1 - 1), "MARIGOLD", font=f_marigold, fill=(*GOLD_MID,    235))
    draw.text((tx1,     ty1),     "MARIGOLD", font=f_marigold, fill=(*GOLD_BRIGHT,  255))
    draw.text((tx1 - 2, ty1 - 2), "MARIGOLD", font=f_marigold, fill=(*PETAL_TIP,    80))

    # "BRIDE" — white
    for ox, oy, a in [(2, 3, 65), (1, 2, 85)]:
        draw.text((tx2 + ox, ty2 + oy), "BRIDE", font=f_bride, fill=(0, 0, 0, a))
    draw.text((tx2 + 1, ty2 + 1), "BRIDE", font=f_bride, fill=(*CREAM,  230))
    draw.text((tx2,     ty2),     "BRIDE", font=f_bride, fill=(*WHITE,   255))
    draw.text((tx2 - 1, ty2 - 1), "BRIDE", font=f_bride, fill=(*IVORY,   70))

    # Rule below BRIDE
    ry2 = ty2 + h2 + 12
    draw.line([(cx - hw - 20, ry2), (cx - 12, ry2)], fill=(*GOLD_MID, 170), width=1)
    draw.line([(cx + 12, ry2), (cx + hw + 20, ry2)], fill=(*GOLD_MID, 170), width=1)
    draw.ellipse([cx - 4, ry2 - 4, cx + 4, ry2 + 4], fill=(*GOLD_MID, 170))

    img.paste(layer.convert("RGB"), (0, 0))


# ── Circular mask ─────────────────────────────────────────────────────────────

def apply_circle_mask(img: Image.Image) -> Image.Image:
    result = img.convert("RGBA")
    mask   = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, SIZE - 1, SIZE - 1], fill=255)
    result.putalpha(mask)
    return result


# ── Main ──────────────────────────────────────────────────────────────────────

def generate_icon() -> Path:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    img = make_background()
    draw_border(ImageDraw.Draw(img))
    draw_name(img)
    img = apply_circle_mask(img)
    img.save(OUT_PATH, "PNG")
    return OUT_PATH


if __name__ == "__main__":
    path = generate_icon()
    print(f"Icon saved → {path}")
