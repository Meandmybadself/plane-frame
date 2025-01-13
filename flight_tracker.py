import time
import requests
from inky.auto import auto
import logging
from PIL import Image, ImageDraw, ImageFont
import json
from dotenv import load_dotenv
import os

load_dotenv()

LATITUDE = float(os.getenv('LATITUDE'))
LONGITUDE = float(os.getenv('LONGITUDE'))
RADIUS = int(os.getenv('RADIUS'))

# Initialize logging
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

# Add display initialization at the global level
display = auto()

def get_route_by_callsign(flight_number):
    """
    Fetch aircraft route information by callsign.
    
    Args:
        flight_number (str): The flight callsign/number
        
    Returns:
        dict: Aircraft route data or None if request fails
    """
    try:
        flight_number = flight_number.strip()
        closest_aircraft_url = f'https://api.adsbdb.com/v0/callsign/{flight_number}'
        logging.info(f'Aircraft Details URL: {closest_aircraft_url}')
        closest_aircraft_response = requests.get(closest_aircraft_url)
        
        # Check for 404 or other error status codes
        if closest_aircraft_response.status_code != 200:
            logging.warning(f'API returned status code: {closest_aircraft_response.status_code}')
            return None
            
        closest_aircraft_data = closest_aircraft_response.json()
        
        # logging.info(f'Aircraft data: {closest_aircraft_data}')
        
        if 'response' in closest_aircraft_data and 'flightroute' in closest_aircraft_data['response']:
            flight_info = closest_aircraft_data['response']['flightroute']

            logging.info(f'Flight info: {flight_info}')
            
            return {
                'from': flight_info.get('origin', {}).get('iata_code'),
                'to': flight_info.get('destination', {}).get('iata_code'),
                'flight': flight_number,
                'airline': flight_info.get('airline', {}).get('name'),
                'origin': flight_info.get('origin', {}).get('municipality'),
                'origin_name': flight_info.get('origin', {}).get('name'),
                'destination': flight_info.get('destination', {}).get('municipality'), 
                'destination_name': flight_info.get('destination', {}).get('name'),
                'altitude': flight_info.get('altitude'),
                'speed': flight_info.get('speed'),
                'type': flight_info.get('type'),
                'route': flight_info.get('route')
            }
        return None
    except Exception as e:
        logging.error(f'Failed to fetch aircraft data: {e}')
        return None

def get_closest_aircraft_details():
    try:
        # Get closest aircraft data
        url = f'https://api.adsb.lol/v2/point/{LATITUDE}/{LONGITUDE}/{RADIUS}'
        logging.info(f'Closest aircraft URL: {url}')
        response = requests.get(url)
        closest_aircraft_search_data = response.json()

        # Filter out any any aircraft whose alt_baro is "ground"
        closest_aircraft_search_data['ac'] = [aircraft for aircraft in closest_aircraft_search_data['ac'] if aircraft['alt_baro'] != 'ground']
        
        # Loop over all aircraft and get the first one that returns a valid response from get_aircraft_by_callsign
        for aircraft in closest_aircraft_search_data['ac']:
            if 'flight' in aircraft:
                logging.info(f'Fetching route data for {aircraft["flight"]}')
                route_data = get_route_by_callsign(aircraft["flight"])
                if route_data:
                    closest_aircraft_data = route_data
                    closest_aircraft_data.update({
                        'altitude': aircraft.get('alt_baro', 'N/A'),
                        'speed': aircraft.get('gs', 'N/A'),
                        'type': aircraft.get('t', 'N/A')
                    })
                    break            
        return closest_aircraft_data
        
    except Exception as e:
        logging.error(f'API request failed: {e}')
        return None

def draw_centered_text(draw, y, text, font, width, fill=(0, 0, 0)):
    """Draw text centered horizontally at specified y position.
    
    Args:
        draw: ImageDraw object
        y: Vertical position
        text: Text to draw
        font: Font to use
        width: Width of the image
        fill: Text color (default black)
    """
    _, _, w, h = draw.textbbox((0, 0), text, font=font)
    x = (width - w) / 2
    draw.text((x, y), text, font=font, fill=fill)

def draw_key_value(draw, x, y, key, value, key_font, value_font, fill=(0, 0, 0)):
    """Draw a key-value pair with left alignment at specified position.
    
    Args:
        draw: ImageDraw object
        x: Horizontal starting position
        y: Vertical position
        key: Key text to draw
        value: Value text to draw
        key_font: Font to use for key
        value_font: Font to use for value
        fill: Text color (default black)
    """
    # Draw the key
    draw.text((x, y), key, font=key_font, fill=fill)
    
    # Get the width of the key text plus some padding
    key_bbox = draw.textbbox((x, y), key, font=key_font)
    key_width = key_bbox[2] - key_bbox[0]
    
    # Draw the value with some padding after the key
    value_x = x + key_width + 10  # 10 pixels padding
    draw.text((value_x, y), value, font=value_font, fill=fill)

def update_display(aircraft_data):
    try:
        # Create initial RGB image in portrait orientation
        image = Image.new('RGB', (480, 800), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        
        # Load fonts
        bold = ImageFont.truetype('./fonts/bold.ttf', 25)
        demi = ImageFont.truetype('./fonts/demi.ttf', 20)
        heavy = ImageFont.truetype('./fonts/heavy.ttf', 20)
        light = ImageFont.truetype('./fonts/light.ttf', 20)
        medium = ImageFont.truetype('./fonts/medium.ttf', 25)
        xtrabold = ImageFont.truetype('./fonts/xtrabold.ttf', 200)

        logging.info(f'Aircraft data: {aircraft_data}')

        airline_plus_flight_number = f'{aircraft_data.get("airline", "N/A")} {aircraft_data.get("flight", "N/A")}'.upper()
        draw_centered_text(draw, 10, airline_plus_flight_number, bold, 480)

        from_airport_code = aircraft_data.get('from', 'N/A')
        draw_centered_text(draw, 10, from_airport_code, xtrabold, 480, (255,0,0))

        origin_name = aircraft_data.get('origin', 'N/A').upper()
        draw_centered_text(draw, 225, origin_name, bold, 480)

        to_airport_code = aircraft_data.get('to', 'N/A')
        draw_centered_text(draw, 250, to_airport_code, xtrabold, 480, (255,0,0))

        destination_name = aircraft_data.get('destination', 'N/A').upper()
        draw_centered_text(draw, 465, destination_name, bold, 480)

        # Draw a horizontal line
        draw.line((15, 515, 465, 515), fill=(0, 0, 0), width=1)

        # Create an array of x/y positions for the text
        positions = [(15, 535), (15, 575), (15, 615)]
        
        if aircraft_data.get('altitude'):
            altitude = aircraft_data.get('altitude')
            pos = positions.pop(0)
            draw_key_value(draw, pos[0], pos[1], "ALTITUDE:", f'{altitude}FT', medium, bold)
        
        if aircraft_data.get('speed'):
            speed = aircraft_data.get('speed')
            pos = positions.pop(0)
            draw_key_value(draw, pos[0], pos[1], "SPEED:", f'{speed}KTS', medium, bold)
        
        if aircraft_data.get('type'):
            type = aircraft_data.get('type')
            pos = positions.pop(0)
            draw_key_value(draw, pos[0], pos[1], "TYPE:", f'{type}', medium, bold)


        try:
            # Rotate image to landscape
            rotated_image = image.rotate(90, expand=True)
             
            display.set_image(rotated_image)
            display.show()
        except Exception as display_error:
            logging.error(f'Display refresh failed: {display_error}')
        
    except Exception as e:
        logging.error(f'Display update failed: {e}')

def main():
    print ('flight tracker started')
    try:
        aircraft_data = get_closest_aircraft_details()
        
        if aircraft_data and 'route' in aircraft_data:
            update_display(aircraft_data)
        else:
            logging.info('No suitable aircraft found')
    except KeyboardInterrupt:
        logging.info('💀')
    except Exception as e:
        logging.error(f'Main loop error: {e}')

if __name__ == "__main__":
    main()