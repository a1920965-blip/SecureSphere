import requests

def weather_api(city:str="Srinagar"):
    API_KEY="162214fb676539bfc2d113a0778c9e70"
    request_url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=162214fb676539bfc2d113a0778c9e70"
    data=requests.get(request_url).json()
    context={"temp":data['main']['temp'],
            "weather_desc":data['weather'][0]['description'],
            'city':data['name'],
            'country':data['sys']['country']}
    print(context)
    return context