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
from image import generate_image

load_dotenv()

LATITUDE = float(os.getenv('LATITUDE'))
LONGITUDE = float(os.getenv('LONGITUDE'))
RADIUS = int(os.getenv('RADIUS'))

# Initialize logging
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)

# Add display initialization at the global level
display = auto()

def update_display(aircraft_data):
    try:
        image = generate_image(aircraft_data)
        
        try:
            # Rotate image to landscape
            rotated_image = image.rotate(90, expand=True)
             
            # Save the image to a jpeg and
            # image.save('image.jpg')
            
            display.set_image(rotated_image)
            display.show()
        except Exception as display_error:
            logging.error(f'Display refresh failed: {display_error}')
        
    except Exception as e:
        logging.error(f'Display update failed: {e}')

def main():
    print ('flight tracker started')
    try:
        aircraft_data = get_closest_aircraft_details(LATITUDE, LONGITUDE, RADIUS)
        
        if aircraft_data:
            
            update_display(aircraft_data)
        else:
            logging.info('No suitable aircraft found')
    except KeyboardInterrupt:
        logging.info('💀')
    except Exception as e:
        logging.error(f'Main loop error: {e}')

if __name__ == "__main__":
    main()