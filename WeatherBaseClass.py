import threading
from abc import abstractmethod
import datetime
from time import sleep

import GlobalSettings
import LoggerService


class WeatherClass(threading.Thread):

    def __init__(self, location):
        threading.Thread.__init__(self)
        self.location = location
        self.weather = {}
        self.update_time = None
        self.updateWeather()
        LoggerService.WritetoLog(self.name, 'Base Class Initialised')

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

    def getTempCurrent(self):
        try:
            return self.weather['temp']['current']
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

    def run(self):
        LoggerService.WritetoLog(self.name, 'Running')
        while GlobalSettings.WeatherProcessFlag:
            if self.update_time < datetime.datetime.now():
                self.updateWeather()
            sleep(30)

