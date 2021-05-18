from flask import Flask, render_template, request
from spotify import *
import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)
# import matplotlib
# matplotlib.use('Agg')
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def homepage():
    artists = getArtists()
    tracks = getTracks()
    return render_template('index.html', artists=artists, tracks=tracks)

if __name__ == '__main__':
    app.run(debug=True)
