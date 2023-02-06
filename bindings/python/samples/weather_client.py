import os
import requests
import json
import time

class WeatherClient():
    def __init__(self):
        api_key = os.environ.get('PRIVATE_API_KEY')
        city = 'berkeley,ca,usa'

        # See `https://developer.mozilla.org/en-US/docs/Web/API/Geolocation/getCurrentPosition`
        # to get current position.
        latitude = '37.8650809'
        longitude = '-122.2545076'

        forecast_num_days = 7

        self.current_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid={api_key}'
        self.forecast_url = f'https://api.openweathermap.org/data/2.5/forecast/daily?q={city}&units=imperial&cnt={forecast_num_days}&appid={api_key}'
        self.air_pollution_url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={latitude}&lon={longitude}&appid={api_key}'

        self.current_data = {}
        self.forecast_data = {}
        self.air_pollution_data = {}

    def query_weather(self):
        try:
            current_response = requests.get(self.current_url)
            print(current_response.text)
            self.current_data = json.loads(current_response.text)
        except:
            print('Failed to get current weather')

        try:
            forecast_response = requests.get(self.forecast_url)
            self.forecast_data = json.loads(forecast_response.text)
        except:
            print('Failed to get forecast weather')

        try:
            air_pollution_response = requests.get(self.air_pollution_url)
            print(air_pollution_response.text)

            self.air_pollution_data = json.loads(air_pollution_response.text)
        except:
            print('Failed to get air pollution.')

    def get_current_temperature(self):
        temp = self.current_data['main']['temp']
        return self.format_temperature(temp)

    def get_high_temperature(self):
        temp = self.forecast_data['list'][0]['temp']['max']
        return self.format_temperature(temp)

    def get_low_temperature(self):
        temp = self.forecast_data['list'][0]['temp']['min']
        return self.format_temperature(temp)

    def get_description(self):
        desc = self.current_data['weather'][0]['description']
        return desc.capitalize()

    def get_sunrise_time(self):
        sunrise = self.current_data['sys']['sunrise']
        return self.format_time(sunrise)

    def get_sunset_time(self):
        sunset = self.current_data['sys']['sunset']
        return self.format_time(sunset)

    def get_feels_like_temperature(self):
        temp = self.current_data['main']['feels_like']
        return self.format_temperature(temp)

    def get_pressure(self):
        pressure = self.current_data['main']['pressure']
        return self.format_pressure(pressure)

    def get_humidity(self):
        humidity = self.current_data['main']['humidity']
        return self.format_humidity(humidity)

    def get_wind_speed(self):
        wind_speed = self.current_data['wind']['speed']
        return self.format_wind_speed(wind_speed)

    def get_air_quality_index(self):
        air_quality_index = int(self.air_pollution_data['list'][0]['main']['aqi'])

        return air_quality_index

    def format_temperature(self, temp):
        return f'{round(temp)}'

    def format_time(self, t):
        t = time.strftime('%I:%M %p %Z', time.localtime(t))
        return f'{t}'

    def format_pressure(self, pressure):
        return f'{pressure} Pa'

    def format_humidity(self, humidity):
        return f'{humidity}%'

    def format_wind_speed(self, wind_speed):
        return f'{round(wind_speed)} mph'
