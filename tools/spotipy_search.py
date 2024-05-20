import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os
from dotenv import load_dotenv

load_dotenv()

scope = "user-library-read"
SPOTIPY_CLIENT_ID=os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET=os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI=os.getenv("SPOTIPY_REDIRECT_URI")

# Auth for Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=scope))

# Get search results for some song
def search_res(track_name):
    tracks = sp.search(track_name, limit=2)['tracks']['items']
    # For each track, get track name, the artists that contributed, and the album name
    query_list = ""
    for track in tracks:
        track_name = track['name']
        artists = ', '.join([artist['name'] for artist in track['artists']])
        #album = track['album']['name']
        query_list += f'{artists} - {track_name}\n'
    return query_list


#rag_output = rag_helper.query(theory_name, query_list)
#print(rag_output)