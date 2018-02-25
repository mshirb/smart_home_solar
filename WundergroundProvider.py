import datetime
from time import sleep

from WeatherBaseClass import WeatherClass
from WunderWeather import weather


class MyWeatherProvider(WeatherClass):

    def __init__(self, api_keys, location):
        self.api = str(api_keys['Wunderground'])
        WeatherClass.__init__(self, location=location)
        self.name = 'WundergroundProvider'
        print(self.name + ': Initialised')

    def updateWeather(self):
        print(self.name + ': Updating Weather Service')

        r = weather.Extract(self.api)
        response_astro = r.astronomy(self.location).data
        response_weather = r.daycast(self.location).data['simpleforecast']['forecastday'][0]
        temp_current = float(r.today_now(self.location).data['temp_c'])

        sunrise = response_astro['sunrise']
        sunset = response_astro['sunset']
        day_high = float(response_weather['high']['celsius'])
        if temp_current > day_high:
            day_high = temp_current
        day_low = float(response_weather['low']['celsius'])
        if temp_current < day_low:
            day_low = temp_current

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

    def run(self):
        print(self.name + ': Running')

        if self.update_time < datetime.datetime.now():
            self.updateWeather()

        sleep(60)