import datetime
import logging
import os
import spotipy
import spotipy.util as util
import pyodbc
import requests
import json
import itertools

import azure.functions as func

def get_token():
    refresh_token = os.environ['SPOTIFY_REFRESH_TOKEN']
    client_id = os.environ['SPOTIFY_CLIENT_ID']
    client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    token_url = 'https://accounts.spotify.com/api/token'
    token_params = {'refresh_token': refresh_token, 'client_id': client_id,'client_secret': client_secret, 'grant_type': 'refresh_token', 'redirect_uri': 'https://denisvashchenko.com/'}
    response = requests.post(token_url, params=token_params, headers=headers)
    return response.json()['access_token']    

def add_records(uris):
    server = 'tcp:discoverweeklys.database.windows.net'
    database = 'discoverWeeklys'
    username = os.environ['AZURE_USER']
    password = os.environ['AZURE_PW']
    driver= '{ODBC Driver 13 for SQL Server}'
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+',1433'+';DATABASE='+database+';UID='+username+';PWD='+password)
    cursor = cnxn.cursor()
    cursor.execut("SELECT * FROM ")
    for uri in uris:
        cursor.execute("INSERT INTO DiscoverWeeklyUris VALUES (?)", uri)
        cnxn.commit()
        logging.info("Storing" + uri)

def get_songs():
    uris = []
    scope = 'user-library-read'
    token = get_token()
    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)
    songs = sp.user_playlist_tracks(user='Denis Vashchenko',playlist_id='spotify:playlist:37i9dQZEVXcCPpnWhFUkrg')
    for item in songs['items']:
        track = item['track']
        uris.append(track['id'])
    logging.info(uris)
    return uris

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    uris = get_songs()
    add_records(uris)
    if mytimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function ran at %s', utc_timestamp)