##!/usr/bin/env python3
from ServicesKeys import marvel_api_public_key
from ServicesKeys import marvel_api_private_key
from flask import Flask
from flask import abort 
from flask import jsonify
from flask import request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import requests
import json
import time
import hashlib  


app = Flask(__name__)
auth = HTTPBasicAuth()

#dictionary holding the users for the API
users = {
    "admin" : generate_password_hash("secret"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():

    return f"""<h1>Welcome {auth.current_user()} to the Services API!</h1>
            <p>You can access the Marvel API from this API!</p>"""

@app.route('/Marvel') #Will only accpet HTTP GET requests
@auth.login_required
def get_marvel_stories():
    if 'story' in request.args:
        #setting up for requesting from the marvel API using server-side authentication
        timestamp = str(time.time())
        str2hash = timestamp + marvel_api_private_key + marvel_api_public_key
        md5hash = hashlib.md5(str2hash.encode()).hexdigest()

        r = requests.get(f"http://gateway.marvel.com/v1/public/stories/{request.args['story']}?apikey={marvel_api_public_key}&hash={md5hash}&ts={timestamp}")

        data = r.json()

        return data

    else:
        abort(400) #return an abort message with HTTP status code 400 (Bad Request)

#The following routes will make post requests which will be turned into HTTP GET requests by the scraper
@app.route('/Weather', methods = ['POST']) #Will accept HTTP POST requests
@auth.login_required
def get_weather():

    return """ <h1> A temporary placeholder response 1 </h1> """

@app.route('/COVID')
@auth.login_required
def get_covid_data():

    return """ <h1> A temporary placeholder response 2 </h1> """

@app.route('/Update') #Will only accept HTTP POST requests
@auth.login_required
def post_user_pass():

    #Make sure to insert new user in dictionary of users
    return """ <h1> A temporary placeholder response 3 </h1> """

if __name__== "__main__":
    app.run(host='127.0.0.1', port = 3000, debug = True)