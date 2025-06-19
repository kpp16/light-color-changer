import spotipy
import os
import json
import requests
import asyncio
import time

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
from kasa import Discover, Module

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
LIGHT_HOST = os.getenv("LIGHT_HOST")
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def getImage():
    scope = "user-read-currently-playing user-read-playback-state playlist-read-private user-library-read user-top-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
                                                redirect_uri=SPOTIPY_REDIRECT_URI))

    current = sp.current_playback()
    json_data = json.dumps(current["item"], indent=4)
    url = current["item"]["album"]["images"][0]['url']
    print(url)
    response = requests.get(url)

    image = Image.open(BytesIO(response.content))
    return image

def get_dominant_color(image: Image.Image, resize=100):
    """
    Resize image and get the most common color.
    """
    # Resize to reduce processing
    img = image.copy()
    img = img.resize((resize, resize))

    # Get all pixels
    pixels = img.getcolors(resize * resize)
    # pixels = img.getcolors()

    # Find the most frequent color
    dominant_color = max(pixels, key=lambda item: item[0])[1]
    return dominant_color

def rgb_to_hsv(r, g, b):

    # R, G, B values are divided by 255
    # to change the range from 0..255 to 0..1:
    r, g, b = r / 255.0, g / 255.0, b / 255.0

    # h, s, v = hue, saturation, value
    cmax = max(r, g, b)    # maximum of r, g, b
    cmin = min(r, g, b)    # minimum of r, g, b
    diff = cmax-cmin       # diff of cmax and cmin.

    # if cmax and cmax are equal then h = 0
    if cmax == cmin: 
        h = 0
    
    # if cmax equal r then compute h
    elif cmax == r: 
        h = (60 * ((g - b) / diff) + 360) % 360

    # if cmax equal g then compute h
    elif cmax == g:
        h = (60 * ((b - r) / diff) + 120) % 360

    # if cmax equal b then compute h
    elif cmax == b:
        h = (60 * ((r - g) / diff) + 240) % 360

    # if cmax equal zero
    if cmax == 0:
        s = 0
    else:
        s = (diff / cmax) * 100

    # compute v
    v = cmax * 100
    return round(h), round(s), round(v)

async def main():
    dev = await Discover.discover_single(host=LIGHT_HOST,username=EMAIL,password=PASSWORD, discovery_timeout=10)
    try:
        await dev.update()

        if not dev.is_on:
            await dev.turn_on()

        light = dev.modules[Module.Light]
        while True:
            image = getImage()
            h,s,v = rgb_to_hsv(*get_dominant_color(image))
            try:
                await light.set_hsv(h,s,v)
            except Exception as e:
                print(e)
            time.sleep(1)
    except KeyboardInterrupt:    
        await dev.disconnect()

if __name__ == "__main__":
    asyncio.run(main())