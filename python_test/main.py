import sys
import spotipy
import spotipy.util as util
import requests

scope = 'user-library-read'
username = "Denis Vashchenko"
ids = []

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)
    results = sp.user_playlist_tracks(user=username,playlist_id="spotify:playlist:37i9dQZEVXcCPpnWhFUkrg")
    for item in results['items']:
        track = item['track']
        print (track['name'] + ' - ' + track['artists'][0]['name'])
        ids.append(track['id'])
    print(ids)
else:
    print("Can't get token for", username)

results = sp.audio_features(ids)
print(results)

# for item in ids:
#     sp.audio_analysis(item)
