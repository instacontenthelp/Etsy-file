"""Generates Marigold Bride Etsy shop icon (500×500px)."""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ── Palette ───────────────────────────────────────────────────────────────────
BG_DARK   = (12, 9, 7)
BG_MID    = (32, 24, 14)
BG_WARM   = (42, 30, 16)

GOLD_BRIGHT  = (255, 215, 80)
GOLD_MID     = (245, 168, 36)
GOLD_DEEP    = (190, 118, 10)
PETAL_TIP    = (255, 250, 200)
PETAL_INNER  = (255, 237, 155)
CENTER_DARK  = (118, 52, 14)
CENTER_MID   = (158, 70, 12)
CENTER_LIGHT = (215, 118, 6)

LEAF_DARK  = (24, 58, 42)
LEAF_MID   = (32, 82, 56)
LEAF_LIGHT = (44, 108, 72)
LEAF_VEIN  = (18, 44, 32)

WHITE      = (255, 255, 255)
CREAM      = (255, 248, 228)
IVORY      = (255, 252, 240)
BLUSH      = (255, 220, 210)
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
    return tuple(int(c1[i] + (c2[i] - c1[i]) * max(0, min(1, t))) for i in range(3))


# ── Background — warm radial gradient ────────────────────────────────────────

def make_background() -> Image.Image:
    img = Image.new("RGB", (SIZE, SIZE), BG_DARK)
    draw = ImageDraw.Draw(img)
    cx = cy = SIZE // 2
    for r in range(cx, 0, -1):
        t = (1 - r / cx) ** 1.6
        col = _blend(BG_DARK, BG_WARM, t)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    return img


# ── Petal polygon ─────────────────────────────────────────────────────────────

def _petal_pts(cx: float, cy: float, length: float, width: float,
               angle_deg: float) -> list[tuple[int, int]]:
    angle = math.radians(angle_deg)
    perp  = angle + math.pi / 2
    pts: list[tuple[int, int]] = []
    steps = 22
    for i in range(steps + 1):
        t  = i / steps
        rp = math.sin(t * math.pi) * width * 0.5
        ra = t * length
        pts.append((int(cx + math.cos(angle) * ra + math.cos(perp) * rp),
                    int(cy + math.sin(angle) * ra + math.sin(perp) * rp)))
    for i in range(steps, -1, -1):
        t  = i / steps
        rp = math.sin(t * math.pi) * width * 0.5
        ra = t * length
        pts.append((int(cx + math.cos(angle) * ra - math.cos(perp) * rp),
                    int(cy + math.sin(angle) * ra - math.sin(perp) * rp)))
    return pts


# ── Leaf ──────────────────────────────────────────────────────────────────────

def _draw_leaf(draw: ImageDraw.ImageDraw, cx: float, cy: float,
               length: float, width: float, angle_deg: float) -> None:
    angle = math.radians(angle_deg)
    perp  = angle + math.pi / 2
    tip   = (cx + math.cos(angle) * length, cy + math.sin(angle) * length)
    mx    = cx + math.cos(angle) * length * 0.52
    my    = cy + math.sin(angle) * length * 0.52
    poly  = [
        (int(cx + math.cos(perp) * width * 0.42), int(cy + math.sin(perp) * width * 0.42)),
        (int(mx + math.cos(perp) * width * 0.92), int(my + math.sin(perp) * width * 0.92)),
        (int(tip[0]), int(tip[1])),
        (int(mx - math.cos(perp) * width * 0.92), int(my - math.sin(perp) * width * 0.92)),
        (int(cx - math.cos(perp) * width * 0.42), int(cy - math.sin(perp) * width * 0.42)),
    ]
    draw.polygon(poly, fill=LEAF_MID, outline=LEAF_DARK)
    draw.line([(int(cx), int(cy)),
               (int(tip[0] * 0.86 + cx * 0.14), int(tip[1] * 0.86 + cy * 0.14))],
              fill=LEAF_VEIN, width=1)
    # lateral veins
    for frac in [0.35, 0.58, 0.75]:
        vx = cx + math.cos(angle) * length * frac
        vy = cy + math.sin(angle) * length * frac
        vl = width * 0.42 * (1 - frac * 0.5)
        for side in [1, -1]:
            ex = vx + math.cos(perp) * vl * side
            ey = vy + math.sin(perp) * vl * side
            draw.line([(int(vx), int(vy)), (int(ex), int(ey))], fill=LEAF_VEIN, width=1)


# ── Marigold bloom ────────────────────────────────────────────────────────────

def draw_marigold(layer: Image.Image, cx: float, cy: float,
                  radius: float, rng: random.Random, rotation: float = 0.0) -> None:
    draw = ImageDraw.Draw(layer)

    # Guard petals (outermost)
    for i in range(15):
        angle = rotation + i * (360 / 15) + 12
        col   = _blend(GOLD_MID, GOLD_DEEP, rng.uniform(0.0, 0.4))
        pts   = _petal_pts(cx, cy, radius * 1.06, radius * 0.38, angle)
        draw.polygon(pts, fill=col, outline=_blend(col, (0, 0, 0), 0.28))
        ar = math.radians(angle)
        draw.line([(int(cx + math.cos(ar) * radius * 0.11),
                    int(cy + math.sin(ar) * radius * 0.11)),
                   (int(cx + math.cos(ar) * radius * 0.91),
                    int(cy + math.sin(ar) * radius * 0.91))],
                  fill=_blend(col, (0, 0, 0), 0.36), width=max(1, int(radius * 0.016)))

    # Mid ring
    for i in range(20):
        angle = rotation + i * (360 / 20) + rng.uniform(-4, 4)
        col   = _blend(GOLD_BRIGHT, GOLD_MID, rng.uniform(0.0, 0.5))
        pts   = _petal_pts(cx, cy, radius * 0.80, radius * 0.31, angle)
        draw.polygon(pts, fill=col, outline=_blend(col, (0, 0, 0), 0.20))
        ar = math.radians(angle)
        draw.line([(int(cx + math.cos(ar) * radius * 0.07),
                    int(cy + math.sin(ar) * radius * 0.07)),
                   (int(cx + math.cos(ar) * radius * 0.74),
                    int(cy + math.sin(ar) * radius * 0.74))],
                  fill=_blend(col, (0, 0, 0), 0.30), width=max(1, int(radius * 0.012)))

    # Inner ring
    for i in range(26):
        angle = rotation + i * (360 / 26) + rng.uniform(-3, 3)
        col   = _blend(PETAL_INNER, GOLD_BRIGHT, rng.uniform(0.0, 0.65))
        pts   = _petal_pts(cx, cy, radius * 0.54, radius * 0.21, angle)
        draw.polygon(pts, fill=col, outline=_blend(col, (0, 0, 0), 0.16))

    # Disc florets
    dr = radius * 0.21
    draw.ellipse([cx - dr, cy - dr, cx + dr, cy + dr], fill=CENTER_DARK)
    for _ in range(int(dr * 2.0)):
        fr = rng.uniform(0, dr * 0.84)
        fa = rng.uniform(0, 2 * math.pi)
        fx, fy = cx + math.cos(fa) * fr, cy + math.sin(fa) * fr
        fs = rng.uniform(dr * 0.07, dr * 0.15)
        draw.ellipse([fx - fs, fy - fs, fx + fs, fy + fs],
                     fill=_blend(CENTER_MID, CENTER_LIGHT, rng.uniform(0, 1)))
    hs = dr * 0.26
    draw.ellipse([cx - hs, cy - hs, cx + hs, cy + hs], fill=CENTER_LIGHT)


# ── Small bridal accent flower (5-petal white) ───────────────────────────────

def _draw_blossom(draw: ImageDraw.ImageDraw, cx: float, cy: float,
                  r: float, rng: random.Random, rotation: float = 0.0) -> None:
    for i in range(5):
        angle = rotation + i * 72
        col   = _blend(WHITE, CREAM, rng.uniform(0.0, 0.35))
        pts   = _petal_pts(cx, cy, r, r * 0.62, angle)
        draw.polygon(pts, fill=(*col, 210), outline=(*_blend(col, (200, 180, 160), 0.3), 160))
    # Centre
    draw.ellipse([cx - r * 0.22, cy - r * 0.22, cx + r * 0.22, cy + r * 0.22],
                 fill=(*GOLD_BRIGHT, 230))


# ── Trailing vine / stem ──────────────────────────────────────────────────────

def _draw_vine(draw: ImageDraw.ImageDraw,
               pts: list[tuple[float, float]], width: int = 2) -> None:
    for i in range(len(pts) - 1):
        x0, y0 = pts[i]
        x1, y1 = pts[i + 1]
        draw.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=LEAF_DARK, width=width)


# ── Ornate border ring ────────────────────────────────────────────────────────

def draw_border(draw: ImageDraw.ImageDraw) -> None:
    cx = cy = SIZE // 2
    r1 = SIZE // 2 - 8    # outer gold band
    r2 = r1 - 6
    r3 = r2 - 10          # inner thin line

    draw.ellipse([cx - r1, cy - r1, cx + r1, cy + r1], outline=GOLD_RING,  width=6)
    draw.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], outline=GOLD_RING2, width=2)
    draw.ellipse([cx - r3, cy - r3, cx + r3, cy + r3], outline=(*GOLD_MID, 120), width=1)

    # Diamond ornaments at N / S / E / W
    for deg in [0, 90, 180, 270]:
        ar = math.radians(deg - 90)
        mx, my = cx + math.cos(ar) * (r1 - 4), cy + math.sin(ar) * (r1 - 4)
        s = 7
        pts = [(mx, my - s), (mx + s, my), (mx, my + s), (mx - s, my)]
        draw.polygon([(int(x), int(y)) for x, y in pts], fill=GOLD_RING)

    # Small dot ornaments between the diamonds (45° positions)
    for deg in [45, 135, 225, 315]:
        ar = math.radians(deg - 90)
        mx, my = cx + math.cos(ar) * (r1 - 5), cy + math.sin(ar) * (r1 - 5)
        draw.ellipse([mx - 3, my - 3, mx + 3, my + 3], fill=GOLD_MID)


# ── Text — two-line MARIGOLD / BRIDE ─────────────────────────────────────────

def draw_name(img: Image.Image) -> None:
    layer = img.convert("RGBA")
    draw  = ImageDraw.Draw(layer)
    cx    = SIZE // 2

    f_marigold = _font(FONT_BOLD, 62)
    f_bride    = _font(FONT_BOLD, 74)
    f_small    = _font(FONT_REG,  19)

    # Measure both words
    b1 = draw.textbbox((0, 0), "MARIGOLD", font=f_marigold)
    b2 = draw.textbbox((0, 0), "BRIDE",    font=f_bride)
    w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
    w2, h2 = b2[2] - b2[0], b2[3] - b2[1]

    # Position: MARIGOLD sits at ~y=318, BRIDE below it
    ty1 = 318
    ty2 = ty1 + h1 + 6
    tx1 = cx - w1 // 2
    tx2 = cx - w2 // 2

    # ── thin decorative rule above MARIGOLD ──
    ry  = ty1 - 14
    hw  = 88
    draw.line([(cx - hw - 24, ry), (cx - 14, ry)], fill=(*GOLD_MID, 200), width=1)
    draw.line([(cx + 14, ry), (cx + hw + 24, ry)], fill=(*GOLD_MID, 200), width=1)
    # diamond at centre of rule
    s = 5
    draw.polygon([(cx, ry - s), (cx + s, ry), (cx, ry + s), (cx - s, ry)],
                 fill=(*GOLD_MID, 200))

    # ── "MARIGOLD" — layered gold shimmer ──
    for ox, oy, a in [(2, 3, 70), (1, 2, 90)]:
        draw.text((tx1 + ox, ty1 + oy), "MARIGOLD", font=f_marigold, fill=(0, 0, 0, a))
    draw.text((tx1 + 2, ty1 + 2), "MARIGOLD", font=f_marigold, fill=(*GOLD_DEEP,  220))
    draw.text((tx1 - 1, ty1 - 1), "MARIGOLD", font=f_marigold, fill=(*GOLD_MID,   235))
    draw.text((tx1,     ty1),     "MARIGOLD", font=f_marigold, fill=(*GOLD_BRIGHT, 255))
    draw.text((tx1 - 2, ty1 - 2), "MARIGOLD", font=f_marigold, fill=(*PETAL_TIP,   80))

    # ── "BRIDE" — white with soft glow ──
    for ox, oy, a in [(2, 3, 65), (1, 2, 85)]:
        draw.text((tx2 + ox, ty2 + oy), "BRIDE", font=f_bride, fill=(0, 0, 0, a))
    draw.text((tx2 + 1, ty2 + 1), "BRIDE", font=f_bride, fill=(*CREAM,  230))
    draw.text((tx2,     ty2),     "BRIDE", font=f_bride, fill=(*WHITE,   255))
    draw.text((tx2 - 1, ty2 - 1), "BRIDE", font=f_bride, fill=(*IVORY,   70))

    # ── thin rule below BRIDE ──
    ry2 = ty2 + h2 + 10
    draw.line([(cx - hw - 24, ry2), (cx - 14, ry2)], fill=(*GOLD_MID, 170), width=1)
    draw.line([(cx + 14, ry2), (cx + hw + 24, ry2)], fill=(*GOLD_MID, 170), width=1)
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
    rng = random.Random(77)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    img  = make_background()
    draw = ImageDraw.Draw(img)
    cx   = SIZE // 2

    # ── Bloom sits in upper half, centred at y≈185 ──
    bloom_cy = 178

    # Leaves fanning behind the bloom
    for angle_deg, length, width in [
        (-125, 72, 24), (-95, 80, 26), (-65, 76, 24),
        ( -45, 68, 22), ( 225, 70, 24), (255, 78, 25),
        (  285, 74, 23), (310, 66, 21),
    ]:
        lx = cx      + math.cos(math.radians(angle_deg)) * 52
        ly = bloom_cy + math.sin(math.radians(angle_deg)) * 52
        _draw_leaf(draw, lx, ly, length, width, angle_deg)

    # Trailing vine stems left and right from bloom base
    vine_pts_l = [(cx - 55, bloom_cy + 55),
                  (cx - 88, bloom_cy + 88),
                  (cx - 108, bloom_cy + 115)]
    vine_pts_r = [(cx + 55, bloom_cy + 55),
                  (cx + 88, bloom_cy + 88),
                  (cx + 108, bloom_cy + 115)]
    _draw_vine(draw, vine_pts_l, width=2)
    _draw_vine(draw, vine_pts_r, width=2)

    # Small leaves on trailing vines
    _draw_leaf(draw, cx - 88, bloom_cy + 88, 38, 16, -150)
    _draw_leaf(draw, cx + 88, bloom_cy + 88, 38, 16,  -30)

    # ── Main marigold bloom ──
    bloom_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw_marigold(bloom_layer, cx, bloom_cy, 112, rng, rotation=rng.uniform(0, 20))

    # Warm glow under bloom
    glow = bloom_layer.filter(ImageFilter.GaussianBlur(18))
    img_rgba = Image.alpha_composite(img.convert("RGBA"), glow)
    img_rgba = Image.alpha_composite(img_rgba, bloom_layer)
    img = img_rgba.convert("RGB")

    # ── Small white bridal blossoms (flanking bloom) ──
    blossom_layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    blossom_draw  = ImageDraw.Draw(blossom_layer, "RGBA")
    blossom_specs = [
        (cx - 142, bloom_cy - 12,  20, 18.0),
        (cx + 142, bloom_cy - 12,  20, 54.0),
        (cx - 118, bloom_cy + 60,  16,  9.0),
        (cx + 118, bloom_cy + 60,  16, 27.0),
        (cx - 158, bloom_cy + 40,  14, 36.0),
        (cx + 158, bloom_cy + 40,  14,  0.0),
    ]
    for bx, by, br, brot in blossom_specs:
        _draw_blossom(blossom_draw, bx, by, br, rng, rotation=brot)

    blossom_glow = blossom_layer.filter(ImageFilter.GaussianBlur(4))
    img_rgba = Image.alpha_composite(img.convert("RGBA"), blossom_glow)
    img_rgba = Image.alpha_composite(img_rgba, blossom_layer)
    img = img_rgba.convert("RGB")

    # ── Ornate gold border ──
    draw = ImageDraw.Draw(img)
    draw_border(draw)

    # ── Name text ──
    draw_name(img)

    # ── Circular mask ──
    img = apply_circle_mask(img)
    img.save(OUT_PATH, "PNG")
    return OUT_PATH


if __name__ == "__main__":
    path = generate_icon()
    print(f"Icon saved → {path}")
