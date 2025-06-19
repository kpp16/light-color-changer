import spotipy
import os
import requests
from PIL import Image
from io import BytesIO

from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

class SpotifyRunner:
    def __init__(self):
        self.scope = "user-read-currently-playing user-read-playback-state playlist-read-private user-library-read user-top-read"

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope,
                                                            client_id=SPOTIFY_CLIENT_ID,
                                                            client_secret=SPOTIFY_CLIENT_SECRET,
                                                            redirect_uri=SPOTIPY_REDIRECT_URI))

    def getImage(self):
        current = self.sp.current_playback()
        url = current["item"]["album"]["images"][0]['url']
        response = requests.get(url)

        image = Image.open(BytesIO(response.content))
        return image
    