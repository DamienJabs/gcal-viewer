import os
import requests
import json
from datetime import datetime, timedelta
from pprint import pprint as pp

icon_weight = {
    # The open weather api doesn't give me the weather for the next day in the free version. So i'm giving a weight on each weather to return the the ugliest weather for that day between 9h & 21h
    "01d": 1,  
    "02d": 2, 
    "03d": 3,
    "04d": 4,
    "10d": 5,
    "09d": 6,
    "11d": 7,
    "13d": 8,
    "50d": 9
}

def weather_request(day):
    try:
        # Get api key from the open weather api
        my_key = os.getenv("API_KEY")
        #Cachan city
        lat = "48.79"
        lon = "2.334"
        if day.lower() == "today":
            url = f"https://api.openweathermap.org/data/2.5/weather?units=metric&lat={lat}9&lon={lon}&appid={my_key}"
            return requests.get(url)
        if day.lower() in ["tomorrow", "demain"]:
            url = f"https://api.openweathermap.org/data/2.5/forecast?units=metric&lat={lat}&lon={lon}&appid={my_key}"
            return requests.get(url)
    except:
        return ""    
  
def weather_temp(day):
    data = weather_request(day).content # type: ignore
    json_data = json.loads(data)
    try:
        if day.lower() == "today":
            return str(round((json_data["main"]["temp"]))) +"°C"
        if day.lower() in ["tomorrow", "demain"]:          
            tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            temp_list = []
            # Retrieve tomorrow's temps between 9h - 21h and return average temp
            for i, forecast in enumerate(json_data.get("list", [])):
                if tomorrow_date in forecast.get("dt_txt"):
                    dt_txt = forecast.get("dt_txt")
                    dt = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
                    # Retrieve all temperatures between 9h & 21h and return the average
                    if 9 <= dt.hour <= 18:
                        temp_list.append(json_data["list"][i]["main"].get("temp"))
            return str(round(sum(temp_list) / len(temp_list))) +"°C"
    except: 
        return ""  

def weather_status(day: str):
    data = weather_request(day).content  # type: ignore
    json_data = json.loads(data)
    try:
        if day.lower() == "today":

            return json_data["weather"][0]["icon"]
        if day.lower() in ["tomorrow", "demain"]:           
            tomorrow_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            icon_list = []
            # Retrieve tomorrow's weather between 9h - 21h and retrieve worst weather (according to me..)
            for i, forecast in enumerate(json_data.get("list", [])):
                if tomorrow_date in forecast.get("dt_txt"):
                    dt_txt = forecast.get("dt_txt")
                    dt = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S")
                    # Retrieve all weather between 9h & 21h and return the worst based on its weight
                    if 9 <= dt.hour <= 18:
                        icon_list.append(json_data["list"][i]["weather"][0].get("icon"))
            return(max(icon_list))
    except: 
        return "📅"  