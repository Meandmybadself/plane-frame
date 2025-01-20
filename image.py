# These are functions for laying out the image

from PIL import Image, ImageDraw, ImageFont
import logging
from drawing import draw_shadowed_text, draw_centered_text, draw_key_value
from flight import calculate_flight_progress

red = (255, 0, 0)
grey = (200, 200, 200)
# Load fonts
bold = ImageFont.truetype('./fonts/bold.ttf', 25)
xtrabold = ImageFont.truetype('./fonts/xtrabold.ttf', 195)

def generate_blank_image():
    # Create initial RGB image in portrait orientation
    image_width = 480
    image_height = 800
    image = Image.new('RGB', (image_width, image_height), (255, 245, 220))
    draw = ImageDraw.Draw(image)

    # Draw the text
    starting_y = 300
    xtrabold_130 = ImageFont.truetype('./fonts/xtrabold.ttf', 130)
    draw_shadowed_text(draw, starting_y, "CLEAR", xtrabold_130, 480, (222, 222, 222))
    draw_shadowed_text(draw, 150 + starting_y, "SKIES", xtrabold_130, 480, (222, 222, 222))
    
    return image

def generate_image(aircraft_data):
    # Create initial RGB image in portrait orientation
    image_width = 480
    image_height = 800
    image = Image.new('RGB', (image_width, image_height), (255, 245, 220))
    draw = ImageDraw.Draw(image)
    
    airplane_img = Image.open('./images/plane.25.jpg').convert('RGBA')

    logging.info(f'Aircraft data: {aircraft_data}') 

    # Calculate flight progress
    starting_y = 115
    padding = 20
    line_width = 2
    line_distance = image_width - padding * 2
    
    # Draw flight information
    airline_plus_flight_number = f'{aircraft_data.get("airline", "N/A")} {aircraft_data.get("flight_number", "N/A")}'.upper()
    draw_centered_text(draw, starting_y, airline_plus_flight_number, bold, 480, red, max_width=440)

    top_line_y = starting_y + 40
    draw.line((padding, top_line_y, line_distance, top_line_y), fill=grey, width=line_width)

    # Extract airport information from legs
    legs = aircraft_data.get('legs', [])
    if len(legs) >= 2:
        origin = legs[0]
        destination = legs[-1]  # Gets last airport in case of multi-leg journey
        
        # ORIGIN
        origin_code = origin['code']
        # if origin_code starts with 'K'
        if origin_code.startswith('K'):
            origin_code = origin_code[1:]
        origin_code_y = starting_y + 60
        draw_shadowed_text(draw, origin_code_y, origin_code, xtrabold, 480, (222, 222, 222))
        
        origin_name = origin['name'].upper()
        origin_name_y = origin_code_y + 165
        origin_name_height = draw_centered_text(draw, origin_name_y, origin_name, bold, 480, red, max_width=440)

        # DESTINATION
        destination_code = destination['code']
        destination_code_y = origin_name_y + origin_name_height + 40
        draw_shadowed_text(draw, destination_code_y, destination_code, xtrabold, 480, (222, 222, 222))

        destination_name = destination['name'].upper()
        destination_name_y = destination_code_y + 165
        destination_name_height = draw_centered_text(draw, destination_name_y, destination_name, bold, 480, red, max_width=440)
    
    # Draw progress line
    # flight_progress is a number between 0 and 1
    flight_progress = calculate_flight_progress(aircraft_data)
    drawn_line_distance = padding + (line_distance * flight_progress)
    
    line_y = destination_name_y + destination_name_height + 15
    draw.line((padding, line_y, line_distance, line_y), fill=grey, width=line_width)
    draw.line((padding, line_y, drawn_line_distance, line_y), fill=red, width=line_width)
    
    # Draw airplane image
    plane_img_size = 25
    plane_x = int(padding + drawn_line_distance - plane_img_size / 2)
    plane_y = int(line_y - plane_img_size / 2) + 1
    logging.info(f'Plane x: {plane_x}, Plane y: {plane_y}')
    image.paste(airplane_img, (plane_x, plane_y))

    # Draw flight details
    positions = [(padding, starting_y + 535), (padding, starting_y + 575), (padding, starting_y + 615)]
    
    # if aircraft_data.get('altitude'):
    #     altitude = f"{int(aircraft_data.get('altitude')):,}"
    #     pos = positions.pop(0)
    #     draw_key_value(draw, pos[0], pos[1], "ALTITUDE:", f'{altitude}FT', bold, bold, black)
    
    # if aircraft_data.get('speed'):
    #     speed = f"{int(aircraft_data.get('speed')):,}"
    #     pos = positions.pop(0)
    #     draw_key_value(draw, pos[0], pos[1], "SPEED:", f'{speed}KTS', bold, bold, black)
    
    return image