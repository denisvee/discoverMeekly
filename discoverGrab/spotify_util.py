import requests
import json
import os
def get_token():
    refresh_token = os.environ['SPOTIFY_REFRESH_TOKEN']
    client_id = os.environ['SPOTIFY_CLIENT_ID']
    client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    token_url = 'https://accounts.spotify.com/api/token'

    token_params = {'refresh_token': refresh_token, 'client_id': client_id,'client_secret': client_secret, 'grant_type': 'refresh_token', 'redirect_uri': 'https://denisvashchenko.com/'}
    response = requests.post(token_url, params=token_params, headers=headers)

    return response.json()['access_token']