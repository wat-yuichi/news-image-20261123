#!/usr/bin/env python3
"""Compose entry.png for the make.fun news-image-20261123 bounty:
one newspaper-style page summing up the world news of Monday,
23 November 2026.

Layout: a masthead carrying the date in large type, six story cards
in a 2-by-3 grid (war in Ukraine, war in Sudan, Korean politics,
Armenian diplomacy, a US tech lawsuit, UN AI governance), and a dark
ticker band with four shorter items from the same day.

All artwork is drawn here with Pillow: coloured badges hold a small
white pictogram per story, and every word is set in a real font file
so the page stays readable when scaled down to a few hundred pixels.
The script refuses to finish unless the result is within the bounty
limits (at most 1024x1024 px and 1 MiB).

Reporting behind each panel is listed in NEWS.md; wording was
cross-checked against at least two outlets on 24 November 2026.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (247, 243, 234)
INK = (24, 24, 28)
GREY = (70, 70, 76)
CARD_BG = (255, 255, 252)
CARD_LINE = (205, 198, 182)
MASTHEAD = (18, 24, 40)
CREAM = (240, 236, 224)
ACCENT = (166, 38, 30)
GOLD = (255, 205, 84)
FLAME = (255, 140, 54)

NOTO = Path("/usr/share/fonts/truetype/noto")
F_SERIF = str(NOTO / "NotoSerif-Black.ttf")
F_BLACK = str(NOTO / "NotoSans-Black.ttf")
F_BOLD = str(NOTO / "NotoSans-Bold.ttf")
F_REG = str(NOTO / "NotoSans-Regular.ttf")


def load(size, path=F_REG):
    return ImageFont.truetype(path, size)


def lines_for(draw, text, fnt, width):
    """Split `text` into lines that each fit `width` pixels."""
    out, pending = [], ""
    for word in text.split():
        trial = word if not pending else pending + " " + word
        if draw.textlength(trial, font=fnt) <= width:
            pending = trial
        else:
            out.append(pending)
            pending = word
    if pending:
        out.append(pending)
    return out


def stack(draw, x, y, text, fnt, fill, width, leading):
    """Draw wrapped text; return the y just below its last line."""
    for line in lines_for(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


# ------------------------------------------------------------------
# Pictograms.  Each takes (draw, cx, cy, r, fg) and draws in white
# (fg) inside a coloured badge; small gold/flame accents are allowed.
# ------------------------------------------------------------------

def pic_rail_power(d, cx, cy, r, fg):
    """A pylon and a rail line under a lightning strike: Ukraine."""
    # pylon: two legs, cross arms
    top = cy - r * 0.85
    d.line([cx - r * 0.42, cy + r * 0.55, cx - r * 0.1, top], fill=fg, width=5)
    d.line([cx + r * 0.42, cy + r * 0.55, cx + r * 0.1, top], fill=fg, width=5)
    d.line([cx - r * 0.3, cy + r * 0.05, cx + r * 0.32, cy + r * 0.05], fill=fg, width=4)
    d.line([cx - r * 0.62, cy - r * 0.38, cx + r * 0.64, cy - r * 0.38], fill=fg, width=5)
    d.line([cx - r * 0.5, cy - r * 0.62, cx + r * 0.52, cy - r * 0.62], fill=fg, width=4)
    # lightning bolt beside the mast
    bx, by = cx + r * 0.52, cy - r * 0.95
    d.polygon([(bx, by), (bx + r * 0.34, by), (bx + r * 0.12, by + r * 0.42),
               (bx + r * 0.34, by + r * 0.42), (bx - r * 0.08, by + r * 0.95),
               (bx + r * 0.02, by + r * 0.55), (bx - r * 0.16, by + r * 0.55)],
              fill=GOLD)
    # rails running away at the base
    d.line([cx - r * 0.95, cy + r * 0.88, cx + r * 0.95, cy + r * 0.88], fill=fg, width=5)
    for t in (-0.66, -0.33, 0.0, 0.33, 0.66):
        d.line([cx + r * t, cy + r * 0.74, cx + r * t, cy + r * 0.98], fill=fg, width=4)


def pic_drone_un(d, cx, cy, r, fg):
    """A quadcopter drone over rooftops, one flying a UN-blue flag."""
    dy = cy - r * 0.52
    d.ellipse([cx - 9, dy - 9, cx + 9, dy + 9], fill=fg)
    for sx in (-1, 1):
        for sy in (-1, 1):
            px, py = cx + sx * r * 0.42, dy + sy * r * 0.26
            d.line([cx, dy, px, py], fill=fg, width=4)
            d.ellipse([px - 11, py - 4, px + 11, py + 4], outline=fg, width=3)
    # rooftops along the bottom
    base = cy + r * 0.9
    d.polygon([(cx - r * 0.95, base), (cx - r * 0.95, cy + r * 0.42),
               (cx - r * 0.55, cy + r * 0.14), (cx - r * 0.15, cy + r * 0.42),
               (cx - r * 0.15, base)], fill=fg)
    d.polygon([(cx + r * 0.02, base), (cx + r * 0.02, cy + r * 0.5),
               (cx + r * 0.38, cy + r * 0.24), (cx + r * 0.74, cy + r * 0.5),
               (cx + r * 0.74, base)], fill=fg)
    # the UN building: taller block with a flag
    d.rectangle([cx + r * 0.78, cy + r * 0.05, cx + r * 0.98, base], fill=fg)
    d.line([cx + r * 0.88, cy + r * 0.05, cx + r * 0.88, cy - r * 0.22], fill=fg, width=3)
    d.polygon([(cx + r * 0.88, cy - r * 0.22), (cx + r * 1.06, cy - r * 0.15),
               (cx + r * 0.88, cy - r * 0.08)], fill=(116, 172, 223))
    # one rooftop ablaze, flame sitting on the left house's apex
    fx, fy = cx - r * 0.55, cy + r * 0.16
    d.polygon([(fx - 8, fy + 8), (fx, fy - 15), (fx + 9, fy + 8),
               (fx + 3, fy + 13), (fx - 3, fy + 13)], fill=FLAME)


def pic_capitol(d, cx, cy, r, fg):
    """A columned government hall with a circular 'reshuffle' arrow."""
    roof_y = cy - r * 0.52
    d.polygon([(cx - r * 0.85, roof_y), (cx, cy - r * 0.88), (cx + r * 0.85, roof_y)], fill=fg)
    d.rectangle([cx - r * 0.85, roof_y, cx + r * 0.85, roof_y + 9], fill=fg)
    for t in (-0.62, -0.21, 0.21, 0.62):
        d.rectangle([cx + r * t - 6, roof_y + 16, cx + r * t + 6, cy + r * 0.62], fill=fg)
    d.rectangle([cx - r * 0.88, cy + r * 0.62, cx + r * 0.88, cy + r * 0.74], fill=fg)
    d.rectangle([cx - r * 0.95, cy + r * 0.8, cx + r * 0.95, cy + r * 0.9], fill=fg)
    # circular arrow above the pediment: posts changing hands
    ax, ay, ar = cx + r * 0.52, cy - r * 0.78, r * 0.3
    d.arc([ax - ar, ay - ar, ax + ar, ay + ar], 300, 210, fill=GOLD, width=5)
    d.polygon([(ax + ar * 0.95, ay - ar * 0.45), (ax + ar * 0.35, ay - ar * 0.5),
               (ax + ar * 0.72, ay + ar * 0.08)], fill=GOLD)


def pic_charter(d, cx, cy, r, fg):
    """A charter scroll beside Mount Ararat, sealed in red wax."""
    x0, x1 = cx - r * 0.92, cx + r * 0.14
    y0, y1 = cy - r * 0.78, cy + r * 0.8
    d.rounded_rectangle([x0, y0, x1, y1], 7, fill=fg)
    for i in range(4):
        ly = y0 + 13 + i * 12
        d.line([x0 + 9, ly, x1 - 9 - (i % 2) * 10, ly],
               fill=(120, 116, 108), width=4)
    # the seal that makes it official
    sx, sy = x1 - 11, y1 - 11
    d.ellipse([sx - 7, sy - 7, sx + 7, sy + 7], fill=(196, 52, 40))
    d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)
    # Mount Ararat standing clear of the page's right edge
    d.polygon([(cx + r * 0.1, cy + r * 0.8), (cx + r * 0.58, cy - r * 0.3),
               (cx + r * 0.97, cy + r * 0.8)], fill=fg)
    d.polygon([(cx + r * 0.47, cy - r * 0.12), (cx + r * 0.58, cy - r * 0.3),
               (cx + r * 0.69, cy - r * 0.12)], fill=GOLD)


def pic_scales(d, cx, cy, r, fg):
    """Scales of justice weighing a chat bubble: the Grok lawsuits."""
    top = cy - r * 0.72
    d.line([cx - r * 0.72, top, cx + r * 0.72, top], fill=fg, width=6)
    d.line([cx, top, cx, cy + r * 0.66], fill=fg, width=6)
    d.rectangle([cx - r * 0.3, cy + r * 0.66, cx + r * 0.3, cy + r * 0.8], fill=fg)
    for sx in (-1, 1):
        px = cx + sx * r * 0.72
        d.line([px, top, px - 16, cy + r * 0.18], fill=fg, width=3)
        d.line([px, top, px + 16, cy + r * 0.18], fill=fg, width=3)
        d.arc([px - 30, cy + r * 0.02, px + 30, cy + r * 0.42], 0, 180, fill=fg, width=5)
    # chat bubble resting on the left pan
    bx, by = cx - r * 0.72, cy - r * 0.28
    d.rounded_rectangle([bx - 24, by - 17, bx + 24, by + 13], 8, fill=GOLD)
    d.polygon([(bx - 8, by + 13), (bx + 4, by + 13), (bx - 6, by + 24)], fill=GOLD)
    d.line([bx - 14, by - 4, bx + 14, by - 4], fill=(24, 24, 28), width=4)
    d.line([bx - 14, by + 5, bx + 6, by + 5], fill=(24, 24, 28), width=4)


def pic_ai_globe(d, cx, cy, r, fg):
    """A globe ringed by connected nodes: a shared AI framework."""
    d.ellipse([cx - r * 0.58, cy - r * 0.58, cx + r * 0.58, cy + r * 0.58],
              outline=fg, width=5)
    d.ellipse([cx - r * 0.26, cy - r * 0.58, cx + r * 0.26, cy + r * 0.58],
              outline=fg, width=3)
    d.line([cx - r * 0.58, cy, cx + r * 0.58, cy], fill=fg, width=3)
    nodes = [(-0.92, -0.55), (0.9, -0.62), (0.98, 0.42), (-0.35, 0.95), (-0.97, 0.3)]
    for nx, ny in nodes:
        px, py = cx + r * nx, cy + r * ny
        gx, gy = cx + r * nx * 0.58, cy + r * ny * 0.58
        d.line([gx, gy, px, py], fill=fg, width=3)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=GOLD)


# ------------------------------------------------------------------
# Page content
# ------------------------------------------------------------------

PANELS = [
    ("UKRAINE · WAR", (36, 78, 150), pic_rail_power,
     "RUSSIA POUNDS RAIL & POWER IN 153-DRONE BARRAGE",
     "Stations, depots and substations hit in 12 regions: 6 killed, "
     "32 hurt. Zelenskyy warns more strikes are coming."),
    ("KHARTOUM, SUDAN · WAR", (128, 44, 36), pic_drone_un,
     "UN & US CONDEMN DRONE HITS ON HOMES, UN OFFICE",
     "Strikes blamed on the RSF kill at least 4, incl. a child. Army "
     "alleges launches from Ethiopia — not verified."),
    ("SEOUL, SOUTH KOREA · POLITICS", (16, 108, 118), pic_capitol,
     "LEE NAMES FIRST WOMAN TO HEAD SPY AGENCY",
     "Ex-justice minister Kang Kum-sil tapped to lead the NIS; new "
     "foreign and unification ministers named too."),
    ("YEREVAN, ARMENIA · DIPLOMACY", (112, 74, 150), pic_charter,
     "ARMENIA DROPS KARABAKH CLAIM IN NEW DRAFT CHARTER",
     "Pashinyan's draft removes Baku's key objection to a peace "
     "treaty; he vows to quit if voters reject it."),
    ("VIRGINIA & OREGON, US · TECH LAW", (52, 96, 62), pic_scales,
     "STATES SUE MUSK'S SPACEX OVER GROK IMAGES",
     "First state suits say Grok's 'spicy mode' made sexualised "
     "images, incl. of children, with too few safeguards."),
    ("BRIDGETOWN, BARBADOS · AI RULES", (30, 110, 76), pic_ai_globe,
     "UN CHIEF: AGREE A GLOBAL AI SAFETY FRAMEWORK",
     "Guterres tells the Bridgetown summit AI shifts power from "
     "states to a few firms — rules needed within a year."),
]

TICKER = (
    "ALSO ON 23 NOV — Zelenskyy confirms 7 sea drones sank Russia's "
    "corvette Merkury at Benghazi; UN seeks a probe • Trump: inclined "
    "to resume Iran strikes after New Year if no deal • Toliver "
    "postpones London show after 'unknown substance' empties "
    "Manchester arena • WHO: Ituri fighting disrupts DR Congo's "
    "Ebola response"
)


# ------------------------------------------------------------------
# Rendering
# ------------------------------------------------------------------

def draw_card(d, x, y, w, h, panel):
    strip, colour, icon, headline, caption = panel
    d.rounded_rectangle([x, y, x + w, y + h], 12, fill=CARD_BG,
                        outline=CARD_LINE, width=2)
    # dateline strip across the top of the card
    d.rounded_rectangle([x, y, x + w, y + 38], 12, fill=colour)
    d.rectangle([x, y + 24, x + w, y + 38], fill=colour)
    d.text((x + 14, y + 8), strip, font=load(20, F_BOLD), fill=(255, 255, 255))
    # round badge with the pictogram, centred in the body
    bcx, bcy, brad = x + 70, y + 38 + (h - 38) // 2 + 4, 50
    d.ellipse([bcx - brad, bcy - brad, bcx + brad, bcy + brad], fill=colour)
    icon(d, bcx, bcy, 37, (255, 255, 255))
    # headline, then caption; the fit is asserted so a long line can
    # never silently spill off the card
    tx = x + 138
    tw = x + w - tx - 14
    end_y = stack(d, tx, y + 46, headline, load(25, F_BLACK), INK, tw, 30)
    end_y = stack(d, tx, end_y + 4, caption, load(17), GREY, tw, 22)
    assert end_y <= y + h - 3, f"card copy overflows: {headline}"


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead: dark band, serif title, red date.
    d.rectangle([0, 0, SIZE, 178], fill=MASTHEAD)
    d.text((30, 20), "ONE DAY · ONE PICTURE · THE WORLD'S NEWS",
           font=load(22, F_BOLD), fill=GOLD)
    d.text((28, 48), "THE WORLD ON MONDAY", font=load(62, F_SERIF),
           fill=(255, 255, 255))
    d.text((30, 126), "23 NOVEMBER 2026", font=load(40, F_BLACK), fill=(255, 120, 96))
    d.text((596, 138), "Six stories that sum up the day",
           font=load(22), fill=CREAM)
    d.line([30, 190, 994, 190], fill=INK, width=3)

    # Six cards, two columns by three rows.
    grid_top, grid_bottom = 202, 898
    col_gap, row_gap = 16, 13
    card_w = (SIZE - 60 - col_gap) // 2
    card_h = (grid_bottom - grid_top - 2 * row_gap) // 3
    for i, panel in enumerate(PANELS):
        px = 30 + (i % 2) * (card_w + col_gap)
        py = grid_top + (i // 2) * (card_h + row_gap)
        draw_card(d, px, py, card_w, card_h, panel)

    # Ticker band at the foot of the page.
    d.rectangle([0, 912, SIZE, SIZE], fill=MASTHEAD)
    stack(d, 30, 924, TICKER, load(19, F_BOLD), CREAM, 964, 25)

    out = Path(__file__).resolve().parent.parent / "entry.png"
    img.save(out, optimize=True)
    nbytes = out.stat().st_size
    print(f"entry.png written: {img.width}x{img.height}, {nbytes} bytes")
    assert img.width <= 1024 and img.height <= 1024
    assert nbytes <= 1_048_576, "entry.png exceeds the 1 MiB limit"


if __name__ == "__main__":
    build()
