"""Generates Marigold Bride Etsy shop icon (500×500px)."""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ── Palette ───────────────────────────────────────────────────────────────────
BG_DARK = (10, 8, 6)
BG_MID = (28, 22, 14)

GOLD_BRIGHT = (255, 213, 79)
GOLD_MID = (245, 166, 35)
GOLD_DEEP = (194, 120, 10)
ORANGE_HOT = (249, 115, 22)
PETAL_TIP = (255, 249, 196)
PETAL_INNER = (255, 236, 153)
CENTER_DARK = (120, 53, 15)
CENTER_MID = (161, 72, 12)
CENTER_LIGHT = (217, 119, 6)

LEAF_DARK = (26, 61, 46)
LEAF_MID = (34, 85, 60)
LEAF_VEIN = (20, 48, 36)

WHITE = (255, 255, 255)
CREAM = (255, 248, 230)
GOLD_RING = (212, 160, 28)

SIZE = 500
OUT_PATH = Path("output/Marigold_Bride_Shop_Icon.png")

FONT_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def _blend(c1: tuple, c2: tuple, t: float) -> tuple:
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


# ── Background ────────────────────────────────────────────────────────────────

def make_background() -> Image.Image:
    img = Image.new("RGB", (SIZE, SIZE), BG_DARK)
    draw = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    # Radial gradient: lighter warm centre
    for r in range(cx, 0, -1):
        t = 1 - r / cx
        col = _blend(BG_DARK, BG_MID, t * t)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    return img


# ── Petal ─────────────────────────────────────────────────────────────────────

def _petal_pts(cx: float, cy: float, length: float, width: float,
               angle_deg: float) -> list[tuple[int, int]]:
    angle = math.radians(angle_deg)
    perp = angle + math.pi / 2
    pts = []
    steps = 20
    for i in range(steps + 1):
        t = i / steps
        rp = math.sin(t * math.pi) * width * 0.5
        ra = t * length
        pts.append((int(cx + math.cos(angle) * ra + math.cos(perp) * rp),
                    int(cy + math.sin(angle) * ra + math.sin(perp) * rp)))
    for i in range(steps, -1, -1):
        t = i / steps
        rp = math.sin(t * math.pi) * width * 0.5
        ra = t * length
        pts.append((int(cx + math.cos(angle) * ra - math.cos(perp) * rp),
                    int(cy + math.sin(angle) * ra - math.sin(perp) * rp)))
    return pts


# ── Leaf ──────────────────────────────────────────────────────────────────────

def _draw_leaf(draw: ImageDraw.ImageDraw, cx: float, cy: float,
               length: float, width: float, angle_deg: float) -> None:
    angle = math.radians(angle_deg)
    perp = angle + math.pi / 2
    tip = (cx + math.cos(angle) * length, cy + math.sin(angle) * length)
    mid_x = cx + math.cos(angle) * length * 0.52
    mid_y = cy + math.sin(angle) * length * 0.52
    poly = [
        (int(cx + math.cos(perp) * width * 0.45), int(cy + math.sin(perp) * width * 0.45)),
        (int(mid_x + math.cos(perp) * width * 0.9), int(mid_y + math.sin(perp) * width * 0.9)),
        (int(tip[0]), int(tip[1])),
        (int(mid_x - math.cos(perp) * width * 0.9), int(mid_y - math.sin(perp) * width * 0.9)),
        (int(cx - math.cos(perp) * width * 0.45), int(cy - math.sin(perp) * width * 0.45)),
    ]
    draw.polygon(poly, fill=LEAF_MID, outline=LEAF_DARK)
    draw.line([(int(cx), int(cy)), (int(tip[0] * 0.88 + cx * 0.12), int(tip[1] * 0.88 + cy * 0.12))],
              fill=LEAF_VEIN, width=1)


# ── Marigold bloom ────────────────────────────────────────────────────────────

def draw_marigold(layer: Image.Image, cx: float, cy: float,
                  radius: float, rng: random.Random, rotation: float = 0.0) -> None:
    draw = ImageDraw.Draw(layer)

    # Outermost guard petals
    for i in range(14):
        angle = rotation + i * (360 / 14) + 13
        col = _blend(GOLD_MID, GOLD_DEEP, rng.uniform(0, 0.35))
        pts = _petal_pts(cx, cy, radius * 1.05, radius * 0.40, angle)
        draw.polygon(pts, fill=col, outline=_blend(col, (0, 0, 0), 0.3))
        ar = math.radians(angle)
        draw.line([(int(cx + math.cos(ar) * radius * 0.12),
                    int(cy + math.sin(ar) * radius * 0.12)),
                   (int(cx + math.cos(ar) * radius * 0.9),
                    int(cy + math.sin(ar) * radius * 0.9))],
                  fill=_blend(col, (0, 0, 0), 0.38), width=max(1, int(radius * 0.018)))

    # Mid ring
    for i in range(18):
        angle = rotation + i * (360 / 18) + rng.uniform(-4, 4)
        col = _blend(GOLD_BRIGHT, GOLD_MID, rng.uniform(0, 0.5))
        pts = _petal_pts(cx, cy, radius * 0.82, radius * 0.33, angle)
        draw.polygon(pts, fill=col, outline=_blend(col, (0, 0, 0), 0.22))
        ar = math.radians(angle)
        draw.line([(int(cx + math.cos(ar) * radius * 0.08),
                    int(cy + math.sin(ar) * radius * 0.08)),
                   (int(cx + math.cos(ar) * radius * 0.76),
                    int(cy + math.sin(ar) * radius * 0.76))],
                  fill=_blend(col, (0, 0, 0), 0.32), width=max(1, int(radius * 0.014)))

    # Inner ring
    for i in range(24):
        angle = rotation + i * (360 / 24) + rng.uniform(-3, 3)
        col = _blend(PETAL_INNER, GOLD_BRIGHT, rng.uniform(0, 0.6))
        pts = _petal_pts(cx, cy, radius * 0.56, radius * 0.22, angle)
        draw.polygon(pts, fill=col, outline=_blend(col, (0, 0, 0), 0.18))

    # Disc
    dr = radius * 0.22
    draw.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], fill=CENTER_DARK)
    for _ in range(int(dr * 1.8)):
        fr = rng.uniform(0, dr * 0.85)
        fa = rng.uniform(0, 2 * math.pi)
        fx, fy = cx + math.cos(fa) * fr, cy + math.sin(fa) * fr
        fs = rng.uniform(dr * 0.07, dr * 0.15)
        draw.ellipse([fx - fs, fy - fs, fx + fs, fy + fs],
                     fill=_blend(CENTER_MID, CENTER_LIGHT, rng.uniform(0, 1)))
    hs = dr * 0.28
    draw.ellipse([cx - hs, cy - hs, cx + hs, cy + hs], fill=CENTER_LIGHT)


# ── Gold decorative ring ──────────────────────────────────────────────────────

def draw_gold_ring(draw: ImageDraw.ImageDraw) -> None:
    cx = cy = SIZE // 2
    # Outer ring
    r_out = SIZE // 2 - 10
    r_in = r_out - 5
    draw.ellipse([cx - r_out, cy - r_out, cx + r_out, cy + r_out],
                 outline=GOLD_RING, width=5)
    # Inner thin ring
    r2 = r_in - 8
    draw.ellipse([cx - r2, cy - r2, cx + r2, cy + r2],
                 outline=(*GOLD_MID, 160), width=2)

    # Diamond tick marks at 12/3/6/9 o'clock
    for angle_deg in [0, 90, 180, 270]:
        ar = math.radians(angle_deg - 90)
        mx = cx + math.cos(ar) * (r_out - 3)
        my = cy + math.sin(ar) * (r_out - 3)
        s = 6
        pts = [(mx, my - s), (mx + s, my), (mx, my + s), (mx - s, my)]
        draw.polygon([(int(x), int(y)) for x, y in pts], fill=GOLD_RING)


# ── Monogram text ─────────────────────────────────────────────────────────────

def draw_monogram(img: Image.Image) -> None:
    layer = img.convert("RGBA")
    draw = ImageDraw.Draw(layer)
    cx = SIZE // 2

    font_m = _font(FONT_BOLD, 52)
    font_s = _font(FONT_REG, 22)

    # "MARIGOLD BRIDE" curved along bottom arc — simulate with straight text
    label = "MARIGOLD  BRIDE"
    bbox = draw.textbbox((0, 0), label, font=font_m)
    tw = bbox[2] - bbox[0]
    tx = cx - tw // 2
    ty = SIZE - 108

    # Shadow
    draw.text((tx + 1, ty + 2), label, font=font_m, fill=(*( 0, 0, 0), 90))
    # Gold shimmer
    draw.text((tx + 1, ty + 1), label, font=font_m, fill=(*GOLD_DEEP, 220))
    draw.text((tx - 1, ty - 1), label, font=font_m, fill=(*GOLD_MID, 230))
    draw.text((tx, ty), label, font=font_m, fill=(*GOLD_BRIGHT, 255))

    # Thin rule above text
    ry = ty - 10
    gap = tw // 2 + 18
    draw.line([(cx - gap, ry), (cx - 22, ry)], fill=(*GOLD_MID, 180), width=1)
    draw.line([(cx + 22, ry), (cx + gap, ry)], fill=(*GOLD_MID, 180), width=1)
    # Small dot centre
    draw.ellipse([cx - 4, ry - 4, cx + 4, ry + 4], fill=(*GOLD_MID, 180))

    img.paste(layer.convert("RGB"), (0, 0))


# ── Circular mask ─────────────────────────────────────────────────────────────

def apply_circle_mask(img: Image.Image) -> Image.Image:
    """Crop image to a circle with transparent outside (for PNG)."""
    result = img.convert("RGBA")
    mask = Image.new("L", (SIZE, SIZE), 0)
    mdraw = ImageDraw.Draw(mask)
    mdraw.ellipse([0, 0, SIZE - 1, SIZE - 1], fill=255)
    result.putalpha(mask)
    return result


# ── Main ──────────────────────────────────────────────────────────────────────

def generate_icon() -> Path:
    rng = random.Random(99)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    img = make_background()

    # ── Small accent leaves behind bloom ──
    draw = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    for angle, length, width in [
        (-50, 80, 28), (30, 72, 25), (140, 68, 24), (220, 75, 26),
        (-130, 65, 22), (80, 60, 20),
    ]:
        lx = cx + math.cos(math.radians(angle)) * 58
        ly = cy + math.sin(math.radians(angle)) * 58
        _draw_leaf(draw, lx, ly, length, width, angle)

    # ── Bloom on separate RGBA layer for glow ──
    bloom_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw_marigold(bloom_layer, cx, cy, 138, rng, rotation=rng.uniform(0, 18))

    glow = bloom_layer.filter(ImageFilter.GaussianBlur(14))
    img_rgba = Image.alpha_composite(img.convert("RGBA"), glow)
    img_rgba = Image.alpha_composite(img_rgba, bloom_layer)
    img = img_rgba.convert("RGB")

    # ── Gold ring overlay ──
    draw = ImageDraw.Draw(img)
    draw_gold_ring(draw)

    # ── Monogram ──
    draw_monogram(img)

    # ── Circular mask for transparent PNG ──
    img_circle = apply_circle_mask(img)

    # Also save a square version (some platforms need it)
    img_circle.save(OUT_PATH, "PNG")
    return OUT_PATH


if __name__ == "__main__":
    path = generate_icon()
    print(f"Icon saved → {path}")
