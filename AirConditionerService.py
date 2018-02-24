import threading
import datetime

import GlobalSettings
from WunderWeather import weather
import SolarEdge_Access
from time import sleep
import pyfttt

class ACThread(threading.Thread):
    def __init__(self, thread_name, api_keys, se_siteid, temps, pvlimit):
        threading.Thread.__init__(self)
        self.name = thread_name
        print(self.name + ': Initialising')
        self.api_keys = api_keys
        self.site_id = se_siteid
        self.temp_high = temps[0]
        self.temp_low = temps[1]
        self.PV_Limit = pvlimit

    def __SolarEdge_Run(self, sedge):
        print(self.name + ': Updating Solar @ ' + str(datetime.datetime.now()))
        success_read = True
        try:
            bdirection, sunit, pvpower, loadpower, gridpower = sedge.getcurrentpowerflow(self.site_id)
        except Exception:
            print(self.name + ': Error with Getting Data')
            success_read = False
            sleep(60)

        if success_read:
            if bdirection and (pvpower > self.PV_Limit) and (sunit == 'kW') and not GlobalSettings.bAirConOn:
                print(self.name + ': Turning on AirConditioner')
                GlobalSettings.bAirConOn = True
                pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning', value1='On @ ' + str(pvpower) + sunit)
            elif bdirection and GlobalSettings.bAirConOn and (pvpower <= self.PV_Limit) and (sunit == 'kW'):
                print(self.name + ': Turning off AirConditioner')
                GlobalSettings.bAirConOn = False
                pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning',
                                  value1=('Off @ ' + str(pvpower) + sunit))
            elif GlobalSettings.bAirConOn:
                print(self.name + ': Air Conditioning already on')

            if not bdirection and GlobalSettings.bAirConOn:
                print(self.name + ': Turning off AirConditioner')
                GlobalSettings.bAirConOn = False
                pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning', value1='Off')
            elif not bdirection:
                print(self.name + ': Still importing')

    def run(self):

        print(self.name + ': Starting')

        #Set Location for the Weather
        location = 'Australia/Googong'

        #Access the SolarEdge API
        sedge = SolarEdge_Access.SolarEdge(self.api_keys['SolarEdge'])

        #Set initial timing constraints
        current_time = datetime.datetime.now()
        weather_update_time = current_time
        solar_update_time = current_time

        if not GlobalSettings.ACFlag:
            print(self.name + ': Running @ ' + str(current_time))

        while not GlobalSettings.ACFlag:

            # Get Current Time
            current_time = datetime.datetime.now()

            # Update Weather
            if weather_update_time < current_time:
                weather_update_time = current_time + datetime.timedelta(minutes=30)
                print(self.name + ': Updating Weather @ ' + str(current_time))
                r = weather.Extract(self.api_keys['Wunderground'])
                response_astro = r.astronomy(location).data
                response_weather = r.daycast(location).data['simpleforecast']['forecastday'][0]
                temp_current = float(r.today_now(location).data['temp_c'])
                ctime = response_astro['current_time']
                sunrise = response_astro['sunrise']
                print(self.name + ': Sunrise:\t\t' + str(sunrise['hour']) + ':' + str(sunrise['minute']))
                sunset = response_astro['sunset']
                print(self.name + ': Sunset:\t\t' + str(sunset['hour']) + ':' + str(sunset['minute']))
                print(self.name + ': Current T:\t' + str(temp_current) + 'C')
                day_high = float(response_weather['high']['celsius'])
                if temp_current > day_high:
                    day_high = temp_current
                print(self.name + ': Temp High:\t' + str(day_high) + 'C')
                day_low = float(response_weather['low']['celsius'])
                if temp_current < day_low:
                    day_low = temp_current
                print(self.name + ': Temp Low:\t' + str(day_low) + 'C')

            # Update Solar Edge Information
            if solar_update_time < current_time and (day_high >= self.temp_high or day_high <= self.temp_low):
                solar_update_time = current_time + datetime.timedelta(minutes=10)

                if int(ctime['hour']) < int(sunrise['hour']):
                    print(self.name + ': Before Sunrise')

                elif int(ctime['hour']) == int(sunset['hour']) and int(ctime['minute']) >= int(sunset['minute']):
                        print(self.name + ': After Sunset')

                elif int(ctime['hour']) > int(sunset['hour']):
                    print(self.name + ': After Sunset')

                else:
                    print(self.name + ': Start')
                    self.__SolarEdge_Run(sedge)

            sleep(60)

        print(self.name + ': Exiting...')
