#Import all necessary libraries
from flask import Flask, session, render_template, request, redirect, url_for
import json
import requests

app = Flask(__name__)

@app.route("/converter", methods = ["POST", "GET"])
def converter():
    translated = ""
    dict_json = ""
    if request.method == "POST":
        text = request.form.get("english-box")
        url = "https://freekode.centeltech.com/api/minions?txt={}".format(text)
        response = requests.get(url).text
        print(response)
        dict_json = json.loads(response)
        print(dict_json["translated"])
        translated = dict_json["translated"]
    return render_template("language_converter.html", translated = translated)

@app.route("/weather", methods = ["POST", "GET"])
def weather():
    dict_json = ""
    weather_type = ""
    temp = ""
    city = False
    city_name = ""
    error = ""
    temp_f = ""
    temp_max = ""
    temp_maxf = ""
    temp_min = ""
    temp_minf = ""
    temp_data = []
    humid = ""
    temp_unit = ""
    if request.method == "POST":
        try: 
            city = True
            city_name = request.form.get("city_name")
            temp_unit = request.form.get("temp_unit")
            url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid=480f3b95ba02ce3527011ce105675d3f".format(city_name)
            response = requests.get(url).text
            print(response)
            dict_json = json.loads(response)
            print(dict_json)
            weather_type = dict_json["weather"][0]["main"]
            print(weather_type)
            temp = dict_json["main"]["temp"]
            temp_max = dict_json["main"]["temp_max"]
            temp_min = dict_json["main"]["temp_min"]
            humid = dict_json["main"]["humidity"]
            temp -= 273.15
            temp = "%.1f"%temp
            temp_f = (float(temp) * 9/5) + 32
            temp_max -= 273.15
            temp_max = "%.1f"%temp_max
            temp_maxf = (float(temp_max) * 9/5) + 32
            temp_min -= 273.15
            temp_min = "%.1f"%temp_min
            temp_minf = (float(temp_min) * 9/5) + 32
            city_name = dict_json["name"]
            temp_data = [dict_json, weather_type, temp, temp_f, city_name, city, temp_max, temp_maxf, humid, temp_min, temp_minf, temp_unit]
        except:
            city = False
            error = "Error 404. No city found."
    return render_template("weather.html", temp_data = temp_data, error = error)

if __name__ == "__main__":
    app.run(debug = True)