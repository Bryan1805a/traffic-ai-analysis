from geopy.geocoders import Nominatim
import time

def get_coordinates(location_name):
    if not location_name or location_name in ["Unknown", "Error"]:
        return None, None
    
    geolocator = Nominatim(user_agent="Bryan")

    query = f"{location_name}, Việt Nam"

    try:
        location = geolocator.geocode(query)
        time.sleep(1)

        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error when finding coordinates: {e}")
        return None, None