"""DataMole icon frame: navy tile, amber line, white panel, source logo centered (badge may overlap its corner), DataMole badge sticker bottom-right."""
import sys, os
from PIL import Image, ImageDraw

NAVY, AMBER, TEAL, WHITE = (15, 27, 45, 255), (245, 165, 36, 255), (20, 184, 166, 255), (255, 255, 255, 255)
S = 500

def is_brand_tile(logo):
    """True when the logo is a square with an opaque, non-white background in every corner."""
    w, h = logo.size
    if abs(w - h) > max(w, h) * 0.05:
        return False
    corners = [logo.getpixel(p) for p in ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))]
    return all(a == 255 and min(r, g, b) < 235 for r, g, b, a in corners)

def frame(logo_path, badge_path, out_path):
    canvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    d.rounded_rectangle((0, 0, S - 1, S - 1), radius=96, fill=NAVY)
    d.rounded_rectangle((14, 14, S - 15, S - 15), radius=84, outline=AMBER, width=6)
    d.rounded_rectangle((30, 30, S - 31, S - 31), radius=70, fill=WHITE)

    logo = Image.open(logo_path).convert("RGBA")
    if is_brand_tile(logo):
        # Square logo with its own colored background (e.g. Substack, WTTJ): fill the whole panel with it
        panel = S - 60
        logo = logo.resize((panel, panel), Image.LANCZOS)
        mask = Image.new("L", (panel, panel), 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, panel - 1, panel - 1), radius=70, fill=255)
        canvas.paste(logo, (30, 30), mask)
    else:
        bbox = logo.getbbox()
        if bbox:
            logo = logo.crop(bbox)
        logo.thumbnail((350, 350), Image.LANCZOS)
        canvas.alpha_composite(logo, ((S - logo.width) // 2, (S - logo.height) // 2))

    size = 112
    badge = Image.open(badge_path).convert("RGBA").resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    cx = cy = 398
    d.ellipse((cx - size // 2 - 7, cy - size // 2 - 7, cx + size // 2 + 7, cy + size // 2 + 7), fill=NAVY)
    canvas.paste(badge, (cx - size // 2, cy - size // 2), mask)
    canvas.save(out_path)

if __name__ == "__main__":
    src_dir, badge, out_dir = sys.argv[1:4]
    for f in sorted(os.listdir(src_dir)):
        if f.endswith(".png"):
            frame(os.path.join(src_dir, f), badge, os.path.join(out_dir, f))
            print(f)
