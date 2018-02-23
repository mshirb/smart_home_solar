import SolarCheck_Thread
from WunderWeather import weather
import settings

import threading
from time import sleep
import datetime

class WundergroundSunsetSunriseThread(threading.Thread):
    def __init__(self, threadID, api_keys, site_id):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.api_keys = api_keys
        self.site_id = site_id
        self.sThread = None

    def __start_sthread(self):
        # Start Thread
        if self.sThread is None:
            self.sThread = SolarCheck_Thread.SolarCheckThread('SE001', self.api_keys, self.site_id)
        else:
            settings.SolarExitFlag = False
        if not self.sThread.is_alive():
            self.sThread.start()

    def __stop_sthread(self):
        # Stop Thread
        if self.sThread is not None:
            settings.SolarExitFlag = True
            self.sThread.join()
            self.sThread = None

    def __sleeping(self, count):
        print(self.threadID + ': Sleeping for ' + str(count))
        sleep(count)

    def run(self):
        location = 'Australia/Canberra'
        response = None
        # WundergroundSunsetSunriseThread.__start_sthread(self)
        while not settings.WunderExitFlag:
            ctime = datetime.datetime.now().time()
            # Update at 1 am
            if (ctime.hour == 1) or response is None:
                print(self.threadID + ': Updating Weather')
                r = weather.Extract(self.api_keys['Wunderground'])
                response = r.astronomy(location).data
            ctime = response['current_time']
            sunrise = response['sunrise']
            sunset = response['sunset']

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

            WundergroundSunsetSunriseThread.__sleeping(self, 30*60)
        print(self.threadID + ': Exiting...')