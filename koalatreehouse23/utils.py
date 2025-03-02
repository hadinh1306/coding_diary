import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
PLAYLIST_ID = f'spotify:playlist:{os.getenv("SPOTIFY_KOALATREEHOUSE23_PLAYLIST_ID")}'
SORTED_PLAYLIST_ID = (
    f'spotify:playlist:{os.getenv("SPOTIFY_PRIVATE_KTHOUSE_DANCE_FLOOR_PLAYLIST_ID")}'
)
