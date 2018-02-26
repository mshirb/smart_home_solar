import datetime
from time import sleep
import requests

from WeatherBaseClass import WeatherClass

url_head = 'https://api.darksky.net/forecast/'


class MyWeatherProvider(WeatherClass):

    def __init__(self, api_keys, location):
        self.api = str(api_keys['ForecastIO'])
        WeatherClass.__init__(self, location=location)
        self.name = 'ForecastIOProvider'
        print(self.name + ': Initialised')

    def updateWeather(self):
        print(self.name + ': Updating Weather Service')

        url = url_head + self.api + '/' + self.location
        response = requests.get(url, {'exclude': 'minutely, hourly', 'units': 'si'})
        if response.status_code != 200:
            return
        # print(response.json()['daily']['data'][0])

        resp = response.json()

        sunrise_unix = resp['daily']['data'][0]['sunriseTime']
        sunrise_dt = datetime.datetime.fromtimestamp(sunrise_unix)
        sunrise = {
            'hour': sunrise_dt.hour,
            'minute': sunrise_dt.minute
        }
        # print(sunrise)
        sunset_unix = resp['daily']['data'][0]['sunsetTime']
        sunset_dt = datetime.datetime.fromtimestamp(sunset_unix)
        sunset = {
            'hour': sunset_dt.hour,
            'minute': sunset_dt.minute
        }
        # print(sunset)

        temp_current = float(resp['currently']['temperature'])
        day_high = float(resp['daily']['data'][0]['temperatureHigh'])
        day_low = float(resp['daily']['data'][0]['temperatureLow'])

        print(self.name + ': Sunrise:\t' + str(sunrise['hour']) + ':' + str(sunrise['minute']))
        print(self.name + ': Sunset:\t' + str(sunset['hour']) + ':' + str(sunset['minute']))
        print(self.name + ': CurTC:\t' + str(temp_current) + 'C')
        print(self.name + ': MaxTC:\t' + str(day_high) + 'C')
        print(self.name + ': MinTC:\t' + str(day_low) + 'C')

        self.weather = \
            {
                'sunrise': sunrise,
                'sunset': sunset,
                'temp':
                    {
                        'high': day_high,
                        'low': day_low,
                        'current': temp_current
                    }
            }

        current_time = datetime.datetime.now()
        self.update_time = current_time + datetime.timedelta(minutes=30)
