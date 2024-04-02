from flask import Flask, redirect, request
from config.config import CLIENT_ID_SPOTIFY, REDIRECT_URI, SECRET_KEY_SPOTIFY

authentication = Flask(__name__)

# Load variables from config.py
authentication.secret_key = SECRET_KEY_SPOTIFY
client_id = CLIENT_ID_SPOTIFY
redirect_uri = REDIRECT_URI

authorization_base_url = 'https://accounts.spotify.com/authorize'
token_url = 'https://accounts.spotify.com/api/token'
scope = 'user-read-private user-read-email'


def spotify_authentication():
    # Object to handle to session
    session_obj = {}

    session_obj['state'] = 'Testing'
    return redirect(authorization_base_url + '?' +
                    f'client_id={client_id}&response_type=code' +
                    f'&redirect_uri={redirect_uri}&scope={scope}&state={session_obj["state"]}')


@authentication.route('/login')
def login():
    return spotify_authentication()


@authentication.route('/callback')
def callback():
    code = request.args.get('code')

    # Saving and/or overwriting the code on .evn file
    with open('.env', 'a') as env_file:
        env_file.write(f'\nTOKEN_SPOTIFY={code}')

    return 'Authorization code saved on: .env'
    LOGGER.info(f"Generated new code: %s, {code}")

if __name__ == '__main__':
    authentication.run(debug=True)
