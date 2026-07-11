import os
from PIL import Image, ImageDraw

def create_checkbox_images():
    assets_dir = os.path.join(os.path.dirname(__file__), 'assets')
    os.makedirs(assets_dir, exist_ok=True)
    
    # 1. Unchecked Light
    img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([1, 1, 18, 18], radius=3, fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    img.save(os.path.join(assets_dir, "checkbox_unchecked_light.png"))
    
    # 2. Checked Light
    img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([1, 1, 18, 18], radius=3, fill=(255, 255, 255), outline=(0, 0, 0), width=2)
    # Draw black checkmark
    draw.line([(5, 10), (9, 14)], fill=(0, 0, 0), width=3)
    draw.line([(9, 14), (15, 6)], fill=(0, 0, 0), width=3)
    img.save(os.path.join(assets_dir, "checkbox_checked_light.png"))
    
    # 3. Unchecked Dark
    img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([1, 1, 18, 18], radius=3, fill=(30, 41, 59), outline=(248, 250, 252), width=2)
    img.save(os.path.join(assets_dir, "checkbox_unchecked_dark.png"))
    
    # 4. Checked Dark
    img = Image.new("RGBA", (20, 20), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle([1, 1, 18, 18], radius=3, fill=(30, 41, 59), outline=(248, 250, 252), width=2)
    # Draw white checkmark
    draw.line([(5, 10), (9, 14)], fill=(248, 250, 252), width=3)
    draw.line([(9, 14), (15, 6)], fill=(248, 250, 252), width=3)
    img.save(os.path.join(assets_dir, "checkbox_checked_dark.png"))

if __name__ == "__main__":
    create_checkbox_images()
    print("Checkbox images created successfully.")
