import argparse

import Wunderground_Thread
import settings

api_keys = {}
site_id = '635862'

def main():
    """
    Main run code for SmartHomeSolar
    :return:
    """
    settings.init()

    #Parse arguments in for API Keys
    parser = argparse.ArgumentParser()

    #Parse for SolarEdge API Key
    parser.add_argument("solaredge_key", help="SolarEdge Monitoring API Key", type=str)
    parser.add_argument("ifttt_key", help="IFTTT Webhook API Key", type=str)
    parser.add_argument("wunderground_key", help="Weather Underground API Key", type=str)
    args = parser.parse_args()

    api_keys['SolarEdge'] = args.solaredge_key
    api_keys['IFTTT'] = args.ifttt_key
    api_keys['Wunderground'] = args.wunderground_key

    checkingThread = Wunderground_Thread.WundergroundSunsetSunriseThread('WG001', api_keys, site_id, 30.0, 20.0, 2.5)

    checkingThread.start()


if __name__ == "__main__":
    main()
