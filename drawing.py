# from PIL import Image, ImageDraw, ImageFont

# Offset for shadowed text.  It's this amount lower than its y position
shadowed_color_y_offset = 55

def draw_shadowed_text(draw, y, text, font, width, fill=(0, 0, 0), stroke_width=3, stroke_fill=(0, 0, 0), shadow_x=-1, shadow_y=1, steps=10):
    """Draw text centered horizontally at specified y position."""
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    x = (width - w) / 2

    for i in range(steps):
        draw.text((x + i * shadow_x, y + i * shadow_y - shadowed_color_y_offset), text, font=font, fill=stroke_fill, stroke_width=stroke_width, stroke_fill=stroke_fill)

    draw.text((x, y - shadowed_color_y_offset), text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)

def draw_centered_text(draw, y, text, font, width, fill=(0, 0, 0), max_width=None):
    """
    Draw text centered horizontally at specified y position with optional text wrapping.
    Returns the total height of the text box.
    """
    if not max_width:
        # Original single-line behavior
        _, _, w, h = draw.textbbox((0, 0), text, font=font)
        x = (width - w) / 2
        draw.text((x, y), text, font=font, fill=fill)
        return h

    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        test_line = ' '.join(current_line)
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]
        
        if line_width > max_width:
            # Remove the last word and add the line
            current_line.pop()
            if current_line:  # Only add if there are words
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:  # Add the last line
        lines.append(' '.join(current_line))
    
    # Get line height from a sample text
    _, _, _, line_height = draw.textbbox((0, 0), 'Ay', font=font)
    
    current_y = y
    for line in lines:
        _, _, w, h = draw.textbbox((0, 0), line, font=font)
        x = (width - w) / 2
        draw.text((x, current_y), line, font=font, fill=fill)
        current_y += line_height
    
    total_height = line_height * len(lines)
    return total_height

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