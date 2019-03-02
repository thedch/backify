import sys
import os
import spotipy
import spotipy.util as util
from private import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, username, playlist_ids

os.environ['SPOTIPY_CLIENT_ID'] = CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = CLIENT_SECRET
os.environ['SPOTIPY_CLIENT_SECRET'] = REDIRECT_URI

def print_tracks(tracks:dict, f):
    for track in tracks['items']:
        # if track['track']['name'] == 'California Love': 
        import pdb; pdb.set_trace()
        track = track['track'] # painful json nesting
        f.write(track['name'] + ' (by) ' + track['artists'][0]['name'] + '\n')


scope = 'playlist-read-private'
token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(auth=token)
playlists = sp.current_user_playlists()

# iterate through playlists
for name, id in playlist_ids.items():
    print(f'Processing playlist {name}')
    with open(f'playlists/{name}.txt', 'w+') as f:
        results = sp.user_playlist(username, id, fields="tracks,next")
        tracks = results['tracks']
        print_tracks(tracks, f)
        while tracks['next']:
            tracks = sp.next(tracks)
            print_tracks(tracks, f)

# grab saved tracks as well
saved_tracks = sp.current_user_saved_tracks(limit=50)
with open(f'playlists/saved_tracks.txt', 'w+') as f:
    print_tracks(saved_tracks, f)
