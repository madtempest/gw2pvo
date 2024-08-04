import requests
from datetime import datetime, timedelta
#“Powered by SunriseSunset.io“.

def get_sunrise_sunset(lat, lng):
    url = f"https://api.sunrisesunset.io/json?lat={lat}&lng={lng}&time_format=24"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        sunrise_time_str = data["results"]["sunrise"]
        sunset_time_str = data["results"]["sunset"]
        
        sunrise_time = datetime.strptime(sunrise_time_str, "%H:%M:%S")
        sunrise_time = sunrise_time.replace(second=0, microsecond=0)
        sunset_time = datetime.strptime(sunset_time_str, "%H:%M:%S")
        sunset_time = sunset_time.replace(second=0, microsecond=0)

        return sunrise_time, sunset_time
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None, None
    

def get_sunrise_tomorrow(lat, lng, tomorrow):
    url = f"https://api.sunrisesunset.io/json?lat={lat}&lng={lng}&date_start={tomorrow}&date_end={tomorrow}&time_format=24"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        sunrise_time_tomorrow_str = data["results"][0]["sunrise"]
        
        sunrise_time_tomorrow = datetime.strptime(sunrise_time_tomorrow_str, "%H:%M:%S")
        sunrise_time_tomorrow = sunrise_time_tomorrow.replace(second=0, microsecond=0)

        return sunrise_time_tomorrow
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None