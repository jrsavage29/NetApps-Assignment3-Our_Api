##!/usr/bin/env python3
from ServicesKeys import marvel_api_public_key
from ServicesKeys import marvel_api_private_key
from flask import Flask
from flask import abort 
from flask import request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import requests
import json
import time
import hashlib  


app = Flask(__name__)
authenticate = HTTPBasicAuth()

#dictionary holding the users for the API
users = {
    "admin" : generate_password_hash("secret"),
}

@authenticate.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route('/')
@authenticate.login_required
def index():

    return f"""<h1>Welcome {authenticate.current_user()} to the Services API!</h1>
            <p>You can access the Marvel API from this API!</p>"""

@app.route('/Marvel', methods = ['GET']) #Will only accpet HTTP GET requests
@authenticate.login_required
def get_marvel_stories():
    if 'story' in request.args:
        #setting up for requesting from the marvel API using server-side authentication
        timestamp = str(time.time())
        str2hash = timestamp + marvel_api_private_key + marvel_api_public_key
        md5hash = hashlib.md5(str2hash.encode()).hexdigest()

        r = requests.get(f"http://gateway.marvel.com/v1/public/stories/{request.args['story']}?apikey={marvel_api_public_key}&hash={md5hash}&ts={timestamp}")

        data = r.json()

        return data["data"]["results"][0]["description"]

    else:
        abort(400) #return an abort message with HTTP status code 400 (Bad Request)

#The following routes will make post requests which will be turned into HTTP GET requests by the scraper
@app.route('/Weather/<city>', methods = ['POST']) #Will accept HTTP POST requests
@authenticate.login_required
def post_weather(city):

    #get the username and password for the scraper from the request body (the -d parameter)
    scraper_username = request.form["user"]
    scraper_password = request.form["pass"]

    r = requests.post(f'http://127.0.0.1:8081/Weather/{city}', auth = (scraper_username, scraper_password))
    if r.status_code  == 200:
        return r.json()
    
    elif r.status_code == 401:
        abort(401)
    
    else:
        abort(400)



@app.route('/COVID/<state>', methods = ['POST'])
@authenticate.login_required
def post_covid_data(state):
    # get the username and password for the scraper from the request body (the -d parameter)
    scraper_username = request.form["user"]
    scraper_password = request.form["pass"]

    r = requests.get(f'http://127.0.0.1:8081/COVID/{state}', auth=(scraper_username, scraper_password))

    # This might or might not need to be changed depending how the scraping works
    if r.status_code == 200:
        # print(r.content)
        # print(r.json())
        return r.content

    elif r.status_code == 401:
        abort(401)

    else:
        abort(400)

@app.route('/Update', methods = ['POST']) #Will only accept HTTP POST requests
@authenticate.login_required
def post_user_pass():
    #"user=scrape_user&pass=scrape_pass&new_user=user2&new_pass=pass2"
    scraper_username = request.form["user"]
    
    scraper_password = request.form["pass"]
    
    newUser = request.form['new_user']
    
    newPass = request.form['new_pass']
    
    r = requests.post(f'http://127.0.0.1:8081/Update/', data = {"new_user":newUser, "new_pass":newPass}, auth=(scraper_username, scraper_password))
    if r.status_code == 200:
        return r.content

    elif r.status_code == 401:
        abort(401)

    else:
        abort(400)



if __name__== "__main__":
    app.run(host='127.0.0.1', port = 3000, debug = True)