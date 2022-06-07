import requests
from datetime import datetime

API_KEY = "67c56251ee16702602cf14ab9f65a802"
UNITS = 'metric'
MODE = 'json'
LANG = 'ru'
CNT = int(input('Введите количество дней на которые вы хотите получить информацию (максимум 16): '))


def get_weather(lat, lon):
    url = 'https://api.openweathermap.org/data/2.5/forecast/daily?lat=%s&lon=%s&appid=%s&mode=%s&lang=%s&units=%s&cnt=%s'
    address = url % (lat, lon, API_KEY, MODE, LANG, UNITS, CNT)
    response = requests.get(address)
    if response.status_code == 200:
        data = response.json()
        print('В городе ', data["city"]["name"], 'погода: ')
        for i in range(0, CNT):
            print("Дата ", datetime.utcfromtimestamp(int(data["list"][i]["dt"])).strftime('%Y-%m-%d %H:%M:%S'),
                  data["list"][i]["weather"][0]['description'], "Температура: ", "Min", data["list"][i]["temp"]["min"],
                  "Max", data["list"][i]["temp"]["max"], "Tемпература днём", data["list"][i]["temp"]["day"])
            print("Дополнительная информация: ")
            print("Время восхода", datetime.utcfromtimestamp(int(data["list"][i]["sunset"])).strftime('%H:%M:%S'),
                  "Время захода", datetime.utcfromtimestamp(int(data["list"][i]["sunrise"])).strftime('%H:%M:%S'))
            print()
    elif response.status_code == 401:
        print('Key protyx')
    elif response.status_code == 400:
        print('Bad requets')


# lat = int(input('Введите координаты: '))
# lon = int(input())
#get_weather(lat, lon)
get_weather(52.5508, 104.4556)