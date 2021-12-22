import requests
from config import TOKEN_OW


def get_cur_weather(lat, lon):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    param = {
        'appid': TOKEN_OW,
        'units': 'metric',
        'lat': lat,
        'lon': lon,
        'lang': 'ru',
    }

    r = requests.get(url, param)
    print(r.json())
    wind = ''
    if r.json()['wind']['deg'] > 337.5: wind = 'северный'
    elif r.json()['wind']['deg'] > 292.5: wind = 'северо-западный'
    elif r.json()['wind']['deg'] > 247.5: wind = 'западный'
    elif r.json()['wind']['deg'] > 202.5: wind = 'юго-западный'
    elif r.json()['wind']['deg'] > 157.5: wind = 'южный'
    elif r.json()['wind']['deg'] > 122.5: wind = 'юго-восточный'
    elif r.json()['wind']['deg'] > 67.5: wind = 'восточный'
    elif r.json()['wind']['deg'] > 22.5: wind = 'северо-восточный'
    else: wind = 'северный'

    res = f"Сейчас на улице {r.json()['weather'][0]['description']}, температура {r.json()['main']['temp']}C, " \
          f"ощущуется как {r.json()['main']['feels_like']}C" \
          f", ветер {wind} - {r.json()['wind']['speed']}м/с, влажность {r.json()['main']['humidity']} % \n" \
          # f"ближайшая метеостанция {r.json()['name']}"
    return res


