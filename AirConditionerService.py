import threading
import datetime

import GlobalSettings
import SolarEdge_Access
from time import sleep
import pyfttt
from LoggerService import WritetoLog
from flask import Flask, jsonify, logging
from logging import getLogger, StreamHandler, DEBUG

# app = Flask(__name__)
# app.logger.disabled = True
# logging.getLogger('werkzeug').disabled = True
# GlobalSettings.initLogger()
AC_CONTROL = True

# For Flask
# @app.route('/control/<level>')
# def control_level(level):
#     global AC_CONTROL
#     if(level == 'OFF'):
#         AC_CONTROL = False
#         return jsonify({'MESSAGE': 'Control of the AC has been turned off'})
#     elif(level == 'ON'):
#         AC_CONTROL = True
#         return jsonify({'MESSAGE': 'Control of the AC has been turned on'})


class ACThread(threading.Thread):
    def __init__(self, weatherprovider, api_keys, se_siteid, temps, pvlimit):
        global app
        threading.Thread.__init__(self)
        self.name = 'Air Conditioning'
        WritetoLog(self.name, 'Initialising')
        self.api_keys = api_keys
        self.site_id = se_siteid
        self.temp_high = temps[0]
        self.temp_low = temps[1]
        self.PV_Limit = pvlimit
        self.weatherprovider = weatherprovider

        #Initiate the Flask server here
        from flask import logging as flask_logging
        # app.run(host='0.0.0.0', use_reloader=False, debug=False)

        WritetoLog(self.name, 'Initialised...')

    def __SolarEdge_Run(self, sedge):
        global AC_CONTROL
        WritetoLog(self.name, 'Updating Solar @ ' + str(datetime.datetime.now()))
        success_read = True
        try:
            bdirection, sunit, pvpower, loadpower, gridpower = sedge.getcurrentpowerflow(self.site_id)
        except Exception:
            WritetoLog(self.name, 'Error with Getting Data')
            success_read = False
            sleep(60)

        if success_read:
            if bdirection and (pvpower > self.PV_Limit) and (sunit == 'kW') and not GlobalSettings.bAirConOn:
                if(AC_CONTROL):
                    WritetoLog(self.name, 'Turning on AirConditioner')
                    GlobalSettings.bAirConOn = True
                    pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning', value1='On @ ' + str(pvpower) + sunit)
                else:
                    WritetoLog(self.name, 'We are not in control of AC')
            elif bdirection and GlobalSettings.bAirConOn and (pvpower <= self.PV_Limit) and (sunit == 'kW'):
                if(AC_CONTROL):
                    WritetoLog(self.name, 'Turning off AirConditioner')
                    GlobalSettings.bAirConOn = False
                    pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning',
                      value1=('Off @ ' + str(pvpower) + sunit))
                else:
                    WritetoLog(self.name, 'We are not in control of AC')
            elif GlobalSettings.bAirConOn:
                WritetoLog(self.name, 'Air Conditioning already on')

            if not bdirection and GlobalSettings.bAirConOn:
                if(AC_CONTROL):
                    WritetoLog(self.name, 'Turning off AirConditioner')
                    GlobalSettings.bAirConOn = False
                    pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning', value1='Off @ Importing')
                else:
                    WritetoLog(self.name, 'We are not in control of AC')
            elif not bdirection:
                WritetoLog(self.name, 'Still importing')

    def run(self):
        global AC_CONTROL
        WritetoLog(self.name, 'Starting')

        #Set Location for the Weather
        location = 'Australia/Googong'

        #Access the SolarEdge API
        sedge = SolarEdge_Access.SolarEdge(self.api_keys['SolarEdge'])

        #Set initial timing constraints
        current_time = datetime.datetime.now()
        weather_update_time = current_time
        solar_update_time = current_time

        if not GlobalSettings.ACFlag:
            WritetoLog(self.name, 'Running @ ' + str(current_time))

        while not GlobalSettings.ACFlag:

            # Get Current Time
            current_time = datetime.datetime.now()

            # Update Weather
            day_high = self.weatherprovider.getTempHigh()
            sunrise = self.weatherprovider.getSunrise()
            sunset = self.weatherprovider.getSunset()
            ctime = current_time

            # Update Solar Edge Information
            if solar_update_time < current_time and (day_high >= self.temp_high or day_high <= self.temp_low):
                solar_update_time = current_time + datetime.timedelta(minutes=10)

                if int(ctime.hour) < int(sunrise['hour']):
                    WritetoLog(self.name, 'Before Sunrise')

                elif int(ctime.hour) > int(sunset['hour']):
                    WritetoLog(self.name, 'After Sunset')
                    if GlobalSettings.bAirConOn and AC_CONTROL:
                        WritetoLog(self.name, 'Turning off AirConditioner')
                        GlobalSettings.bAirConOn = False
                        pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning', value1='Off @ Sunset')
                    elif not AC_CONTROL:
                        WritetoLog(self.name, 'We are not in control of AC')

                else:
                    WritetoLog(self.name, 'Start')
                    self.__SolarEdge_Run(sedge)

            sleep(60)

        WritetoLog(self.name, 'Exiting...')
