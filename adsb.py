import logging
import requests
from math import radians, sin, cos, sqrt, asin
import json

# open airports.json
with open('./data/airports.json', 'r') as file:
    airports = json.load(file)

# open airlines.json
with open('./data/airlines.json', 'r') as file:
    airlines = json.load(file)

def clean_airport_name(airport_name):
    # create a list of words to remove
    words_to_remove = [' / Wold–Chamberlain Field']
    for word in words_to_remove:
        if word in airport_name:
            airport_name = airport_name.replace(word, '')
    return airport_name

def clean_airport_code(airport_code):
    if len(airport_code) == 4: 
        airport_code = airport_code[1:]
    return airport_code

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
        closest_aircraft_url = f'https://api.adsb.lol/api/0/routeset'
        logging.info(f'Aircraft Details URL: {closest_aircraft_url}')

        # Prepare request body
        request_body = {
            "planes": [
                {
                    "callsign": flight_number,
                    "lat": 0,
                    "lng": 0
                }
            ]
        }
        
        closest_aircraft_response = requests.post(closest_aircraft_url, json=request_body)
        
        if closest_aircraft_response.status_code != 200:
            logging.warning(f'API returned status code: {closest_aircraft_response.status_code}')
            return None
            
        closest_aircraft_data = closest_aircraft_response.json()

        # Handle new response format
        if isinstance(closest_aircraft_data, list) and len(closest_aircraft_data) > 0:
            route_info = closest_aircraft_data[0]
            if 'airport_codes' in route_info:
                # Clean and split airport codes
                airport_codes = route_info['airport_codes'].replace('?', '').replace(' ', '')
                legs = airport_codes.split('-') 
                route_legs = []
                
                for airport_code in legs:
                    if airport_code in airports:
                        airport_data = airports[airport_code]
                        route_legs.append({
                            'code': clean_airport_code(airport_code),
                            'name': clean_airport_name(airport_data['name']),
                            'latitude': airport_data['latitude_deg'],
                            'longitude': airport_data['longitude_deg']
                        })

                route = {
                    'flight_number': flight_number,
                    'airline': airlines[route_info.get('airline_code')] if route_info.get('airline_code') in airlines else '',
                    'legs': route_legs
                }
                
                return route
        return None
    except Exception as e:
        logging.error(f'Failed to fetch aircraft data: {e}')
        return None
    
def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points on Earth.
    """
    # Check for None or invalid values
    if None in (lat1, lon1, lat2, lon2):
        return float('inf')  # Return infinity for invalid coordinates
    
    try:
        # Convert coordinates to radians
        lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radius of Earth in kilometers
        return c * r
    except (ValueError, TypeError):
        return float('inf')  # Return infinity for calculation errors

def get_closest_aircraft_details(latitude, longitude, radius):
    try:
        url = f'https://api.adsb.lol/v2/point/{latitude}/{longitude}/{radius}'
        logging.info(f'Closest aircraft URL: {url}')
        response = requests.get(url)
        closest_aircraft_search_data = response.json()

        # filter out aircraft that are not airborne
        closest_aircraft_search_data['ac'] = [aircraft for aircraft in closest_aircraft_search_data['ac'] if aircraft['alt_baro'] != 'ground']

        # filter out aircraft whose callsigns begin with N - those are civilian aircraft & will not have a route in adsbdb
        closest_aircraft_search_data['ac'] = [aircraft for aircraft in closest_aircraft_search_data['ac'] if not aircraft['flight'].startswith('N')]
    
        # Sort the aircraft by distance, but only if they have valid coordinates
        closest_aircraft_search_data['ac'] = sorted(
            [aircraft for aircraft in closest_aircraft_search_data['ac'] if 'lat' in aircraft and 'lon' in aircraft],
            key=lambda x: haversine(latitude, longitude, x['lat'], x['lon'])
        )
        
        logging.info(f'Number of aircraft found: {len(closest_aircraft_search_data["ac"])}')

        for aircraft in closest_aircraft_search_data['ac']:
            if 'flight' in aircraft:
                logging.info(f'Fetching route data for {aircraft["flight"]}')
                route_data = get_route_by_callsign(aircraft["flight"])
                if route_data:
                    closest_aircraft_data = route_data
                    closest_aircraft_data.update({
                        'aircraft_lat': aircraft.get('lat', 'N/A'),
                        'aircraft_lon': aircraft.get('lon', 'N/A'),
                        'altitude': aircraft.get('alt_baro', 'N/A'),
                        'speed': aircraft.get('gs', 'N/A'),
                        'type': aircraft.get('t', 'N/A')
                    })
                    return closest_aircraft_data            
        return None
        
    except Exception as e:
        logging.error(f'API request failed: {e}')
        # log the response error
        # logging.error(f'Response error: {response.text}')
        return None 