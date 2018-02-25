import datetime
from time import sleep
import requests

from WeatherBaseClass import WeatherClass

url_head = 'https://api.darksky.net/forecast/'


class MyWeatherProvider(WeatherClass):

    def __init__(self, api_keys, location):
        WeatherClass.__init__(self, location=location)
        self.name = 'ForecastIOProvider'
        self.api = api_keys['ForecastIO']
        print(self.name + ': Initialised')

    def updateWeather(self):
        print(self.name + ': Updating Weather Service')

        url = url_head + self.api + '/' + self.location

        current_time = datetime.datetime.now()
        self.update_time = current_time + datetime.timedelta(minutes=30)

    def run(self):
        print(self.name + ': Running')

        if self.update_time < datetime.datetime.now():
            self.updateWeather()

        sleep(60)


api_keys = {}
api_keys['ForecastIO'] = 'AAAA'
MyWeatherProvider(api_keys=api_keys, location=None)