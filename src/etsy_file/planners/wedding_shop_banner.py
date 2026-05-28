"""Generates Marigold Bride Etsy shop banner (3360×840px)."""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

# ── Palette ───────────────────────────────────────────────────────────────────
BG_DARK = (10, 8, 6)
BG_MID = (22, 18, 12)

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
LEAF_LIGHT = (45, 110, 74)
LEAF_VEIN = (20, 48, 36)

WHITE = (255, 255, 255)
CREAM = (255, 248, 230)
GRAY_LIGHT = (200, 190, 175)
GRAY_MID = (150, 140, 125)
BLACK = (0, 0, 0)

# ── Sizes ─────────────────────────────────────────────────────────────────────
W, H = 3360, 840
OUT_PATH = Path("output/Marigold_Bride_Etsy_Banner.png")

FONT_PATH_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
FONT_PATH_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"


def _font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


# ── Background ────────────────────────────────────────────────────────────────

def draw_background(img: Image.Image) -> None:
    draw = ImageDraw.Draw(img)
    # Radial-ish gradient: dark edges, slightly warmer centre
    for y in range(H):
        t = y / H
        r = int(BG_DARK[0] + (BG_MID[0] - BG_DARK[0]) * math.sin(t * math.pi))
        g = int(BG_DARK[1] + (BG_MID[1] - BG_DARK[1]) * math.sin(t * math.pi))
        b = int(BG_DARK[2] + (BG_MID[2] - BG_DARK[2]) * math.sin(t * math.pi))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Subtle horizontal vignette strips left/right
    for x in range(280):
        alpha = int(80 * (1 - x / 280))
        draw.line([(x, 0), (x, H)], fill=(0, 0, 0, 0))
        # just darken via overlay
    # We'll handle vignette with a separate layer


def add_vignette(img: Image.Image) -> Image.Image:
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(vig)
    steps = 220
    for i in range(steps):
        t = i / steps
        alpha = int(160 * (1 - t) ** 2)
        draw.rectangle([i, i, W - i, H - i], outline=(0, 0, 0, alpha))
    base = img.convert("RGBA")
    base = Image.alpha_composite(base, vig)
    return base.convert("RGB")


# ── Leaf helpers ──────────────────────────────────────────────────────────────

def _leaf_poly(cx: float, cy: float, length: float, width: float, angle_deg: float) -> list[tuple[int, int]]:
    """Return polygon points for a leaf shape."""
    angle = math.radians(angle_deg)
    perp = angle + math.pi / 2
    tip = (cx + math.cos(angle) * length, cy + math.sin(angle) * length)
    base_l = (cx + math.cos(perp) * width * 0.5, cy + math.sin(perp) * width * 0.5)
    base_r = (cx - math.cos(perp) * width * 0.5, cy - math.sin(perp) * width * 0.5)
    # Mid bulge points
    mid_x = cx + math.cos(angle) * length * 0.55
    mid_y = cy + math.sin(angle) * length * 0.55
    left_x = mid_x + math.cos(perp) * width * 0.85
    left_y = mid_y + math.sin(perp) * width * 0.85
    right_x = mid_x - math.cos(perp) * width * 0.85
    right_y = mid_y - math.sin(perp) * width * 0.85
    return [
        (int(base_l[0]), int(base_l[1])),
        (int(left_x), int(left_y)),
        (int(tip[0]), int(tip[1])),
        (int(right_x), int(right_y)),
        (int(base_r[0]), int(base_r[1])),
    ]


def draw_leaf(draw: ImageDraw.ImageDraw, cx: float, cy: float,
              length: float, width: float, angle_deg: float, alpha_img: Image.Image) -> None:
    poly = _leaf_poly(cx, cy, length, width, angle_deg)
    draw.polygon(poly, fill=LEAF_MID, outline=LEAF_DARK)
    # vein: centre line
    angle = math.radians(angle_deg)
    tip_x = cx + math.cos(angle) * length
    tip_y = cy + math.sin(angle) * length
    draw.line([(int(cx), int(cy)), (int(tip_x * 0.9 + cx * 0.1), int(tip_y * 0.9 + cy * 0.1))],
              fill=LEAF_VEIN, width=2)
    # lateral veins
    for frac in [0.3, 0.5, 0.65, 0.78]:
        vx = cx + math.cos(angle) * length * frac
        vy = cy + math.sin(angle) * length * frac
        perp = angle + math.pi / 2
        vlen = width * 0.45 * (1 - frac * 0.6)
        for side in [1, -1]:
            ex = vx + math.cos(perp) * vlen * side
            ey = vy + math.sin(perp) * vlen * side
            draw.line([(int(vx), int(vy)), (int(ex), int(ey))], fill=LEAF_VEIN, width=1)


# ── Petal helpers ─────────────────────────────────────────────────────────────

def _petal_points(cx: float, cy: float, length: float, width: float,
                  angle_deg: float, tip_curve: float = 0.0) -> list[tuple[int, int]]:
    """Rounded petal as polygon approximation."""
    angle = math.radians(angle_deg)
    perp = angle + math.pi / 2
    pts = []
    # Build half-petal outline in polar steps then mirror
    steps = 18
    for i in range(steps + 1):
        t = i / steps
        # radial distance: 0→peak at ~0.15 width, then narrows to tip
        r_perp = math.sin(t * math.pi) * width * 0.5
        r_along = t * length
        # slight inward curve near base, tip rounds off
        r_along += tip_curve * math.sin(t * math.pi * 2) * length * 0.04
        px = cx + math.cos(angle) * r_along + math.cos(perp) * r_perp
        py = cy + math.sin(angle) * r_along + math.sin(perp) * r_perp
        pts.append((int(px), int(py)))
    for i in range(steps, -1, -1):
        t = i / steps
        r_perp = math.sin(t * math.pi) * width * 0.5
        r_along = t * length
        r_along += tip_curve * math.sin(t * math.pi * 2) * length * 0.04
        px = cx + math.cos(angle) * r_along - math.cos(perp) * r_perp
        py = cy + math.sin(angle) * r_along - math.sin(perp) * r_perp
        pts.append((int(px), int(py)))
    return pts


def _blend_color(c1: tuple, c2: tuple, t: float) -> tuple:
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def draw_marigold(layer: Image.Image, cx: float, cy: float,
                  radius: float, rng: random.Random, rotation: float = 0.0) -> None:
    """Draw a botanical marigold bloom onto `layer`."""
    draw = ImageDraw.Draw(layer)

    # ── outermost guard petals (slightly greenish-gold) ──
    n_outer = 16
    outer_len = radius * 1.05
    outer_w = radius * 0.38
    for i in range(n_outer):
        angle = rotation + i * (360 / n_outer) + 11
        tip_col = _blend_color(GOLD_MID, GOLD_DEEP, rng.uniform(0.0, 0.3))
        base_col = _blend_color(LEAF_MID, GOLD_DEEP, 0.5)
        color = _blend_color(base_col, tip_col, 0.6)
        pts = _petal_points(cx, cy, outer_len, outer_w, angle, tip_curve=rng.uniform(-0.5, 0.5))
        draw.polygon(pts, fill=color, outline=_blend_color(color, (0, 0, 0), 0.25))
        # mid vein
        angle_r = math.radians(angle)
        tx = cx + math.cos(angle_r) * outer_len * 0.88
        ty = cy + math.sin(angle_r) * outer_len * 0.88
        vein_col = _blend_color(color, (0, 0, 0), 0.35)
        draw.line([(int(cx + math.cos(angle_r) * radius * 0.12), int(cy + math.sin(angle_r) * radius * 0.12)),
                   (int(tx), int(ty))], fill=vein_col, width=max(1, int(radius * 0.012)))

    # ── second ring of petals ──
    n_mid = 20
    mid_len = radius * 0.82
    mid_w = radius * 0.32
    for i in range(n_mid):
        angle = rotation + i * (360 / n_mid) + rng.uniform(-4, 4)
        t = rng.uniform(0.0, 0.5)
        color = _blend_color(GOLD_BRIGHT, GOLD_MID, t)
        pts = _petal_points(cx, cy, mid_len, mid_w, angle, tip_curve=rng.uniform(-0.3, 0.8))
        draw.polygon(pts, fill=color, outline=_blend_color(color, (0, 0, 0), 0.20))
        angle_r = math.radians(angle)
        tx = cx + math.cos(angle_r) * mid_len * 0.85
        ty = cy + math.sin(angle_r) * mid_len * 0.85
        vein_col = _blend_color(color, (0, 0, 0), 0.30)
        draw.line([(int(cx + math.cos(angle_r) * radius * 0.08), int(cy + math.sin(angle_r) * radius * 0.08)),
                   (int(tx), int(ty))], fill=vein_col, width=max(1, int(radius * 0.010)))

    # ── inner dense ring ──
    n_inner = 26
    inner_len = radius * 0.56
    inner_w = radius * 0.22
    for i in range(n_inner):
        angle = rotation + i * (360 / n_inner) + rng.uniform(-3, 3)
        t = rng.uniform(0.0, 0.6)
        color = _blend_color(PETAL_INNER, GOLD_BRIGHT, t)
        pts = _petal_points(cx, cy, inner_len, inner_w, angle)
        draw.polygon(pts, fill=color, outline=_blend_color(color, (0, 0, 0), 0.18))

    # ── disc florets (the bumpy center) ──
    disc_r = radius * 0.24
    # filled disc
    draw.ellipse([cx - disc_r, cy - disc_r, cx + disc_r, cy + disc_r],
                 fill=CENTER_DARK, outline=CENTER_MID)
    # tiny floret bumps
    floret_count = int(disc_r * 1.6)
    for _ in range(floret_count):
        fr = rng.uniform(0, disc_r * 0.82)
        fa = rng.uniform(0, 2 * math.pi)
        fx = cx + math.cos(fa) * fr
        fy = cy + math.sin(fa) * fr
        fs = rng.uniform(disc_r * 0.06, disc_r * 0.14)
        col = _blend_color(CENTER_MID, CENTER_LIGHT, rng.uniform(0, 1))
        draw.ellipse([fx - fs, fy - fs, fx + fs, fy + fs], fill=col)

    # centre bright highlight
    hs = disc_r * 0.28
    draw.ellipse([cx - hs, cy - hs, cx + hs, cy + hs], fill=CENTER_LIGHT)


# ── Stem / branch helpers ──────────────────────────────────────────────────────

def draw_stem(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int,
              width: int = 4) -> None:
    draw.line([(x0, y0), (x1, y1)], fill=LEAF_DARK, width=width)


# ── Full floral cluster ────────────────────────────────────────────────────────

def draw_cluster(base: Image.Image, bloom_x: float, bloom_y: float,
                 main_r: float, rng: random.Random, flip: bool = False) -> None:
    """Draw a marigold cluster with stems, leaves, and blooms."""
    draw = ImageDraw.Draw(base)
    flip_sign = -1 if flip else 1

    # Main stem
    stem_base_x = int(bloom_x - flip_sign * main_r * 0.3)
    stem_base_y = int(bloom_y + main_r * 3.2)
    draw_stem(draw, stem_base_x, stem_base_y, int(bloom_x), int(bloom_y + main_r * 0.3),
              width=max(3, int(main_r * 0.065)))

    # Leaves along stem
    for frac, leaf_side, leaf_angle_off in [(0.35, 1, 40), (0.55, -1, -35), (0.72, 1, 38)]:
        lx = stem_base_x + (bloom_x - stem_base_x) * frac
        ly = stem_base_y + (bloom_y - stem_base_y) * frac
        leaf_angle = (-70 + leaf_angle_off * leaf_side * flip_sign)
        draw_leaf(draw, lx, ly, main_r * rng.uniform(0.55, 0.75),
                  main_r * rng.uniform(0.28, 0.38), leaf_angle, base)

    # Side buds
    bud_offsets = [
        (flip_sign * main_r * 1.55, -main_r * 0.5, main_r * 0.55),
        (-flip_sign * main_r * 0.9, -main_r * 1.1, main_r * 0.42),
    ]
    for dx, dy, br in bud_offsets:
        bx, by = bloom_x + dx, bloom_y + dy
        draw_stem(draw, int(bloom_x), int(bloom_y),
                  int(bx), int(by + br * 0.3), width=max(2, int(main_r * 0.04)))
        # small leaf on bud stem
        lx2, ly2 = (bloom_x + bx) / 2, (bloom_y + by) / 2
        draw_leaf(draw, lx2, ly2, br * 0.5, br * 0.25,
                  rng.uniform(-60, -30) * flip_sign, base)

    # Draw blooms on a separate RGBA layer for glow
    bloom_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_marigold(bloom_layer, bloom_x, bloom_y, main_r, rng,
                  rotation=rng.uniform(0, 22))
    for dx, dy, br in bud_offsets:
        draw_marigold(bloom_layer, bloom_x + dx, bloom_y + dy, br, rng,
                      rotation=rng.uniform(0, 30))

    # Soft glow under blooms
    glow = bloom_layer.filter(ImageFilter.GaussianBlur(radius=int(main_r * 0.35)))
    # Tint glow gold
    glow_tinted = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_tinted.paste(glow, (0, 0))
    base_rgba = base.convert("RGBA")
    base_rgba = Image.alpha_composite(base_rgba, glow_tinted)
    base_rgba = Image.alpha_composite(base_rgba, bloom_layer)
    # paste back
    base.paste(base_rgba.convert("RGB"), (0, 0))


# ── Scattered petals ───────────────────────────────────────────────────────────

def draw_scattered_petals(draw: ImageDraw.ImageDraw, rng: random.Random) -> None:
    for _ in range(55):
        px = rng.uniform(0, W)
        py = rng.uniform(0, H)
        ang = rng.uniform(0, 360)
        plen = rng.uniform(14, 48)
        pw = rng.uniform(7, 22)
        t = rng.uniform(0, 1)
        col = _blend_color(GOLD_MID, PETAL_TIP, t)
        alpha = rng.randint(55, 140)
        pts = _petal_points(px, py, plen, pw, ang)
        # Draw to RGBA manually
        draw.polygon(pts, fill=(*col, alpha))


def draw_gold_dust(draw: ImageDraw.ImageDraw, rng: random.Random) -> None:
    """Tiny gold specks for shimmer."""
    for _ in range(320):
        x = rng.uniform(0, W)
        y = rng.uniform(0, H)
        r = rng.uniform(0.8, 3.5)
        t = rng.uniform(0.3, 1.0)
        col = _blend_color(GOLD_MID, GOLD_BRIGHT, t)
        alpha = rng.randint(30, 110)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(*col, alpha))


# ── Decorative text rule ───────────────────────────────────────────────────────

def draw_rule(draw: ImageDraw.ImageDraw, y: int, x_left: int, x_right: int,
              color: tuple = GOLD_MID, thickness: int = 2) -> None:
    draw.line([(x_left, y), (x_right, y)], fill=color, width=thickness)


def draw_diamond_ornament(draw: ImageDraw.ImageDraw, cx: int, cy: int,
                           size: int = 8, color: tuple = GOLD_MID) -> None:
    pts = [(cx, cy - size), (cx + size, cy), (cx, cy + size), (cx - size, cy)]
    draw.polygon(pts, fill=color)


# ── Text ──────────────────────────────────────────────────────────────────────

def draw_text_layer(img: Image.Image) -> None:
    # Work on RGBA so we can use alpha
    layer = img.convert("RGBA")
    draw = ImageDraw.Draw(layer)

    cx = W // 2

    # ── brand name ──
    font_main = _font(FONT_PATH_BOLD, 210)
    font_bride = _font(FONT_PATH_BOLD, 160)
    font_tag = _font(FONT_PATH_REG, 56)
    font_small = _font(FONT_PATH_REG, 44)

    # "MARIGOLD" — gold gradient effect via multiple shadow passes
    text_main = "MARIGOLD"
    bbox = draw.textbbox((0, 0), text_main, font=font_main)
    tw = bbox[2] - bbox[0]
    tx = cx - tw // 2
    ty = 230

    # Shadow
    for ox, oy, alpha in [(-4, 6, 60), (-2, 3, 80), (0, 4, 50)]:
        draw.text((tx + ox, ty + oy), text_main, font=font_main, fill=(*BLACK, alpha))

    # Gold shimmer: draw three times with slight offsets in light→dark gold
    draw.text((tx + 2, ty + 2), text_main, font=font_main, fill=(*GOLD_DEEP, 220))
    draw.text((tx - 1, ty - 1), text_main, font=font_main, fill=(*GOLD_MID, 230))
    draw.text((tx, ty), text_main, font=font_main, fill=(*GOLD_BRIGHT, 255))
    # Highlight stroke (top-left catch-light)
    draw.text((tx - 2, ty - 2), text_main, font=font_main, fill=(*PETAL_TIP, 90))

    # ── "B R I D E" with letter spacing simulation ──
    text_bride = "B  R  I  D  E"
    bbox2 = draw.textbbox((0, 0), text_bride, font=font_bride)
    tw2 = bbox2[2] - bbox2[0]
    tx2 = cx - tw2 // 2
    ty2 = ty + (bbox[3] - bbox[1]) - 18

    draw.text((tx2 + 2, ty2 + 3), text_bride, font=font_bride, fill=(*BLACK, 100))
    draw.text((tx2, ty2), text_bride, font=font_bride, fill=(*WHITE, 255))

    # ── decorative rule with diamonds ──
    rule_y = ty2 + (bbox2[3] - bbox2[1]) + 28
    gap = 260
    draw_rule(draw, rule_y, cx - gap - 180, cx - gap, GOLD_MID, 2)
    draw_diamond_ornament(draw, cx - gap, rule_y, 7, GOLD_MID)
    draw_rule(draw, rule_y, cx - gap + 14, cx + gap - 14, GOLD_MID, 2)
    draw_diamond_ornament(draw, cx + gap, rule_y, 7, GOLD_MID)
    draw_rule(draw, rule_y, cx + gap + 14, cx + gap + 180, GOLD_MID, 2)

    # ── tagline ──
    tagline = "Wedding Planning Made Beautiful"
    bbox3 = draw.textbbox((0, 0), tagline, font=font_tag)
    tw3 = bbox3[2] - bbox3[0]
    tx3 = cx - tw3 // 2
    ty3 = rule_y + 22
    draw.text((tx3 + 1, ty3 + 2), tagline, font=font_tag, fill=(*BLACK, 80))
    draw.text((tx3, ty3), tagline, font=font_tag, fill=(*CREAM, 210))

    # ── sub-tag ──
    subtag = "Digital Planners · Printables · Wedding Templates"
    bbox4 = draw.textbbox((0, 0), subtag, font=font_small)
    tw4 = bbox4[2] - bbox4[0]
    tx4 = cx - tw4 // 2
    ty4 = ty3 + (bbox3[3] - bbox3[1]) + 14
    draw.text((tx4, ty4), subtag, font=font_small, fill=(*GRAY_LIGHT, 185))

    img.paste(layer.convert("RGB"), (0, 0))


# ── Main ──────────────────────────────────────────────────────────────────────

def generate_banner() -> Path:
    rng = random.Random(42)
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Base image
    img = Image.new("RGB", (W, H), BG_DARK)
    draw_background(img)

    # ── Floral clusters ──────────────────────────────────────────────────────
    # Left large cluster
    draw_cluster(img, 390, 440, main_r=158, rng=rng, flip=False)

    # Right large cluster
    draw_cluster(img, W - 390, 440, main_r=152, rng=rng, flip=True)

    # Left accent cluster (smaller, partially off-edge)
    draw_cluster(img, 105, 560, main_r=90, rng=rng, flip=False)

    # Right accent cluster
    draw_cluster(img, W - 105, 560, main_r=88, rng=rng, flip=True)

    # Small blooms near centre for depth
    bloom_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_marigold(bloom_layer, W // 2 - 820, 760, 54, rng, rotation=15)
    draw_marigold(bloom_layer, W // 2 + 820, 760, 50, rng, rotation=5)
    glow_small = bloom_layer.filter(ImageFilter.GaussianBlur(18))
    img_rgba = Image.alpha_composite(img.convert("RGBA"), glow_small)
    img_rgba = Image.alpha_composite(img_rgba, bloom_layer)
    img = img_rgba.convert("RGB")

    # ── Scattered petals & dust ──────────────────────────────────────────────
    petal_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(petal_layer, "RGBA")
    draw_scattered_petals(pdraw, rng)
    draw_gold_dust(pdraw, rng)
    petal_blur = petal_layer.filter(ImageFilter.GaussianBlur(1.2))
    img = Image.alpha_composite(img.convert("RGBA"), petal_blur).convert("RGB")

    # ── Vignette ─────────────────────────────────────────────────────────────
    img = add_vignette(img)

    # ── Text ─────────────────────────────────────────────────────────────────
    draw_text_layer(img)

    # ── Final subtle sharpening ───────────────────────────────────────────────
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=115, threshold=3))

    img.save(OUT_PATH, "PNG", dpi=(144, 144))
    return OUT_PATH


if __name__ == "__main__":
    path = generate_banner()
    print(f"Banner saved → {path}")
