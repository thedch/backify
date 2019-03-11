import sys
import os
import spotipy
import spotipy.util as util
from private import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, username, playlist_ids

os.environ['SPOTIPY_CLIENT_ID'] = CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI'] = REDIRECT_URI


def write_tracks(tracks:dict, f):
    for track in tracks['items']:
        track = track['track']
        if 'is_playable' in track:
            if track['is_playable']:
                flag = ''
            else:
                flag = ' !! NOT PLAYABLE'
        else:
            flag = ' !! PLAYABLE UNKNOWN'

        artists = ' (and) '.join(artist['name'] for artist in track['artists'])
        f.write(track['name'] + ' (by) ' + artists + flag + '\n')


scope = 'playlist-read-private'
market='from_token'
token = util.prompt_for_user_token(username, scope)

sp = spotipy.Spotify(auth=token)
playlists = sp.current_user_playlists()

# iterate through playlists
for name, id in playlist_ids.items():
    print('Processing playlist', name)
    with open('playlists/' + name + '.txt', 'w+') as f:
        tracks = sp.user_playlist_tracks(username, id, market=market)
        write_tracks(tracks, f)
        while tracks['next']:
            tracks = sp.next(tracks)
            write_tracks(tracks, f)

# grab saved tracks as well -- 'market' is not a supported keyword of
# current_user_saved_tracks(), you must edit the library source code
# for this to run
saved_tracks = sp.current_user_saved_tracks(limit=50, market=market)
with open('playlists/saved_tracks.txt', 'w+') as f:
    write_tracks(saved_tracks, f)
