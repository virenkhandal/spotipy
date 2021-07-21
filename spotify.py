import spotipy, requests
from PIL import Image, ImageDraw, ImageFont
from io import StringIO
from spotipy.oauth2 import SpotifyClientCredentials
import jinja2
env = jinja2.Environment()
env.globals.update(zip=zip)

top_artists = []
top_tracks = []

artists_endpoint = 'https://api.spotify.com/v1/me/top/artists'
tracks_endpoint = 'https://api.spotify.com/v1/me/top/tracks'

short_payload = {'time_range': 'short_term', 'limit': 10} 
mid_payload = {'time_range': 'medium_term', 'limit': 10} 
long_payload = {'time_range': 'long_term', 'limit': 10} 

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def getArtists(access_token, duration):
    if duration == "short":
        payload = short_payload
    elif duration == "medium":
        payload = mid_payload
    else:
        payload = long_payload
    auth = BearerAuth(access_token)
    # print(auth)
    artists = requests.get(artists_endpoint, params=payload, auth=auth)
    top_artists = []
    for i in artists.json().get("items"):
        artist = i.get("name")
        images_endpoint = i.get("images")
        # print(i.get('external_urls'))
        link = i.get('external_urls').get('spotify')
        image = i.get("images")[0].get("url")
        curr = [artist, image, link]
        top_artists.append(curr)
    return top_artists

def getTracks(access_token, duration):
    if duration == "short":
        payload = short_payload
    elif duration == "medium":
        payload = mid_payload
    else:
        payload = long_payload
    auth = BearerAuth(access_token)
    tracks = requests.get(tracks_endpoint, params=payload, auth=auth)
    top_tracks = []
    for i in tracks.json().get("items"):
        track = i.get("name")
        image = i.get('album').get('images')[0].get("url")
        # print(i.get('external_urls'))
        link = i.get('external_urls').get('spotify')
        curr = [track, image, link]
        top_tracks.append(curr)
    return top_tracks

def get_ig_story(duration, artists, tracks):
    image = Image.open("static/igstory.png")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(r'static/Quantico-Regular.ttf', 36) 
    time_font = ImageFont.truetype(r'static/Quantico-Bold.ttf', 80) 

    # Text to write onto image
    time = duration
    artist_one = concat(artists[0][0], font)
    artist_two = concat(artists[1][0], font)
    artist_three = concat(artists[2][0], font)
    artist_four = concat(artists[3][0], font)
    artist_five = concat(artists[4][0], font)

    track_one = concat(tracks[0][0], font)
    track_two = concat(tracks[1][0], font)
    track_three = concat(tracks[2][0], font)
    track_four = concat(tracks[3][0], font)
    track_five = concat(tracks[4][0], font)

    # Drawing text on image
    draw.text((650, 162), time, fill="black", font=time_font, align="left")

    draw.text((120, 1147), artist_one, fill="black", font=font, align="left")
    draw.text((120, 1212), artist_two, fill="black", font=font, align="left")
    draw.text((120, 1277), artist_three, fill="black", font=font, align="left")
    draw.text((120, 1342), artist_four, fill="black", font=font, align="left")
    draw.text((120, 1407), artist_five, fill="black", font=font, align="left")

    draw.text((650, 1147), track_one, fill="black", font=font, align="left")
    draw.text((650, 1212), track_two, fill="black", font=font, align="left")
    draw.text((650, 1277), track_three, fill="black", font=font, align="left")
    draw.text((650, 1342), track_four, fill="black", font=font, align="left")
    draw.text((650, 1407), track_five, fill="black", font=font, align="left")

    # Display image
    buf = StringIO.StringIO()
    image.save(buf, "PNG")
    contents = buf.getvalue()
    return contents

    # image.show()

def concat(text, font):
    split = text.split(" ")
    artist_breakpoint = len(split)
    for i in range(len(split) + 1):
        size = font.getsize(' '.join(split[:i]) + " ...")
        if size[0] > 300:
            artist_breakpoint = i
            break
    if artist_breakpoint < len(split):
        text = ' '.join(split[:artist_breakpoint]) + "..."
    else:
        text = ' '.join(split[:artist_breakpoint])
    return text

if __name__ == "__main__":
    pass
    # print(getArtists())
    # print(getTracks())