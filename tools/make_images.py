"""Generate the launcher icon (96x96) and TV banner (320x180): a white gear on a dark blue tile.

Usage: python3 tools/make_images.py res/drawable-xhdpi [docs]
The optional second directory gets a 3x banner for the README.
"""
import math, sys
from PIL import Image, ImageDraw, ImageFont

SS = 4  # supersampling for smooth edges
BG = (20, 37, 61)
FG = (255, 255, 255)
ACCENT = (255, 153, 0)

def gear(draw, cx, cy, r, teeth=8):
    ro, ri = r, r * 0.78
    pts = []
    steps = teeth * 4
    for k in range(steps):
        a0 = 2 * math.pi * k / steps
        rad = ro if k % 4 in (1, 2) else ri
        for t in (0.0, 1.0):
            a = a0 + t * 2 * math.pi / steps
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    draw.polygon(pts, fill=FG)
    hole = r * 0.36
    draw.ellipse([cx - hole, cy - hole, cx + hole, cy + hole], fill=BG)

def render(w, h, fn):
    img = Image.new("RGB", (w * SS, h * SS), BG)
    fn(ImageDraw.Draw(img), w * SS, h * SS)
    return img.resize((w, h), Image.LANCZOS)

def icon(d, W, H):
    gear(d, W / 2, H / 2, W * 0.38)

def banner(d, W, H):
    d.rectangle([0, H - H * 0.05, W, H], fill=ACCENT)
    gear(d, W * 0.22, H * 0.475, H * 0.30)
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(H * 0.17))
    x = W * 0.42
    d.text((x, H * 0.27), "Fire", font=font, fill=FG)
    d.text((x, H * 0.49), "Settings", font=font, fill=FG)

out = sys.argv[1]
render(96, 96, icon).save(f"{out}/icon.png", optimize=True)
render(320, 180, banner).save(f"{out}/banner.png", optimize=True)
if len(sys.argv) > 2:
    render(960, 540, banner).save(f"{sys.argv[2]}/banner.png", optimize=True)
