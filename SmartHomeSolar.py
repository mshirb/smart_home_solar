import SolarEdge_Access

api_key = '4VJK000831ZQJKMAWLGOF5ML6X6TL9I5'
site_id = '635862'

bAirConOn = False

sedge = SolarEdge_Access.SolarEdge(api_key)
bdirection, sunit, PVPower, LoadPower, GridPower = sedge.getcurrentpowerflow(site_id)

if bdirection:
    print('Your system is using all power from grid')
else:
    print('Your system is importing power from grid\r\nYou should consider turning off AirCon')

if bdirection and (PVPower > 3.00) and not bAirConOn:
    print('Turning on AirConditioner')

if not bdirection and bAirConOn:
    print('Turning off AirConditioner')
