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
import sys
from PIL import Image, ImageDraw
app = Flask(__name__)
auth_payload = {'client_id': '61bb4c3ea3c24253a738bd8f34956191', 'response_type': 'token', 'redirect_uri': 'https%3A%2F%2Fspotipy1.herokuapp.com%2Fresults'}
app.secret_key = 'bruhbruhbruhbruh'
@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('index.html')


@app.route('/short/', methods=['GET', 'POST'])
def short():
    code = request.args.get('code')
    auth_token_url = f"https://accounts.spotify.com/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"authorization_code",
        "code":code,
        # "redirect_uri":"http://127.0.0.1:5000/short/",
        "redirect_uri":"https://spotipy1.herokuapp.com/short/",
        "client_id":'61bb4c3ea3c24253a738bd8f34956191',
        "client_secret":'43e1501fc8d94c768d8af79f096395eb'
        })
    res_body = res.json()
    token = res_body.get("access_token")
    artists = getArtists(token, "short")
    tracks = getTracks(token, "short")
    session["toke"] = token
    return render_template('results.html', artists=artists, tracks=tracks, duration="short")

@app.route('/medium/', methods=['GET', 'POST'])
def medium():
    code = request.args.get('code')
    auth_token_url = f"https://accounts.spotify.com/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"authorization_code",
        "code":code,
        # "redirect_uri":"http://127.0.0.1:5000/medium/",
        "redirect_uri":"https://spotipy1.herokuapp.com/medium/",
        "client_id":'61bb4c3ea3c24253a738bd8f34956191',
        "client_secret":'43e1501fc8d94c768d8af79f096395eb'
        })
    res_body = res.json()
    token = res_body.get("access_token")
    artists = getArtists(token, "medium")
    tracks = getTracks(token, "medium")
    session["toke"] = token
    return render_template('results.html', artists=artists, tracks=tracks, duration="medium")

@app.route('/long/', methods=['GET', 'POST'])
def longs():
    code = request.args.get('code')
    auth_token_url = f"https://accounts.spotify.com/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"authorization_code",
        "code":code,
        # "redirect_uri":"http://127.0.0.1:5000/long/",
        "redirect_uri":"https://spotipy1.herokuapp.com/long/",
        "client_id":'61bb4c3ea3c24253a738bd8f34956191',
        "client_secret":'43e1501fc8d94c768d8af79f096395eb'
        })
    res_body = res.json()
    token = res_body.get("access_token")
    artists = getArtists(token, "long")
    tracks = getTracks(token, "long")
    session["toke"] = token
    return render_template('results.html', artists=artists, tracks=tracks, duration="long")


def render_ig():
    with Image.open('/static/igstory.png') as im:
        draw = ImageDraw.Draw(im)
        one = 'Kid Cudi'
        draw.text((5, 5), one)
        im.show()

if __name__ == '__main__':
    app.run(debug=True)
