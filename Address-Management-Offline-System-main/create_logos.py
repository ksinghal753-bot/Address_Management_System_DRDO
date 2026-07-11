"""
Script to generate placeholder logo images for ADRDE and DRDO.
Run this once if you don't have actual logo files.
"""

import os
import sys

def create_placeholder_logos():
    """Create simple placeholder logo images using Pillow."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow not installed. Run: pip install Pillow")
        sys.exit(1)

    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    os.makedirs(assets_dir, exist_ok=True)

    logos = [
        {
            "filename": "drdo_logo_clean.png",
            "text": "ADRDE",
            "sub": "DRDO",
            "bg": (16, 42, 86),       # Navy
            "fg": (200, 164, 0),       # Gold
        },
        {
            "filename": "drdo_logo_clean.png",
            "text": "DRDO",
            "sub": "भारत",
            "bg": (10, 22, 40),
            "fg": (200, 164, 0),
        },
    ]

    for logo in logos:
        size = (128, 128)
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Draw circle background
        margin = 4
        draw.ellipse(
            [margin, margin, size[0]-margin, size[1]-margin],
            fill=logo["bg"],
            outline=logo["fg"],
            width=4
        )

        # Draw text
        try:
            font_main = ImageFont.truetype("arial.ttf", 22)
            font_sub  = ImageFont.truetype("arial.ttf", 12)
        except Exception:
            font_main = ImageFont.load_default()
            font_sub  = font_main

        # Main text
        bbox = draw.textbbox((0,0), logo["text"], font=font_main)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        draw.text(
            ((size[0]-tw)//2, (size[1]-th)//2 - 10),
            logo["text"], fill=logo["fg"], font=font_main
        )
        # Sub text
        bbox2 = draw.textbbox((0,0), logo["sub"], font=font_sub)
        tw2, th2 = bbox2[2]-bbox2[0], bbox2[3]-bbox2[1]
        draw.text(
            ((size[0]-tw2)//2, (size[1]-th2)//2 + 18),
            logo["sub"], fill=(180, 200, 240), font=font_sub
        )

        out_path = os.path.join(assets_dir, logo["filename"])
        img.save(out_path)
        print(f"Created: {out_path}")

    print("\nPlaceholder logos created. Replace with actual ADRDE/DRDO logos when available.")


if __name__ == "__main__":
    create_placeholder_logos()
