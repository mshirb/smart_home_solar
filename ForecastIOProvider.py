import requests
import threading
import datetime

url_head = 'https://api.darksky.net/forecast/'


class MyWeatherProvider(threading.Thread):

    def __init__(self, api_keys, lat, long):
        threading.Thread.__init__(self)
        self.name = 'ForecastIOWeatherProvider'
        self.api = api_keys['ForecastIO']
        self.latitude = lat
        self.longtitude = long
        self.weather = {}
        self.updateWeather()
        print(self.name + ': Initialised')

    def getTempHigh(self):
        try:
            return self.weather['temp']['high']
        except KeyError:
            return 'N/A'

    def getTempLow(self):
        try:
            return self.weather['temp']['low']
        except KeyError:
            return 'N/A'

    def getSunrise(self):
        try:
            return self.weather['sunrise']
        except KeyError:
            return 'N/A'

    def getSunset(self):
        try:
            return self.weather['sunset']
        except KeyError:
            return 'N/A'

    def updateWeather(self):
        print(self.name + ': Updating @ ' + str(datetime.datetime.now()))

    def run(self):
        print(self.name + ': Running')