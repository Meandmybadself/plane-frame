
from inky.auto import auto
import logging
from dotenv import load_dotenv
import os
from adsb import get_closest_aircraft_details
from image import generate_image, generate_blank_image

load_dotenv()

LATITUDE = float(os.getenv('LATITUDE'))
LONGITUDE = float(os.getenv('LONGITUDE'))
RADIUS = int(os.getenv('RADIUS'))

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Add display initialization at the global level
display = auto()

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
    current_callsign = None
    print('flight tracker started')
    try:
        aircraft_data = get_closest_aircraft_details(LATITUDE, LONGITUDE, RADIUS)
        logging.info(f'Aircraft Data: {aircraft_data}')
        if aircraft_data:
            callsign = aircraft_data.get('callsign')
            
            if current_callsign and current_callsign != callsign:
                update_display(aircraft_data)
                current_callsign = callsign
        else:
            if current_callsign:
                image = generate_blank_image()
                current_callsign = None
                display.set_image(image)
                display.show()
    except KeyboardInterrupt:
        logging.info('💀')
    except Exception as e:
        logging.error(f'Main loop error: {e}')

if __name__ == "__main__":
    main()