"""Image generation utilities for the e-ink display."""

from PIL import Image, ImageDraw, ImageFont
import os
from typing import Dict, Any, Tuple

# Font paths
FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'fonts')
REGULAR_FONT = os.path.join(FONT_DIR, 'Roboto-Regular.ttf')
BOLD_FONT = os.path.join(FONT_DIR, 'Roboto-Bold.ttf')

def draw_shadowed_text(draw: ImageDraw.ImageDraw,
                      position: Tuple[int, int],
                      text: str,
                      font: ImageFont.FreeTypeFont,
                      text_color: str = 'black',
                      shadow_color: str = 'white') -> None:
    """Draw text with a shadow effect."""
    x, y = position
    # Draw shadow
    draw.text((x+1, y+1), text, font=font, fill=shadow_color)
    # Draw main text
    draw.text((x, y), text, font=font, fill=text_color)

def draw_key_value(draw: ImageDraw.ImageDraw,
                   position: Tuple[int, int],
                   key: str,
                   value: str,
                   font_regular: ImageFont.FreeTypeFont,
                   font_bold: ImageFont.FreeTypeFont) -> None:
    """Draw a key-value pair with different fonts."""
    x, y = position
    # Draw key
    draw.text((x, y), f"{key}: ", font=font_regular, fill='black')
    # Get width of key text
    key_width = draw.textlength(f"{key}: ", font=font_regular)
    # Draw value
    draw.text((x + key_width, y), value, font=font_bold, fill='black')

def generate_image(aircraft_data: Dict[str, Any]) -> Image.Image:
    """Generate an image with flight information."""
    # Create a new image with white background
    image = Image.new('RGB', (400, 300), 'white')
    draw = ImageDraw.Draw(image)
    
    # Load fonts
    title_font = ImageFont.truetype(BOLD_FONT, 36)
    regular_font = ImageFont.truetype(REGULAR_FONT, 24)
    bold_font = ImageFont.truetype(BOLD_FONT, 24)
    
    # Draw flight number
    draw_shadowed_text(draw, (10, 10), 
                      f"Flight {aircraft_data['flight_number']}", 
                      title_font)
    
    # Draw route
    if aircraft_data.get('legs'):
        origin = aircraft_data['legs'][0]['code']
        destination = aircraft_data['legs'][-1]['code']
        draw_key_value(draw, (10, 60), "Route", 
                      f"{origin} → {destination}", 
                      regular_font, bold_font)
    
    # Draw other details
    y_position = 100
    details = [
        ('Altitude', f"{aircraft_data['altitude']} ft"),
        ('Speed', f"{aircraft_data['speed']} kts"),
        ('Distance', f"{aircraft_data['distance']:.1f} nm")
    ]
    
    for key, value in details:
        draw_key_value(draw, (10, y_position), 
                      key, value, 
                      regular_font, bold_font)
        y_position += 40
    
    return image

def generate_blank_image() -> Image.Image:
    """Generate a blank white image."""
    return Image.new('RGB', (400, 300), 'white') 