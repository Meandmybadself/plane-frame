from image import generate_image
from adsb import get_closest_aircraft_details
from dotenv import load_dotenv
import os
import logging
load_dotenv()

LATITUDE = float(os.getenv('LATITUDE'))
LONGITUDE = float(os.getenv('LONGITUDE'))
RADIUS = int(os.getenv('RADIUS'))

logging.basicConfig(level=logging.INFO)

def main():
    print('==============================================')
    # Test data - simulating an aircraft data dictionary
    # test_aircraft_data = {
    #     "route": "LAX → JFK",
    #     "altitude": "35000",
    #     "speed": "460",
    #     "aircraft": "B738",
    #     "registration": "N12345",
    #     "airline": "Test Airlines",
    #     "flight": "TEST123",
    #     "from": "LAX",
    #     "to": "JFK",
    #     "destination": "JFK"
    # }


    # test_aircraft_data =  {'from': 'MSP', 'to': 'SFO', 'flight': 'SCX395', 'airline': 'Sun Country Airlines', 'origin': 'Minneapolis', 'origin_name': 'Minneapolis–Saint Paul International Airport / Wold–Chamberlain Field', 'destination': 'San Francisco', 'destination_name': 'San Francisco International Airport', 'altitude': 8725, 'speed': 262.7, 'type': 'B738', 'route': None}

    test_aircraft_data =  get_closest_aircraft_details(LATITUDE, LONGITUDE, RADIUS)

    logging.info(f'Test aircraft data: {test_aircraft_data}')

    try:
        # Generate the image using the same function as the main program
        image = generate_image(test_aircraft_data)
        
        # Save directly to test_image.jpg without rotation
        image.save('test_image.jpg')
        print("Test image generated successfully: test_image.jpg")
        
    except Exception as e:
        print(f'Error generating test image: {e}')

if __name__ == "__main__":
    main() 