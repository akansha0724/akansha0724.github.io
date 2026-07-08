"""
build_thumbnail.py — Regenerate the 1200x630 social-preview card (og:image).

No SVG rasterizer is needed — this reproduces thumbnail.svg's design directly
with matplotlib so the PNG can be rebuilt whenever the headline stats change.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

OUT = Path(__file__).parent / "thumbnail.png"
W, H = 1200, 630

# palette (matches the site)
CREAM_TL = (255, 248, 251)
CREAM_BR = (254, 240, 245)
ACCENT = "#d6336c"
INK = "#2b1a22"
DEEP = "#a61e4d"
PILL_BG = "#ffe1ec"

# headline stats — edit these when the portfolio grows
STATS = ["10 projects", "900K+ records", "3 domains"]


def svgy(y):  # SVG top-down y -> matplotlib bottom-up y
    return H - y


fig = plt.figure(figsize=(12, 6.3), dpi=100)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# diagonal cream gradient
grad = np.zeros((H, W, 3))
tl = np.array(CREAM_TL) / 255
br = np.array(CREAM_BR) / 255
for i in range(3):
    ramp = np.linspace(0, 1, W)[None, :] * 0.5 + np.linspace(1, 0, H)[:, None] * 0.5
    grad[:, :, i] = tl[i] * (1 - ramp) + br[i] * ramp
ax.imshow(grad, extent=[0, W, 0, H], aspect="auto", zorder=0)

# left accent bar
ax.add_patch(Rectangle((0, 0), 10, H, color=ACCENT, zorder=1))

# decorative blobs
ax.add_patch(Circle((1050, svgy(90)), 200, color="#ffc7de", alpha=0.22, zorder=1))
ax.add_patch(Circle((140, svgy(560)), 150, color="#ffe0b8", alpha=0.18, zorder=1))

# kicker
ax.text(100, svgy(148), "FINANCE · HEALTHCARE · CONSULTING ANALYTICS",
        family="monospace", fontsize=15, fontweight="bold", color=ACCENT, zorder=2)

# name
ax.text(100, svgy(245), "Akansha Singh", family="serif", fontsize=58,
        fontweight="bold", color=INK, zorder=2)

# role
ax.text(100, svgy(312), "Data Analytics", family="serif", fontsize=32,
        fontstyle="italic", color=ACCENT, zorder=2)

# divider
ax.add_patch(Rectangle((100, svgy(349)), 90, 4, color=ACCENT, zorder=2))

# stat pills
x = 100
for label in STATS:
    w = 34 + len(label) * 12.5
    ax.add_patch(FancyBboxPatch((x, svgy(429)), w, 44,
                                boxstyle="round,pad=0,rounding_size=10",
                                facecolor=PILL_BG, edgecolor="none", zorder=2))
    ax.text(x + w / 2, svgy(407), label, family="monospace", fontsize=15,
            fontweight="bold", color=DEEP, ha="center", va="center", zorder=3)
    x += w + 14

# url
ax.text(100, svgy(520), "akansha0724.github.io", family="monospace",
        fontsize=16, fontweight="bold", color=ACCENT, zorder=2)

fig.savefig(OUT, dpi=100)
plt.close(fig)
print(f"wrote {OUT.name} ({OUT.stat().st_size // 1024} KB)")
