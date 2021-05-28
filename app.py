from flask import Flask, render_template, request, session
from flask.templating import render_template_string
from werkzeug.utils import redirect
from spotify import *
import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)
import requests
from flask import request
from urlpath import URL
import os
app = Flask(__name__)
auth_payload = {'client_id': '61bb4c3ea3c24253a738bd8f34956191', 'response_type': 'token', 'redirect_uri': 'https%3A%2F%2Fspotipy1.herokuapp.com%2Fresults'}

@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    auth_url = 'https://accounts.spotify.com/authorize?client_id=61bb4c3ea3c24253a738bd8f34956191&response_type=code&redirect_uri=https%3A%2F%2Fspotipy1.herokuapp.com%2Fresults%2F&scope=user-top-read'
    # auth_url = 'http://accounts.spotify.com/authorize?client_id=61bb4c3ea3c24253a738bd8f34956191&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Fresults%2F&scope=user-top-read'
    return redirect(auth_url)

@app.route('/results/', methods=['GET', 'POST'])
def results():
    code = request.args.get('code')
    # print("code: ", code)
    auth_token_url = f"https://accounts.spotify.com/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"authorization_code",
        "code":code,
        # "redirect_uri":"http://127.0.0.1:5000/results/",
        "redirect_uri":"https://spotipy1.herokuapp.com/results/",
        "client_id":'61bb4c3ea3c24253a738bd8f34956191',
        "client_secret":'43e1501fc8d94c768d8af79f096395eb'
        })
    res_body = res.json()
    # res.headers.add('Access-Control-Allow-Headers',
    #                      "Origin, X-Requested-With, Content-Type, Accept, x-auth")
    # print(res.json())
    session["toke"] = res_body.get("access_token")
    # res.set_cookie('access_token', session["toke"])
    print("token: ", session.get("toke"))
    # print("token: ", session['toke'])
    # artists = getArtists(session["toke"])
    # tracks = getTracks(session["toke"])
    return render_template('auth.html')

@app.route('/short', methods=['GET', 'POST'])
def short():
    token = session.get("toke")
    artists = getArtists(token, "short")
    tracks = getTracks(token, "short")
    session["toke"] = token
    return render_template('results.html', artists=artists, tracks=tracks, duration="short")

@app.route('/medium', methods=['GET', 'POST'])
def medium():
    token = session.get("toke")
    artists = getArtists(token, "medium")
    tracks = getTracks(token, "medium")
    session["toke"] = token
    return render_template('results.html', artists=artists, tracks=tracks, duration="medium")

@app.route('/long', methods=['GET', 'POST'])
def longs():
    token = session.get("toke")
    artists = getArtists(token, "long")
    tracks = getTracks(token, "long")
    session["toke"] = token
    return render_template('results.html', artists=artists, tracks=tracks, duration="long")

if __name__ == '__main__':
    app.run(debug=True)
