import requests
import configparser
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/') #this is to tell flask that we want something to be routed to the webpage
def weather_dashboard():
    return render_template('home.html') #automatically searches for the template folder and runs the html file there

@app.route('/results', methods=["POST"])
def render_results():
    country_code = request.form['countryCode']
    zip_code = request.form['zipCode']
    data = get_weather_results(country_code, zip_code, get_api_key())
    print(data)
    temp = "{0:2f}".format(data["main"]["temp"])
    feels_like = "{0:2f}".format(data["main"]["feels_like"])
    weather = data["weather"][0]["main"]
    location = data["name"]

    return render_template('results.html', location =location, temp=temp, weather=weather, feels_like=feels_like)

def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweather']['api']

def get_weather_results(country_code, zip_code, api_key):
    api_url = "http://api.openweathermap.org/data/2.5/weather?zip={},{}&units=metric&appid={}".format(zip_code, country_code, api_key)
    print(api_url)
    r = requests.get(api_url)
    return r.json()


if __name__ =='__main__': #this is to make sure that only one instance is running
    app.run()