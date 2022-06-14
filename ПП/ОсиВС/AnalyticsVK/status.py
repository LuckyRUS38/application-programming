import requests
import vk_api
import cfg
from datetime import datetime
from pytz import timezone

vk_token = cfg.vk_token
API_KEY = '67c56251ee16702602cf14ab9f65a802'
UNITS = 'metric'
MODE = 'json'
LANG = 'ru'
lat = 52.249796040547096
lon = 104.26627313621

weather_icons = {'01d': '☀', '02d': '⛅', '03d': '☁', '04d': '☁', '09d': '🌧', '10d': '💧', '11d': '⛈', '13d': '❄',
                 '50d': '🌫'}


def get_weather():
    url = 'https://api.openweathermap.org/data/2.5/weather?appid=%s&lat=%s&lon=%s&units=%s&lang=%s&mode=%s'
    address = url % (API_KEY, lat, lon, UNITS, LANG, MODE)
    response = requests.get(address)
    if response.status_code == 200:
        data = response.json()
        return data['weather'][0]['description'], data['weather'][0]['icon'], data['main']['temp']
    else:
        print('HTTP code: ' + str(response.status_code))
        return


def get_datetime():
    irkutsk = timezone('Asia/Irkutsk')
    datetime_now = datetime.now(irkutsk)
    str_date = datetime_now.strftime('%d.%m.%Y')
    str_time = datetime_now.strftime('%H:%M')
    return str_date, str_time

date_str, time_str = get_datetime()
weather_desc, weather_icon_id, weather_temp = get_weather()

if weather_icon_id in weather_icons:
    weather_icon = weather_icons[weather_icon_id]
else:
    weather_icon = '❓'

status_str = '📅 %s, ⏰ %s, %s %s 🌡%s°C' % (date_str, time_str, weather_icon, weather_desc, round(weather_temp, 1))

vk_session = vk_api.VkApi(token=vk_token)
vk = vk_session.get_api()

vk.status.set(text=status_str)