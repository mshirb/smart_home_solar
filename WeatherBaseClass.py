import threading
from abc import abstractmethod

class WeatherClass(threading.Thread):

    def __init__(self, location):
        threading.Thread.__init__(self)
        self.location = location
        self.weather = {}
        self.update_time = None
        self.updateWeather()
        print(self.name + ': Base Class Initialised')

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

    @abstractmethod
    def updateWeather(self):
        pass
