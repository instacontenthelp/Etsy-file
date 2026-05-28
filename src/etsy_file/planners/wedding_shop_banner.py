"""Generates Marigold Bride Etsy shop banner (3360×840px) — floral-free base for Canva editing."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ── Palette ───────────────────────────────────────────────────────────────────
BG_DARK   = (10, 8, 6)
BG_MID    = (28, 20, 10)

GOLD_BRIGHT = (255, 213, 79)
GOLD_MID    = (245, 166, 35)
GOLD_DEEP   = (194, 120, 10)
PETAL_TIP   = (255, 249, 196)

WHITE      = (255, 255, 255)
CREAM      = (255, 248, 230)
GRAY_LIGHT = (200, 190, 175)

W, H     = 3360, 840
OUT_PATH = Path("output/Marigold_Bride_Etsy_Banner.png")

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def _blend(c1: tuple, c2: tuple, t: float) -> tuple:
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


# ── Background ────────────────────────────────────────────────────────────────

def draw_background(img: Image.Image) -> None:
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t   = math.sin(y / H * math.pi)
        col = _blend(BG_DARK, BG_MID, t)
        draw.line([(0, y), (W, y)], fill=col)


def add_vignette(img: Image.Image) -> Image.Image:
    vig  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(vig)
    for i in range(240):
        alpha = int(170 * (1 - i / 240) ** 2)
        draw.rectangle([i, i, W - i, H - i], outline=(0, 0, 0, alpha))
    base = Image.alpha_composite(img.convert("RGBA"), vig)
    return base.convert("RGB")


# ── Decorative rules & ornaments ─────────────────────────────────────────────

def draw_diamond(draw: ImageDraw.ImageDraw, cx: int, cy: int,
                 size: int = 8, color: tuple = GOLD_MID) -> None:
    pts = [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)]
    draw.polygon(pts, fill=color)


def draw_text_layer(img: Image.Image) -> None:
    layer = img.convert("RGBA")
    draw  = ImageDraw.Draw(layer)
    cx    = W // 2

    font_main  = _font(FONT_BOLD, 210)
    font_bride = _font(FONT_BOLD, 160)
    font_tag   = _font(FONT_REG,  56)
    font_small = _font(FONT_REG,  44)

    # ── "MARIGOLD" ──
    bbox = draw.textbbox((0, 0), "MARIGOLD", font=font_main)
    tw   = bbox[2] - bbox[0]
    tx   = cx - tw // 2
    ty   = 230

    for ox, oy, a in [(-4, 6, 60), (-2, 3, 80)]:
        draw.text((tx + ox, ty + oy), "MARIGOLD", font=font_main, fill=(0, 0, 0, a))
    draw.text((tx + 2, ty + 2), "MARIGOLD", font=font_main, fill=(*GOLD_DEEP,   220))
    draw.text((tx - 1, ty - 1), "MARIGOLD", font=font_main, fill=(*GOLD_MID,    230))
    draw.text((tx,     ty),     "MARIGOLD", font=font_main, fill=(*GOLD_BRIGHT,  255))
    draw.text((tx - 2, ty - 2), "MARIGOLD", font=font_main, fill=(*PETAL_TIP,    90))

    # ── "B R I D E" ──
    text_bride = "B  R  I  D  E"
    bbox2 = draw.textbbox((0, 0), text_bride, font=font_bride)
    tw2   = bbox2[2] - bbox2[0]
    tx2   = cx - tw2 // 2
    ty2   = ty + (bbox[3] - bbox[1]) - 18

    draw.text((tx2 + 2, ty2 + 3), text_bride, font=font_bride, fill=(0, 0, 0, 100))
    draw.text((tx2,     ty2),     text_bride, font=font_bride, fill=(*WHITE, 255))

    # ── Decorative rule with diamonds ──
    rule_y = ty2 + (bbox2[3] - bbox2[1]) + 28
    gap    = 260
    draw.line([(cx - gap - 180, rule_y), (cx - gap, rule_y)],      fill=(*GOLD_MID, 220), width=2)
    draw_diamond(draw, cx - gap, rule_y, 7, GOLD_MID)
    draw.line([(cx - gap + 14,  rule_y), (cx + gap - 14, rule_y)], fill=(*GOLD_MID, 220), width=2)
    draw_diamond(draw, cx + gap, rule_y, 7, GOLD_MID)
    draw.line([(cx + gap + 14,  rule_y), (cx + gap + 180, rule_y)], fill=(*GOLD_MID, 220), width=2)

    # ── Tagline ──
    bbox3 = draw.textbbox((0, 0), "Wedding Planning Made Beautiful", font=font_tag)
    tw3   = bbox3[2] - bbox3[0]
    tx3   = cx - tw3 // 2
    ty3   = rule_y + 22
    draw.text((tx3 + 1, ty3 + 2), "Wedding Planning Made Beautiful", font=font_tag,  fill=(0, 0, 0, 80))
    draw.text((tx3,     ty3),     "Wedding Planning Made Beautiful", font=font_tag,  fill=(*CREAM, 210))

    # ── Sub-tag ──
    subtag = "Digital Planners · Printables · Wedding Templates"
    bbox4  = draw.textbbox((0, 0), subtag, font=font_small)
    tw4    = bbox4[2] - bbox4[0]
    tx4    = cx - tw4 // 2
    ty4    = ty3 + (bbox3[3] - bbox3[1]) + 14
    draw.text((tx4, ty4), subtag, font=font_small, fill=(*GRAY_LIGHT, 185))

    img.paste(layer.convert("RGB"), (0, 0))


# ── Main ──────────────────────────────────────────────────────────────────────

def generate_banner() -> Path:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    img = Image.new("RGB", (W, H), BG_DARK)
    draw_background(img)
    img = add_vignette(img)
    draw_text_layer(img)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=3))

    img.save(OUT_PATH, "PNG", dpi=(144, 144))
    return OUT_PATH


if __name__ == "__main__":
    path = generate_banner()
    print(f"Banner saved → {path}")
