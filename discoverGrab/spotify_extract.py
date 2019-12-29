import spotipy
import spotipy.util as util
import os

def get_songs():
    ids = []
    titles = []
    artists = []

    scope = 'user-library-read'
    token = os.environ['SPOTIFY_TOKEN']
    if token:
        global sp
        sp = spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)
    songs = sp.user_playlist_tracks(user='Denis Vashchenko',playlist_id='spotify:playlist:37i9dQZEVXcCPpnWhFUkrg')
    for item in songs['items']:
        track = item['track']
        titles.append(track['name'])
        artists.append(track['artists'][0]['name'])
        ids.append(track['id'])
    # Return an object of all titles, artists, and ids
    print(ids)
    print(titles)
    print(artists)

if __name__ == "__main__":
    get_songs()