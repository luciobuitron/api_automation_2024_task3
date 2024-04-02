from dotenv import load_dotenv
import os

load_dotenv()
token_spotify = os.getenv("TOKEN_SPOTIFY")

USER_SPOTIFY = "312vih3vepthrzoqcnalign7ub74"
CLIENT_ID_SPOTIFY = "06fa290127c84445be2944ebc5ed4040"
SECRET_KEY_SPOTIFY = "632a80ac73b74cd6b150e6f00a5a9fb6"
SCOPE_SPOTIFY = "playlist_modify_public"
REDIRECT_URI = "uri=http://localhost:3000"
URL_SPOTIFY = "https://api.spotify.com/v1"
LIMIT_TRACKS = 50
HEADERS_SPOTIFY = {
    "Authorization": f"Bearer {token_spotify}",
    "Content-Type": "application/json"
    }