import datetime
import pytz
from geopy.geocoders import Nominatim 
from timezonefinder import TimezoneFinder 

if __name__ == '__main__':
    fmt = '%A %Y-%m-%d %H:%M'

    utc = pytz.utc
    utc_now = utc.localize(datetime.datetime.utcnow())
    geolocator = Nominatim(user_agent="MyApp")

    while True:
        city_name = input("Enter city name: ").strip()
        print(city_name)
        location = geolocator.geocode(city_name)
        
        if location is None:
            print("City not found. Please enter a valid city name.")
            continue
        
        obj = TimezoneFinder() 
        tz_name = obj.timezone_at(lng=location.longitude, lat=location.latitude) 
        
        if tz_name is None:
            print("Timezone not found for the given city.")
            continue

        try:
            tz = pytz.timezone(tz_name)
            tz_now = utc_now.astimezone(tz)
            print(f'{city_name}: {tz_now.strftime(fmt)}')
        except pytz.exceptions.UnknownTimeZoneError:
            print("Invalid timezone. Please enter a valid timezone.")
