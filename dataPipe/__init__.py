import logging
import pyodbc
import json
import os
import spotipy
import spotipy.util as util
import requests
import numpy as np

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

def feature_analysis(bucket_uris):
    final_buckets = []

    scope = 'user-library-read'
    token = get_token()
    if token:
        sp = spotipy.Spotify(auth=token)
    else:
        logging.info("Can't get token for", username)
        return

    for bucket in bucket_uris:
        avg_bucket_relevant_features = {}
        danceability = []
        energy = []
        instrumentalness = []
        liveness = []
        loudness = []
        speechiness = []
        valence = []

        features = sp.audio_features(bucket)

        for feature in features:
            danceability.append(feature['danceability']) 
            energy.append(feature['energy'])
            instrumentalness.append(feature['instrumentalness'])
            liveness.append(feature['liveness'])
            loudness.append(feature['loudness'])
            speechiness.append(feature['speechiness'])
            valence.append(feature['valence'])

        avg_bucket_relevant_features['danceability'] = np.average(danceability)
        avg_bucket_relevant_features['energy'] = np.average(energy)
        avg_bucket_relevant_features['instrumentalness'] = np.average(instrumentalness)
        avg_bucket_relevant_features['liveness'] = np.average(liveness)
        avg_bucket_relevant_features['loudness'] = np.average(loudness)
        avg_bucket_relevant_features['speechiness'] = np.average(speechiness)
        avg_bucket_relevant_features['valence'] = np.average(valence)
        
        final_buckets.append(avg_bucket_relevant_features)
        
    return final_buckets

def get_uris():
    uris = []
    buckets = []
    username = os.environ['AZURE_USER']
    password = os.environ['AZURE_PW']
    connection_string = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:discoverweeklys.database.windows.net,1433;Database=discoverWeeklys;Uid="+username+";Pwd="+password+";Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    logging.info(connection_string)
    cnxn = pyodbc.connect(connection_string)
    cursor = cnxn.cursor()
    cursor.execute('SELECT * FROM DiscoverWeeklyUris')
    for row in cursor.fetchall():
        uris.append(row[0])
    for i in range(0, len(uris), 30):
             buckets.append(uris[i:i + 30])
    return buckets

def main(req: func.HttpRequest) -> func.HttpResponse:
    uris = []
    logging.info('Python HTTP trigger function processed a request.')
    
    if (req.params.get('analysis') == 'features'):
        bucket_uris = get_uris()
        return func.HttpResponse(
            status_code = 200,
            body = json.dumps(feature_analysis(bucket_uris))
        )
    else:
        return func.HttpResponse(
            body = "Check req_type parameter",
            status_code = 404
        )