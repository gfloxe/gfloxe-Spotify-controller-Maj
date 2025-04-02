import sys
import os

# Construire le chemin absolu vers le dossier contenant credentials.py
credentials_dir = os.path.join(os.path.expanduser("~"), "Documents", "SpotifyControllerApp")

# Ajouter le dossier au sys.path s'il n'est pas déjà présent
if credentials_dir not in sys.path:
    sys.path.append(credentials_dir)

# Importer les identifiants depuis credentials.py
from credentials import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI # type: ignore

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from utils import log_error

class SpotifyAPI:
    def __init__(self):
        try:
            self.sp = Spotify(auth_manager=SpotifyOAuth(
                client_id=SPOTIFY_CLIENT_ID,
                client_secret=SPOTIFY_CLIENT_SECRET,
                redirect_uri=SPOTIFY_REDIRECT_URI,
                scope="user-read-playback-state,user-modify-playback-state"
            ))
        except Exception as e:
            log_error(f"Erreur lors de l'initialisation de l'API Spotify : {e}")
            raise e

    def get_current_song(self):
        try:
            playback = self.sp.current_playback()
            if playback and playback.get("item"):
                song_title = playback["item"]["name"]
                artist_name = ", ".join(artist["name"] for artist in playback["item"]["artists"])
                duration_ms = playback["item"]["duration_ms"]
                progress_ms = playback["progress_ms"]
                album_image_url = playback["item"]["album"]["images"][0]["url"]
                return song_title, artist_name, progress_ms, duration_ms, album_image_url
            else:
                return "En attente d'une lecture", "", 0, 0, None
        except Exception as e:
            log_error(f"Erreur lors de la récupération des informations de la chanson : {e}")
            return "Erreur", "", 0, 0, None
