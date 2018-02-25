import DEP_SolarCheck_Thread
from WunderWeather import weather
import GlobalSettings

import threading
from time import sleep
import datetime


class WundergroundSunsetSunriseThread(threading.Thread):
    def __init__(self, threadID, api_keys, high_temp, low_temp):
        """
        WundergroundSunsetSunriseThread works with Wunderground to provide weather smarts
        Using sunrise and sunset we run the solar check thread
        Using high temperature we can determine if it needs to go on
        :param threadID:    ID dedicated to this thread
        :param api_keys:    Dictionary of API Keys
        :param site_id:     Site ID for Solar Edge
        :param high_temp:   The highest temp that you are acceptable with
        :param low_temp:    The lowest temp that you are acceptable with
        :param PVLimit:     The kW limit for AC (eg. turn on AC when 2.5kW produced)
        """
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.api_keys = api_keys
        self.sThread = None
        self.high_temp = high_temp
        self.low_temp = low_temp

    def __start_sthread(self):
        # Start Thread
        if self.sThread is None:
            self.sThread = DEP_SolarCheck_Thread.SolarCheckThread('SE001', self.api_keys, self.site_id, self.PVLimit)
        else:
            GlobalSettings.SolarExitFlag = False
        if not self.sThread.is_alive():
            self.sThread.start()

    def __stop_sthread(self):
        # Stop Thread
        if self.sThread is not None:
            GlobalSettings.SolarExitFlag = True
            self.sThread.join()
            self.sThread = None

    def __sleeping(self, count):
        print(self.threadID + ': Sleeping for ' + str(count))
        sleep(count)

    def run(self):
        location = 'Australia/Googong'
        response_astro = None
        # WundergroundSunsetSunriseThread.__start_sthread(self)
        while not GlobalSettings.WunderExitFlag:
            ctime = datetime.datetime.now().time()
            # Update at 1 am
            # if (ctime.hour == 1) or response_astro is None:
            print(self.threadID + ': Updating Weather @ ' + str(datetime.datetime.now()))
            r = weather.Extract(self.api_keys['Wunderground'])
            response_astro = r.astronomy(location).data
            response_weather = r.daycast(location).data['simpleforecast']['forecastday'][0]
            ctime = response_astro['current_time']
            sunrise = response_astro['sunrise']
            print(self.threadID + ': Sunrise: ' + str(sunrise['hour']) + ':' + str(sunrise['minute']))
            sunset = response_astro['sunset']
            print(self.threadID + ': Sunset: ' + str(sunset['hour']) + ':' + str(sunset['minute']))
            day_high = float(response_weather['high']['celsius'])
            print(self.threadID + ': Temp High: ' + str(day_high) + 'C')
            day_low = float(response_weather['low']['celsius'])
            print(self.threadID + ': Temp Low: ' + str(day_low) + 'C')

            if day_high >= self.high_temp or day_high <= self.low_temp:
                if int(ctime['hour']) < int(sunrise['hour']):
                    print(self.threadID + ': Stop')
                    WundergroundSunsetSunriseThread.__stop_sthread(self)

                elif int(ctime['hour']) == int(sunset['hour']):
                    if int(ctime['minute']) >= int(sunset['minute']):
                        print(self.threadID + ': Stop')
                        WundergroundSunsetSunriseThread.__stop_sthread(self)

                elif int(ctime['hour']) > int(sunset['hour']):
                    print(self.threadID + ': Stop')
                    WundergroundSunsetSunriseThread.__stop_sthread(self)

                else:
                    print(self.threadID + ': Start')
                    WundergroundSunsetSunriseThread.__start_sthread(self)
            else:
                print(self.threadID + ': Stop')
                WundergroundSunsetSunriseThread.__stop_sthread(self)

            WundergroundSunsetSunriseThread.__sleeping(self, 30*60)
        print(self.threadID + ': Exiting...')