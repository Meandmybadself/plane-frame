"""Aircraft tracking using ADS-B data."""

import logging
import requests
from typing import Optional, Dict, Any, List
from ..config import config

class ADSBTracker:
    """Tracks aircraft using ADS-B data."""
    
    def __init__(self):
        """Initialize the tracker."""
        self.base_url = "https://adsb.lol/api/0/aircraft"
    
    def get_closest_aircraft(self) -> Optional[Dict[str, Any]]:
        """Get details of the closest aircraft to the configured location."""
        try:
            params = {
                'lat': config.LATITUDE,
                'lon': config.LONGITUDE,
                'radius': config.RADIUS
            }
            
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if not data.get('ac'):
                return None
                
            # Sort aircraft by distance and get the closest one
            aircraft = sorted(data['ac'], key=lambda x: x.get('dist', float('inf')))[0]
            
            # Get flight details
            flight_info = self._get_flight_info(aircraft.get('flight', '').strip())
            if flight_info:
                return {
                    'registration': aircraft.get('r', 'Unknown'),
                    'flight_number': aircraft.get('flight', 'Unknown'),
                    'altitude': aircraft.get('alt_baro', 0),
                    'speed': aircraft.get('gs', 0),
                    'distance': aircraft.get('dist', 0),
                    'legs': flight_info.get('legs', [])
                }
            
            return None
            
        except Exception as e:
            logging.error(f'Failed to get aircraft data: {e}')
            return None
    
    def _get_flight_info(self, flight: str) -> Optional[Dict[str, Any]]:
        """Get detailed flight information."""
        if not flight:
            return None
            
        try:
            url = f"https://www.adsbdb.com/api/v0/flight/{flight.strip()}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f'Failed to get flight info: {e}')
            return None

# Create a singleton tracker instance
tracker = ADSBTracker() 