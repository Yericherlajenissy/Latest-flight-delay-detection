import requests
from datetime import datetime

# Define the latitude, longitude, and API key
lat = 40.7128  # Example: Latitude for New York City
lon = -74.0060  # Example: Longitude for New York City
api_key = "fddc902e4b2f5af4fc20b00d2bfb3bf9"  # Your API key

# Construct the API call URL with 'units=imperial' to get temperature in Fahrenheit
url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=imperial"

# Make the API request
response = requests.get(url)

# Check the response status
if response.status_code == 200:
    # Parse the JSON response
    forecast_data = response.json()

    # Iterate through the list of forecast entries for the next 5 days
    for i in range(0, len(forecast_data['list']), 8):  # Each day has 8 3-hour intervals
        forecast = forecast_data['list'][i]
        
        # Extract datetime information
        dt = forecast['dt']
        forecast_time = datetime.utcfromtimestamp(dt)  # Convert timestamp to datetime
        year = forecast_time.year
        month = forecast_time.month
        day = forecast_time.day
        hour = forecast_time.hour

        # Extract weather data
        temp = forecast['main']['temp']  # Temperature in Fahrenheit
        dewp = forecast['main']['temp_min']  # Assuming 'temp_min' as dew point in Fahrenheit
        humid = forecast['main']['humidity']  # Humidity
        wind_speed = forecast['wind']['speed']  # Wind speed in m/s
        visib = forecast.get('visibility', 10000) / 1000  # Visibility in km (default 10 km)

        # Print the values in the required format
        print(f"{year},{month},{day},{hour},{temp:.2f},{dewp:.2f},{humid:.2f},{wind_speed:.5f},{visib:.1f}")
else:
    print(f"Error: Unable to fetch data, status code {response.status_code}")
