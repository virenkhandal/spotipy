from flask import Flask, render_template, request
from flask.templating import render_template_string
from spotify import *
import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)
import requests
from flask import request
# import matplotlib
# matplotlib.use('Agg')
app = Flask(__name__)

auth_payload = {'client_id': '61bb4c3ea3c24253a738bd8f34956191', 'response_type': 'token', 'redirect_uri': 'https%3A%2F%2Fspotipy1.herokuapp.com%2Fresults'}

@app.route('/', methods=['GET', 'POST'])
def homepage():
    requests.get('https://accounts.spotify.com/authorize?client_id=61bb4c3ea3c24253a738bd8f34956191&response_type=token&redirect_uri=https%3A%2F%2Fspotipy1.herokuapp.com%2Fresults/')
    return render_template('index.html')
    
@app.route('/en/login', methods=['GET', 'POST'])
def login():
    r = requests.get('https://accounts.spotify.com/authorize?client_id=61bb4c3ea3c24253a738bd8f34956191&response_type=token&redirect_uri=https%3A%2F%2Fspotipy1.herokuapp.com%2Fresults/')
    return render_template_string(r.text)

@app.route('/results/', methods=['GET', 'POST'])
def results():
    token = request.args.get('access_token')
    artists = getArtists(token)
    tracks = getTracks(token)
    return render_template('results.html', artists=artists, tracks=tracks)

if __name__ == '__main__':
    app.run(debug=True)
