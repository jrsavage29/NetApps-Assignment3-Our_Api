##!/usr/bin/env python3
from ScraperKeys import weather_api_public_key
from flask import Flask 
from flask import jsonify
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import requests
import json  

app = Flask(__name__)
auth = HTTPBasicAuth()

#dictionary holding the users for the API
users = {
    "admin" : generate_password_hash("secret"),
}

#code used to verfiy the possible users for the API
@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return f"""<h1>Welcome {auth.current_user()} to the Services API!</h1>
                <p> You can access several services with this scraper:</p>
                    <ul>
                        <li> Weather info </li>
                        <li> Covid Statistics </li>
                        <li> And even add new Flask Usernames and Passwords </li>
                    </u1>"""

#get details on Weather by city
@app.route('/Weather') #Will accept HTTP GET requests
@auth.login_required
def get_weather():

    return """ <h1> A temporary placeholder response 1 </h1> """

#get details on COVID by state
@app.route('/COVID')
@auth.login_required
def get_covid_data():

    return """ <h1> A temporary placeholder response 2 </h1> """

#Add new user
@app.route('/Update') #Will only accept HTTP POST requests
@auth.login_required
def post_user_pass():

    #Make sure to insert new user in dictionary of users
    return """ <h1> A temporary placeholder response 3 </h1> """

if __name__== "__main__":
    app.run(host='127.0.0.1', port = 8081, debug = True)