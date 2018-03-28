import datetime
import logging
import GlobalSettings

# # Logger information to print to screen and file
# logger = logging.getLogger('SHS_LoggingService')
# logger.setLevel(logging.DEBUG)
# fh = logging.FileHandler('SHS_LoggingService.log')
# ch = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)
# logger.addHandler(fh)
# logger.addHandler(ch)

def WritetoLog(thread_id, message, level = logging.DEBUG):
    msg = "{}: {}".format(thread_id, message)
    if(level == logging.DEBUG):
        GlobalSettings.logger.debug(msg)
    elif(level == logging.INFO):
        GlobalSettings.logger.info(msg)

