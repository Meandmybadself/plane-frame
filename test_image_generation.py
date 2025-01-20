from image import generate_image
from adsb import get_closest_aircraft_details
from dotenv import load_dotenv
import os
import logging
from image import generate_blank_image

load_dotenv()

LATITUDE = float(os.getenv('LATITUDE'))
LONGITUDE = float(os.getenv('LONGITUDE'))
RADIUS = int(os.getenv('RADIUS'))

logging.basicConfig(level=logging.INFO)

def main():
    print('==============================================')
    # Test data - simulating an aircraft data dictionary
    # test_aircraft_data = {'flight_number': 'SKW3836', 'airline': 'SKW', 'legs': [{'code': 'KMSP', 'name': 'Minneapolis–Saint Paul International Airport / Wold–Chamberlain Field', 'latitude': 44.880081, 'longitude': -93.221741}, {'code': 'KOMA', 'name': 'Eppley Airfield', 'latitude': 41.3032, 'longitude': -95.894096}], 'aircraft_lat': 44.855455, 'aircraft_lon': -93.404221, 'altitude': 8025, 'speed': 278.2, 'type': 'CRJ9'}
    # test_aircraft_data =  {'from': 'MSP', 'to': 'SFO', 'flight': 'SCX395', 'airline': 'Sun Country Airlines', 'origin': 'Minneapolis', 'origin_name': 'Minneapolis–Saint Paul International Airport / Wold–Chamberlain Field', 'destination': 'San Francisco', 'destination_name': 'San Francisco International Airport', 'altitude': 8725, 'speed': 262.7, 'type': 'B738', 'route': None}
    # test_aircraft_data = {'flight_number': 'SKW3886', 'airline': 'SkyWest', 'legs': [{'code': 'KMSP', 'name': 'Minneapolis–Saint Paul International Airport', 'latitude': 44.880081, 'longitude': -93.221741}, {'code': 'KSBN', 'name': 'South Bend Regional Airport', 'latitude': 41.708698, 'longitude': -86.317299}], 'aircraft_lat': 44.92868, 'aircraft_lon': -93.256792, 'altitude': 3425, 'speed': 178.6, 'type': 'E75L'}

    test_aircraft_data =  get_closest_aircraft_details(LATITUDE, LONGITUDE, RADIUS)


    logging.info(f'Test aircraft data: {test_aircraft_data}')

    try:
        if test_aircraft_data and len(test_aircraft_data['legs']) > 0:
            image = generate_image(test_aircraft_data)
            image.save('test_image.jpg', quality=100)
            print("Test image generated successfully: test_image.jpg")
        else:
            image = generate_blank_image()
            image.save('test_image.jpg', quality=100)
            print("Test image generated successfully: test_image.jpg")
        
    except Exception as e:
        print(f'Error generating test image: {e}')

if __name__ == "__main__":
    main() 