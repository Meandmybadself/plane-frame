from math import radians, sin, cos, sqrt, atan2

def calculate_flight_progress(flight_data):
    """
    Calculate the relative progress of an aircraft between origin and destination.
    
    Args:
        flight_data (dict): Dictionary containing flight information with the following keys:
            - origin_lat: Origin latitude
            - origin_lon: Origin longitude
            - destination_lat: Destination latitude
            - destination_lon: Destination longitude
            - aircraft_lat: Current aircraft latitude
            - aircraft_lon: Current aircraft longitude
            
    Returns:
        float: A number between 0 and 1 representing the relative position of the aircraft
              between origin (0) and destination (1)
    """
    def haversine_distance(lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points on Earth.
        
        Args:
            lat1, lon1: Latitude and longitude of first point in degrees
            lat2, lon2: Latitude and longitude of second point in degrees
            
        Returns:
            float: Distance in nautical miles
        """
        # Convert coordinates to radians
        lat1, lon1 = map(radians, [lat1, lon1])
        lat2, lon2 = map(radians, [lat2, lon2])
        
        # Differences in coordinates
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        # Haversine formula
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        # Earth's radius in nautical miles
        r = 3440.065  # nautical miles
        
        return c * r
    
    # Extract coordinates
    origin_lat = flight_data['origin_lat']
    origin_lon = flight_data['origin_lon']
    dest_lat = flight_data['destination_lat']
    dest_lon = flight_data['destination_lon']
    aircraft_lat = flight_data['aircraft_lat']
    aircraft_lon = flight_data['aircraft_lon']
    
    # Calculate distances
    total_distance = haversine_distance(origin_lat, origin_lon, dest_lat, dest_lon)
    distance_traveled = haversine_distance(origin_lat, origin_lon, aircraft_lat, aircraft_lon)
    
    # Calculate progress ratio
    progress = distance_traveled / total_distance
    
    # Ensure the result is between 0 and 1
    return max(0, min(1, progress))