"""Main entry point for the Plane Frame application."""

import logging
import time
from .config import config
from .tracking.adsb import tracker
from .display.screen import display
from .utils.image_generator import generate_image, generate_blank_image

def main():
    """Main application loop."""
    logging.basicConfig(level=logging.INFO)
    logging.info('Plane Frame started')
    
    if not config.validate():
        logging.error('Invalid configuration. Please check your .env file.')
        return
    
    try:
        while True:
            aircraft_data = tracker.get_closest_aircraft()
            
            if aircraft_data and aircraft_data.get('legs'):
                origin = aircraft_data['legs'][0]['code']
                destination = aircraft_data['legs'][-1]['code']
                
                if display.needs_update(origin, destination):
                    logging.info(f'Updating display with flight {origin} -> {destination}')
                    image = generate_image(aircraft_data)
                    display.update(image)
                    display.set_current_flight(origin, destination)
            else:
                if display.needs_update('', ''):
                    logging.info('No aircraft found, clearing display')
                    display.clear()
            
            time.sleep(config.REFRESH_INTERVAL)
            
    except KeyboardInterrupt:
        logging.info('Shutting down...')
    except Exception as e:
        logging.error(f'Application error: {e}')

if __name__ == '__main__':
    main() 