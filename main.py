import time
import requests
from inky.auto import auto
import logging
from PIL import Image, ImageDraw, ImageFont
import json
from dotenv import load_dotenv
import os
from adsb import get_closest_aircraft_details
from drawing import draw_shadowed_text, draw_key_value
from image import generate_image, generate_blank_image

load_dotenv()

LATITUDE = float(os.getenv('LATITUDE'))
LONGITUDE = float(os.getenv('LONGITUDE'))
RADIUS = int(os.getenv('RADIUS'))

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Add display initialization at the global level
display = auto()

# Initialize tracking variables
current_origin_airport_code = None
current_destination_airport_code = None

def update_display(aircraft_data):
    try:
        image = generate_image(aircraft_data)
        
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
    global current_origin_airport_code, current_destination_airport_code
    print('flight tracker started')
    while True:
        try:
            aircraft_data = get_closest_aircraft_details(LATITUDE, LONGITUDE, RADIUS)
            if aircraft_data:
                if current_origin_airport_code != aircraft_data.get('legs')[0]['code'] and current_destination_airport_code != aircraft_data.get('legs')[-1]['code']:
                    update_display(aircraft_data)
                    current_origin_airport_code = aircraft_data.get('legs')[0]['code']
                    current_destination_airport_code = aircraft_data.get('legs')[-1]['code']
            else:
                if current_origin_airport_code or current_destination_airport_code:
                    image = generate_blank_image()
                    current_origin_airport_code = None
                    current_destination_airport_code = None
                    display.set_image(image)
                    display.show()
            time.sleep(30)
        except KeyboardInterrupt:
            logging.info('💀')
            break  # Exit the loop on keyboard interrupt
        except Exception as e:
            logging.error(f'Main loop error: {e}')
            time.sleep(30)

if __name__ == "__main__":
    main()