from io import BytesIO
import json
from flask import Flask, render_template, request, session, send_file
from spotify import *
import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)
import requests
from flask import request
import ast
app = Flask(__name__)

auth_payload = {'client_id': '61bb4c3ea3c24253a738bd8f34956191', 'response_type': 'token', 'redirect_uri': 'https%3A%2F%2Fspotipy1.herokuapp.com%2Fresults'}
app.secret_key = 'bruhbruhbruhbruh'
@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template('index.html')

def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG', quality=70)
    img_io.seek(0)
    # return img_io
    return send_file(img_io, mimetype='image/png', as_attachment=True, download_name="Wrapt.png")

@app.route('/short/', methods=['GET', 'POST'])
def short():
    code = request.args.get('code')
    auth_token_url = f"https://accounts.spotify.com/api/token"
    res = requests.post(auth_token_url, data={
        "grant_type":"authorization_code",
        "code":code,
        # "redirect_uri":"http://127.0.0.1:5000/short/",
        # "redirect_uri":"https://spotipy1.herokuapp.com/short/",
        "redirect_uri":"https://wrapt.azurewebsites.net/short/",
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
        # "redirect_uri":"https://spotipy1.herokuapp.com/medium/",
        "redirect_uri":"https://wrapt.azurewebsites.net/medium/",
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
        # "redirect_uri":"https://spotipy1.herokuapp.com/long/",
        "redirect_uri":"https://wrapt.azurewebsites.net/long/",
        "client_id":'61bb4c3ea3c24253a738bd8f34956191',
        "client_secret":'43e1501fc8d94c768d8af79f096395eb'
        })
    res_body = res.json()
    token = res_body.get("access_token")
    artists = getArtists(token, "long")
    tracks = getTracks(token, "long")
    session["toke"] = token
    return render_template('results.html', artists=artists, tracks=tracks, duration="long")

@app.route('/download', methods=['GET', 'POST'])
def download():
    artists = list(request.args.get('artists'))
    string = ''.join([str(elem) for elem in artists])
    arr = ast.literal_eval(string)    
    
    tracks = request.args.get('tracks')
    t_string = ''.join([str(elem) for elem in tracks])
    t_arr = ast.literal_eval(t_string)

    duration = request.args.get('duration')
    if duration == 'short':
        duration = 'weeks'
    elif duration == 'medium':
        duration = 'months'
    else:
        duration = 'years'
    img_io = get_ig_story(duration, arr, t_arr)
    return serve_pil_image(img_io)

if __name__ == '__main__':
    app.run(debug=True)
