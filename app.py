from flask import Flask, render_template, request, session, send_file
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
import base64
from PIL import Image, ImageDraw
app = Flask(__name__)
auth_payload = {'client_id': '61bb4c3ea3c24253a738bd8f34956191', 'response_type': 'token', 'redirect_uri': 'https%3A%2F%2Fspotipy1.herokuapp.com%2Fresults'}
app.secret_key = 'bruhbruhbruhbruh'
@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('index.html')

# def serve_pil_image(pil_img):
#     img_io = BytesIO()
#     pil_img.save(img_io, 'PNG', quality=70)
#     img_io.seek(0)
#     return img_io
#     return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="Wrapt.png")

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
    # print(len(artists))
    session["toke"] = token
    # img_io = serve_pil_image(get_ig_story("weeks", artists, tracks))
    # img_io = get_ig_story("weeks", artists, tracks)
    # print(img_io)
    # base64EncodedStr = base64.b64encode(img_io.encode('utf-8'))
    # img_tag = "<img src='data:image/png;base64,'" + img_io + "</img>"
    # print(img_tag)
    # return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="Wrapt_Short.png")
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
    # img_io = serve_pil_image(get_ig_story("months", artists, tracks))
    # img_tag = "<img src='data:image/png;base64,'" + img_io + "</img>"
    # print(img_tag)
    # return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="Wrapt_Medium.png")
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
    # img_io = serve_pil_image(get_ig_story("years", artists, tracks))
    # img_tag = "<img src='data:image/png;base64,'" + img_io + "</img>"
    # print(img_tag)
    # return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="Wrapt_Long.png")
    return render_template('results.html', artists=artists, tracks=tracks, duration="long")

# @app.route('/igstory/<duration>', methods=['GET', 'POST'])
# def story(duration):
#     # return serve_pil_image(image)
#     pass

# def render_ig():
#     with Image.open('/static/igstory.png') as im:
#         draw = ImageDraw.Draw(im)
#         one = 'Kid Cudi'
#         draw.text((5, 5), one)
#         im.show()

if __name__ == '__main__':
    app.run(debug=True)
