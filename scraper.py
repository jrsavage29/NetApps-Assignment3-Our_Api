##!/usr/bin/env python3
from ScraperKeys import weather_api_public_key
from flask import Flask 
from flask import request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import requests
import json
from bs4 import BeautifulSoup  

app = Flask(__name__)
authenticate = HTTPBasicAuth()

#dictionary holding the users for the API
users = {
    "admin" : generate_password_hash("Secret"),
}

#code used to verfiy the possible users for the API
@authenticate.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@authenticate.login_required
def index():
    return f"""<h1>Welcome {authenticate.current_user()} to the Services API!</h1>
                <p> You can access several services with this scraper:</p>
                    <ul>
                        <li> Weather info </li>
                        <li> Covid Statistics </li>
                        <li> And even add new Flask Usernames and Passwords </li>
                    </u1>"""

#get details on Weather by city
@app.route('/Weather/<city>', methods = ['GET']) #Will accept HTTP GET requests
@authenticate.login_required
def get_weather(city):

    place = city
    r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={place}&appid={weather_api_public_key}")
    data = r.json()
    location = data['name']
    temperature = data['main']['temp']
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    weather_data = {"location":location, "temperature":temperature, "pressure": pressure, "humidity":humidity}
    json_string = json.dumps(weather_data)
    return json_string

#get details on COVID by state from this website: https://www.worldometers.info/coronavirus/country/us/
@app.route('/COVID/<state>', methods = ['GET']) #You will need to look up how scrap data from this website: https://realpython.com/beautiful-soup-web-scraper-python/
@authenticate.login_required
def get_covid_data(state):
    r = requests.get(f"https://www.worldometers.info/coronavirus/usa/{state}")
    soup = BeautifulSoup(r.content, 'html.parser')
    results = soup.find_all(id='maincounter-wrap')
    i = 0
    for result in results:
        num = result.find('span')
        if i == 0:
            cases = num.text.strip()
        elif i == 1:
            deaths = num.text.strip()
        elif i == 2:
            recovered = num.text.strip()
        i += 1
    covid_data = {"state": state, "total cases": cases, "deaths": deaths, "total recovered": recovered}
    json_string = json.dumps(covid_data)
    print(json_string)
    return json_string

#Add new user
@app.route('/Update/', methods = ['POST']) #Will only accept HTTP POST requests
@authenticate.login_required
def post_user_pass():
    # Make sure to insert new user into the dictionary of users
    credentials = request.form
    # print(credentials)

    hashPass = generate_password_hash(credentials["new_pass"])
    users.update({credentials["new_user"]: hashPass})
    # print(users)
    if credentials["new_user"] in users and check_password_hash(users.get(credentials["new_user"]), credentials["new_pass"]):
        return "Success"
    else:
        return "Failure"    


if __name__== "__main__":
    app.run(host='127.0.0.1', port = 8081, debug = True)