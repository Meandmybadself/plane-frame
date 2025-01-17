# from PIL import Image, ImageDraw, ImageFont

def draw_shadowed_text(draw, y, text, font, width, fill=(0, 0, 0), stroke_width=3, stroke_fill=(0, 0, 0), shadow_x=-1, shadow_y=1, steps=10):
    """Draw text centered horizontally at specified y position."""
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    x = (width - w) / 2

    for i in range(steps):
        draw.text((x + i * shadow_x, y + i * shadow_y), text, font=font, fill=stroke_fill, stroke_width=stroke_width, stroke_fill=stroke_fill)

    draw.text((x, y), text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)

def draw_centered_text(draw, y, text, font, width, fill=(0, 0, 0)):
    """Draw text centered horizontally at specified y position."""
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    x = (width - w) / 2

    # for i in range(steps):
    #     draw.text((x + i * shadow_x, y + i * shadow_y), text, font=font, fill=shadow_fill)

    draw.text((x, y), text, font=font, fill=fill)

def draw_key_value(draw, x, y, key, value, key_font, value_font, fill=(0, 0, 0)):
    """Draw a key-value pair with left alignment at specified position."""
    # Draw the key
    draw.text((x, y), key, font=key_font, fill=fill)
    
    # Get the width of the key text plus some padding
    key_bbox = draw.textbbox((x, y), key, font=key_font)
    key_width = key_bbox[2] - key_bbox[0]
    
    # Draw the value with some padding after the key`
    value_x = x + key_width + 10  # 10 pixels padding
    draw.text((value_x, y), value, font=value_font, fill=fill) 