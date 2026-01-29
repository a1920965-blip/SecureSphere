import requests
import os
def weather_api(city:str="Srinagar"):
    request_url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={os.getenv('API_KEY')}"
    data=requests.get(request_url).json()
    context={"temp":data['main']['temp'],
            "weather_desc":data['weather'][0]['description'],
            'city':data['name'],
            'country':data['sys']['country']}
    print(context)
    return context