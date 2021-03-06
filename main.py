import os
import spotipy
import spotipy.util as util
from private import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, username, playlist_ids

os.environ['SPOTIPY_CLIENT_ID'] = CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI'] = REDIRECT_URI

"""
To find IDs of other playlists:
>>> playlists = sp.current_user_playlists()
>>> for p in playlists['items']: print(p['id'], p['name'])
"""


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


def main():
    scope = 'playlist-read-private'
    market = 'from_token'
    token = util.prompt_for_user_token(username, scope)

    sp = spotipy.Spotify(auth=token)

    # iterate through playlists
    for name, p_id in playlist_ids.items():
        print('Processing playlist', name)
        with open('playlists/' + name + '.txt', 'w+') as f:
            tracks = sp.user_playlist_tracks(username, p_id, market=market)
            write_tracks(tracks, f)
            while tracks['next']:
                tracks = sp.next(tracks)
                write_tracks(tracks, f)

    # sp.current_user_saved_tracks does not support market keyword, so directly use _get
    saved_tracks = sp._get('me/tracks', limit=50, offset=0, market=market)
    with open('playlists/saved_tracks.txt', 'w+') as f:
        write_tracks(saved_tracks, f)

if __name__ == '__main__':
    main()
