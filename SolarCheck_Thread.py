import pyfttt
import SolarEdge_Access
import GlobalSettings

import threading
from time import sleep


class SolarCheckThread(threading.Thread):
    def __init__(self, threadID, api_keys, se_siteid, PVLimit):
        """
        SolarCheckThread works with SolarEdge and IFTTT to turn on or off AC
        :param threadID:    ID dedicated to this thread
        :param api_keys:    Dictionary of API Keys
        :param se_siteid:   Site ID for Solar Edge
        :param PVLimit:     The kW limit for AC
        """
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.api_keys = api_keys
        self.site_id = se_siteid
        self.AirOnPVLimit = PVLimit

    def __sleeping(self, count):
        print(self.threadID + ': Sleeping for ' + str(count))
        sleep(count)

    def run(self):
        while not GlobalSettings.SolarExitFlag:
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

            if bdirection and (PVPower > self.AirOnPVLimit) and (sunit == 'kW') and not GlobalSettings.bAirConOn:
                print(self.threadID + ': Turning on AirConditioner')
                GlobalSettings.bAirConOn = True
                pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning', value1='On @ ' + str(PVPower) + sunit)
            elif bdirection and GlobalSettings.bAirConOn and (PVPower <= self.AirOnPVLimit) and (sunit == 'kW'):
                print(self.threadID + ': Turning off AirConditioner')
                GlobalSettings.bAirConOn = False
                pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning', value1=('Off @ ' + str(PVPower) + sunit))
            elif GlobalSettings.bAirConOn:
                print(self.threadID + ': Air Conditioning already on')

            if not bdirection and GlobalSettings.bAirConOn:
                print(self.threadID + ': Turning off AirConditioner')
                GlobalSettings.bAirConOn = False
                pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning', value1='Off')
            elif not bdirection:
                print(self.threadID + ': Still importing')

            SolarCheckThread.__sleeping(self, 10 * 60)

        if GlobalSettings.bAirConOn:
            print(self.threadID + ': Turning off AirConditioner due to exit')
            GlobalSettings.bAirConOn = False
            pyfttt.send_event(self.api_keys['IFTTT'], 'press_air_conditioning', value1='Off')
        print(self.threadID + ': Exiting...')