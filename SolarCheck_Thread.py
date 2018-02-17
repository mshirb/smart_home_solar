import pyfttt
import SolarEdge_Access
import settings

import threading
from time import sleep

class SolarCheckThread(threading.Thread):
    def __init__(self, threadID, api_keys, se_siteid):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.api_keys = api_keys
        self.site_id = se_siteid

    def __sleeping(self, count):
        print(self.threadID + ': Sleeping for ' + str(count))
        sleep(count)

    def run(self):
        while not settings.SolarExitFlag:
            sedge = SolarEdge_Access.SolarEdge(self.api_keys['SolarEdge'])
            try:
                bdirection, sunit, PVPower, LoadPower, GridPower = sedge.getcurrentpowerflow(self.site_id)
            except Exception:
                print(self.threadID + ': Error with Getting Data')
                SolarCheckThread.__sleeping(self, 5*60)
                continue

            if bdirection:
                print(self.threadID + ': Your system is using all power from PV')
            else:
                print(self.threadID + ': Your system is importing power from grid')

            if bdirection and (PVPower > 2.00) and not settings.bAirConOn:
                print(self.threadID + ': Turning on AirConditioner')
                settings.bAirConOn = True
                pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning', value1='On @' + PVPower + sunit)
            elif bdirection and settings.bAirConOn and (PVPower <= 2.00):
                print(self.threadID + ': Turning off AirConditioner')
                settings.bAirConOn = False
                pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning', value1=('Off @' + PVPower + sunit))
            elif settings.bAirConOn:
                print(self.threadID + ': Air Conditioning already on')

            if not bdirection and settings.bAirConOn:
                print(self.threadID + ': Turning off AirConditioner')
                settings.bAirConOn = False
                pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning', value1='Off')
            elif not bdirection:
                print(self.threadID + ': Still importing')

                SolarCheckThread.__sleeping(self, 10 * 60)