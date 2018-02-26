
__version__ = '0.8'

bAirConOn = None
ACFlag = None
WeatherProcessFlag = None

def init():
    global bAirConOn, ACFlag, WeatherProcessFlag
    bAirConOn = False
    ACFlag = False
    WeatherProcessFlag = True
