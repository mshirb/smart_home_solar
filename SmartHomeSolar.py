import SolarEdge_Access
import pyfttt

import argparse

def main():
    """
    Main run code for SmartHomeSolar
    :return:
    """
    solaredge_api_key = ''
    ifttt_api_key = ''
    site_id = '635862'

    bAirConOn = False

    #Parse arguments in for API Keys
    parser = argparse.ArgumentParser()

    #Parse for SolarEdge API Key
    parser.add_argument("solaredge_key", help="SolarEdge Monitoring API Key", type=str)
    parser.add_argument("ifttt_key", help="IFTTT Webhook API Key", type=str)
    args = parser.parse_args()

    solaredge_api_key = args.solaredge_key
    ifttt_api_key = args.ifttt_key

    sedge = SolarEdge_Access.SolarEdge(solaredge_api_key)
    try:
        bdirection, sunit, PVPower, LoadPower, GridPower = sedge.getcurrentpowerflow(site_id)
    except Exception:
        print('Error with Getting Data')

    if bdirection:
        print('Your system is using all power from grid')
    else:
        print('Your system is importing power from grid\r\nYou should consider turning off AirCon')

    if bdirection and (PVPower > 3.00) and not bAirConOn:
        print('Turning on AirConditioner')
        bAirConOn = True
        pyfttt.send_event(ifttt_api_key, 'send_notification', value1='Air Conditioner On')

    if not bdirection and bAirConOn:
        print('Turning off AirConditioner')
        bAirConOn = False
        pyfttt.send_event(ifttt_api_key, 'send_notification', value1='Air Conditioner Off')


if __name__ == "__main__":
    main()
