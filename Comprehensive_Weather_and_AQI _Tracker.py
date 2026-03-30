import requests
import time
import argparse
from typing import Optional, Dict, Any, Tuple



def fetch_with_retry(url:str,params:Dict[str, Any],max_retries:int = 3)->Optional[Dict[str, Any]]:
    """fetches data from a URL"""

    for attempt in range(max_retries):
        try:

            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error on attempt {attempt+1}:{e}")
            
            
            if attempt<max_retries-1:
                wait_time = 2**attempt  
                print(f"Retrying in {wait_time} seconds...")


                time.sleep(wait_time)
#if fails to fetch data

            else:

                print("max retries reached. Failed to fetch data.")
                return None
    return None



def get_coordinates(city_name:str)->Optional[Tuple[float, float, str]]:
    print(f"searching for coordinates for '{city_name}'...")
    geocoding_url="https://geocoding-api.open-meteo.com/v1/search"
    params={"name": city_name, "count": 1, "language": "en", "format": "json"}



    data=fetch_with_retry(geocoding_url, params)
    
    if data and data.get('results'):
        result= data['results'][0]
        latitude= result['latitude']
        longitude= result['longitude']

        # this use the name/country to provide a clearer name  to the user
        display_name=f"{result.get('name', city_name)}, {result.get('country_code', '')}"

        print(f"Found coordinates: Lat={latitude}, Lon={longitude} for {display_name}")
        return latitude,longitude,display_name
    else:
        print(f"Could not find coordinates for city: {city_name}.")
        return None


def fetch_weather_and_aqi_data(latitude: float, longitude: float) -> Optional[Dict[str, Any]]:
    print("Getting real-time weather and AQI data...")

    api_url ="https://api.open-meteo.com/v1/forecast"
    params ={
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,apparent_temperature,precipitation,rain,weather_code,wind_speed_10m,wind_direction_10m",
        "hourly": "pm10,pm2_5", 

        "timezone": "auto",
        "forecast_hours" : 1 #get the most recent data

    }



#weather data
    weather_data=   fetch_with_retry(api_url, params)

    if not weather_data:
        return None

  
    aqi_url = "https://air-quality-api.open-meteo.com/v1/air-quality"


    aqi_params={
        "latitude": latitude,

        "longitude": longitude,
        "hourly": "european_aqi,us_aqi,pm10,pm2_5",
        "timezone": "auto",
        "forecast_hours": 1 #only get most recent data
    }


    aqi_data = fetch_with_retry(aqi_url, aqi_params)
    
    
    combined_data=weather_data
    combined_data['air_quality'] = aqi_data

    return combined_data


def get_weather_description(weather_code: int) -> str:
    """this converts WMO weather codes to a readable description."""
  

    if weather_code == 0:
        return "Clear Sky"

    elif 1 <= weather_code <= 3:

        return "Mainly Clear to Overcast"

    elif 45 <= weather_code <= 48:



        return "Fog and Depositing Rime Fog"


    elif 51 <= weather_code <= 55:

        return "Drizzle: Light, Moderate, and Dense"

    elif 61 <= weather_code <= 65:

        return "Rain: Slight, Moderate, and Heavy"

    elif 71 <= weather_code <= 75:

        return "Snowfall: Light, Moderate, and Heavy"

    elif 80 <= weather_code <= 82:

        return "Rain Showers: Light, Moderate, and Very Heavy"

    elif 95 <= weather_code <= 99:

        return "Thunderstorm"

    else:
        return "Weather condition not found"



def get_aqi_level(aqi_value: float) -> str:
  
    if aqi_value is None:
        return "N/A"    
    # This uses the European AQI (EAQI) simplified categories for context
    if 0 <= aqi_value <= 20:
        return "Very Good"

    elif 21 <= aqi_value <= 40:

        return "Good"
    elif 41 <= aqi_value <= 60:

        return "Fair"
    elif 61 <= aqi_value <= 80:
        return "Poor"

    elif 81 <= aqi_value <= 100:
        return "Very Poor"

    else:
        return "Extremely Poor "


def display_results(city_name: str, data: Dict[str, Any], display_name: str):
    # prints whether it get data or not


    if not data or not data.get('current') or not data.get('air_quality'):
        print("\n--- Failed to get complete data for display. ---")
        return



    #extracting weather data
    current =data['current']
    temperature =current.get('temperature_2m')
    app_temp =current.get('apparent_temperature')
    wind_speed    =current.get('wind_speed_10m')

    wind_direction   = current.get('wind_direction_10m')
    weather_code=current.get('weather_code')
    weather_desc=get_weather_description(weather_code)
    
    # extracting AQI data 
    aqi_data = data['air_quality'].get('hourly', {})


    # air Quality Index (European AQI is often simpler, but US AQI is also provided)
    e_aqi_values   = aqi_data.get('european_aqi', [None])
    us_aqi_values= aqi_data.get('us_aqi', [None])
    e_aqi = e_aqi_values[0] if e_aqi_values else None
    us_aqi = us_aqi_values[0] if us_aqi_values else None

 
    # particulate Matter (PM) levels
    pm10_values    =aqi_data.get('pm10', [None])
    pm25_values   =aqi_data.get('pm2_5', [None])
    pm10=pm10_values[0] if pm10_values else None
    pm25=pm25_values[0] if pm25_values else None



    print("\n" + "="*50)
    print(f" REAL-TIME REPORT FOR: {display_name.upper()}")
    print("="*50)


    # --- WEATHER SECTION
    print("\n--- WEATHER CONDITIONS ---")
    print(f"Temperature:        {temperature}°C")
    print(f"Feels Like:         {app_temp}°C")
    print(f"Conditions:         {weather_desc}")
    print(f"Wind Speed:         {wind_speed} km/h")
    print(f"Wind Direction:     {wind_direction}°")


    #  AQI SECTION 
    print("\nAIR QUALITY INDEX (AQI)")



    # choose which AQI to display and its context
    main_aqi  =e_aqi if e_aqi is not None else us_aqi
    aqi_standard    ="European AQI (EAQI)" if e_aqi is not None else ("US AQI" if us_aqi is not None else "AQI")


    if main_aqi is not None:

        aqi_status=get_aqi_level(main_aqi)
        print(f"{aqi_standard}:  {main_aqi} ({aqi_status})")

    else:
        print(f"Air Quality Index (AQI): not availiable")



    if pm25 is not None:
        print(f"PM2.5 : {pm25} µg/m³")


    if pm10 is not None:
        print(f"PM10 :{pm10} µg/m³")




    print("\n" + "="*50)
    print("="*50 + "\n")




def main_interactive():
    print("\n" + "="*50)
    print("Welcome to the Weather and AQI Tracker")
    print("="*50)
    
    city_name=input("Enter the name of the city: ")
    
    if not city_name:
        print("No city entered. Exiting program.")
        return



    # 1. get Coordinates
    coords=get_coordinates(city_name)
    if not coords:
        print("Program failed.")
        return

    latitude,longitude,display_name=coords



    # 2. fetch Data
    data=fetch_weather_and_aqi_data(latitude, longitude)
    


    # 3. display Results
    if data:
        display_results(city_name,data,display_name)
    else:
        print(f"complete weather or AQI data for {display_name} was not found.")



if __name__ =="__main__":
    main_interactive()
    
# if you run into a 'no module named requests' error