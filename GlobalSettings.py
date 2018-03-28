import logging

__version__ = '0.8'

bAirConOn = None
ACFlag = None
WeatherProcessFlag = None
logger = None

def initLogger():
    global logger
    # Logger information to print to screen and file
    logger = logging.getLogger('SHS_LoggingService')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('SHS_LoggingService.log')
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)


def init():
    global bAirConOn, ACFlag, WeatherProcessFlag
    bAirConOn = False
    ACFlag = False
    WeatherProcessFlag = True
    initLogger()

