import argparse

import GlobalSettings
import AirConditionerService

api_keys = {}
site_id = '635862'

def main():
    """
    Main run code for SmartHomeSolar
    :return:
    """
    GlobalSettings.init()

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

    airconditioner_service = AirConditionerService.ACThread('AC001', api_keys=api_keys, temps=[30.0, 17.0], se_siteid=site_id, pvlimit=2.5)
    airconditioner_service.start()

if __name__ == "__main__":
    main()
