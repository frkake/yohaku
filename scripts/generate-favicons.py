#!/usr/bin/env python3
"""Generate favicon files from the yohaku symbol mark."""

from pathlib import Path

from PIL import Image, ImageDraw

BRAND_BLUE = (74, 158, 204)  # #4A9ECC
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "static"

# PNG favicon sizes
SIZES = {
    "favicon-16x16.png": 16,
    "favicon-32x32.png": 32,
    "apple-touch-icon.png": 180,
    "android-chrome-192x192.png": 192,
    "android-chrome-512x512.png": 512,
}

# ICO contains multiple sizes
ICO_SIZES = [16, 32, 48]


def draw_mark(size: int) -> Image.Image:
    """Draw the symbol mark (dot + line) at the given pixel size.

    Coordinates are proportional to the logo-mark.svg viewBox (0 0 100 100):
      circle  cx=22  cy=28  r=10
      rect    x=4  y=64  w=72  h=6  rx=3
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    s = size

    # Dot (filled circle)
    cx, cy, r = 0.22 * s, 0.28 * s, 0.10 * s
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BRAND_BLUE)

    # Line (rounded rectangle)
    x0, y0 = 0.04 * s, 0.64 * s
    x1, y1 = 0.76 * s, 0.70 * s
    corner = max(1, int(0.03 * s))
    draw.rounded_rectangle([x0, y0, x1, y1], radius=corner, fill=BRAND_BLUE)

    return img


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating favicons …")

    # PNG favicons
    for filename, size in SIZES.items():
        img = draw_mark(size)
        img.save(OUTPUT_DIR / filename, "PNG")
        print(f"  {filename} ({size}x{size})")

    # Multi-size .ico
    ico_images = [draw_mark(s) for s in ICO_SIZES]
    ico_images[0].save(
        OUTPUT_DIR / "favicon.ico",
        format="ICO",
        sizes=[(s, s) for s in ICO_SIZES],
        append_images=ico_images[1:],
    )
    print(f"  favicon.ico ({'/'.join(str(s) for s in ICO_SIZES)}px)")

    print("Done!")


if __name__ == "__main__":
    main()
