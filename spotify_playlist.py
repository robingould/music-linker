"""
Robin made dis :D
CLI tool to convert Spotify Playlists to text for importing to Jellyfin
Gets all the playlist songs, then sorts them by: Artist Name - Album Name - Song Name

Jellyfin file structure:
    Music
    ├── Some Artist
    │   ├── Album A
    │   │   ├── Song 1.flac
    │   │   ├── Song 2.flac
    │   │   └── Song 3.flac
    │   └── Album B
    │       ├── Track 1.m4a
    │       ├── Track 2.m4a
    │       └── Track 3.m4a
    └── Album X
        ├── Whatever You.mp3
        ├── Like To.mp3
        ├── Name Your.mp3
        └── Music Files.mp3
"""

import os
import re
import spotipy
from time import time
from dotenv import load_dotenv
from rich.console import Console
from spotipy.oauth2 import SpotifyOAuth
import tools.proc_animation as animation


load_dotenv()

console = Console()

scope = "user-library-read"
SPOTIPY_CLIENT_ID=os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET=os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI=os.getenv("SPOTIPY_REDIRECT_URI")


# Auth for Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=scope))


# Helper functions
def get_playlist_tracks(playlist_id):
    """
    get_playlist_tracks helper function

    Args: 
            playlist_id (any, required): Spotify URI, URL, or playlist ID.
    """
    results = sp.playlist_tracks(playlist_id, offset=1, market='US')
    tracks = results['items']
    
    while results['next']:
       results = sp.next(results)
       tracks.extend(results['items'])
    
    return tracks

# User instructions
print()
console.print("[bold green]Convert Spotify Playlists to txt for importing by Jellyfin later!")
console.print("[bold white]Steps:")
console.print("[bold]1. Right click the [underline]playlist's name[/underline]!")
console.print("[bold]2. Hover [underline]Share[/underline] [bold  white](at the bottom)!")
console.print("[bold]3. Left click [bold white ]\"[underline]Copy link to playlist[/underline]\"!")

# Get url, check if valid. Note, caveman logic
url = console.input('[bold medium_purple4]Paste in Spotify URL here!!: ')

regex = r"https://open.spotify.com/playlist/([a-zA-Z0-9]{22})"
while not re.search(regex, url):
    url = console.input('[bold dark_red]!!!!Needs to be valid Spotify URL!!!: ')

print()
console.print("[bold medium_purple4]Valid URL, processing tracks...")

# Processing timing
start = time()

# Start our processing animation
proc_anim = animation.Loading().start()

# Apply our helper function and print the number of tracks found for extra verification that we used the right url
tracks = get_playlist_tracks(url)
console.print(f"[italic light_slate_grey]Found [underline]{len(tracks)}[/underline] tracks!~            ")

# For each track, get track name, the artists that contributed, and the album name
track_info = []
for track in tracks:
    track_name = track['track']['name']
    artists = ', '.join([artist['name'] for artist in track['track']['artists']])
    album = track['track']['album']['name']
    track_info.append(f'{artists} - {album} - {track_name}')

# Simplest way I could think of grouping by artist and by album within each artist
track_info.sort()
console.print(f"[italic light_slate_grey]Processed [underline]{len(track_info)}[/underline] tracks successfully!~")
print()
# Write to a text file with the name of our playlist
playlist_name = sp.playlist(url)['name']
with open(f'./output/{playlist_name}.txt', 'w', encoding='utf-8') as file:
    for track in track_info:
        file.write(track + "\n")

# Stop our processing animation
proc_anim.stop()
print()
console.print(f"[bold pale_turquoise4]Output send to: {playlist_name}.txt (inside output)")
console.print(f'[bold pale_turquoise4]Time taken: [bold blue]{round(time() - start, 2)}s')
console.print("[italic light_slate_grey]*Reminder, formatting for Jellyfin: Artist Name - Album Name - Song Name")
