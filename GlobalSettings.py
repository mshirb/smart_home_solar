
__version__ = '0.8'

bAirConOn = None
ACFlag = None
WeatherProcessFlag = None

def init():
    global bAirConOn, ACFlag
    bAirConOn = False
    ACFlag = False
    WeatherProcessFlag = True
