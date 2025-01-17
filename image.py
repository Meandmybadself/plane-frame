from PIL import Image, ImageDraw, ImageFont
import logging
from drawing import draw_shadowed_text, draw_centered_text, draw_key_value
from flight import calculate_flight_progress

def generate_image(aircraft_data):
    # Create initial RGB image in portrait orientation
    image_width = 480
    image_height = 800
    image = Image.new('RGB', (image_width, image_height), (255, 245, 220))
    draw = ImageDraw.Draw(image)
    black = (0, 0, 0)
    red = (255, 0, 0)

    # Load fonts
    bold = ImageFont.truetype('./fonts/bold.ttf', 20)
    # demi = ImageFont.truetype('./fonts/demi.ttf', 20)
    # heavy = ImageFont.truetype('./fonts/heavy.ttf', 20)
    # light = ImageFont.truetype('./fonts/light.ttf', 20)
    # medium = ImageFont.truetype('./fonts/medium.ttf', 25)
    xtrabold = ImageFont.truetype('./fonts/xtrabold.ttf', 195)

    airplane_img = Image.open('./plane.25.png').convert('RGBA')

    logging.info(f'Aircraft data: {aircraft_data}') 

    # Calculate flight progress
    starting_y = 125
    padding = 20

    line_distance = image_width - padding * 2
    flight_progress = calculate_flight_progress(aircraft_data)
    drawn_line_distance = padding + (line_distance * flight_progress)

    top_line_y = starting_y
    draw.line((padding, top_line_y, line_distance, top_line_y), fill=(215, 215, 215), width=2)

    # Draw flight information
    airline_plus_flight_number = f'{aircraft_data.get("airline", "N/A")} {aircraft_data.get("flight", "N/A")}'.upper()
    draw_centered_text(draw, starting_y + 17, airline_plus_flight_number, bold, 480, red)

    from_airport_code = aircraft_data.get('from', 'N/A')
    draw_shadowed_text(draw, starting_y + 15, from_airport_code, xtrabold, 480, (222, 222, 222))

    origin_name = aircraft_data.get('origin', 'N/A').upper()
    draw_centered_text(draw, starting_y + 230, origin_name, bold, 480, red)

    to_airport_code = aircraft_data.get('to', 'N/A')
    draw_shadowed_text(draw, starting_y + 230, to_airport_code, xtrabold, 480, (222, 222, 222))

    destination_name = aircraft_data.get('destination', 'N/A').upper()
    draw_centered_text(draw, starting_y + 450, destination_name, bold, 480, red)

    # Draw progress line
    line_y = starting_y + 500
    draw.line((padding, line_y, line_distance, line_y), fill=(215, 215, 215), width=2)
    draw.line((padding, line_y, drawn_line_distance, line_y), fill=red, width=2)
    
    # Draw airplane image
    plane_img_size = 25
    plane_x = int(padding + drawn_line_distance - plane_img_size / 2)
    plane_y = int(line_y - plane_img_size / 2)
    logging.info(f'Plane x: {plane_x}, Plane y: {plane_y}')
    image.paste(airplane_img, (plane_x, plane_y))

    # Draw flight details
    positions = [(padding, starting_y + 535), (padding, starting_y + 575), (padding, starting_y + 615)]
    
    if aircraft_data.get('altitude'):
        altitude = f"{int(aircraft_data.get('altitude')):,}"
        pos = positions.pop(0)
        draw_key_value(draw, pos[0], pos[1], "ALTITUDE:", f'{altitude}FT', bold, bold, black)
    
    if aircraft_data.get('speed'):
        speed = f"{int(aircraft_data.get('speed')):,}"
        pos = positions.pop(0)
        draw_key_value(draw, pos[0], pos[1], "SPEED:", f'{speed}KTS', bold, bold, black)
    
    return image