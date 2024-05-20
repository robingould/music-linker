"""
Robin made dis :D
CLI tool to convert Youtube Playlists to text for importing to Jellyfin
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

----------------------------------------------
A LOT of youtube videos in my playlists have goofy names (due to the uploader (not me lol))
We use openai inferences + RAG to fix this!
                        Youtube playlist 
                                | (via pytube)
                        Python list of songs
                                | (via OpenAI inference)
                        Cleaned up list             
                                |
                        Validate based on Spotify searches, get album names if they exist
                                |
                        Split into easily usable list and the list to download from youtube

"""
import re
from time import time
from rich.console import Console
from pytube import YouTube, Playlist
import tools.proc_animation as animation
import tools.spotipy_RAG_helper as rag_helper
import tools.spotipy_search as spotipy_searcher
from concurrent.futures import ThreadPoolExecutor, as_completed

console = Console()
# User instructions
print()
console.print("[bold red]Convert Youtube Playlists to txt for importing by Jellyfin later!")
console.print("[bold white]Steps:")
console.print("[bold]1. Copy the url, thats it lol!")

# Helper functions

def get_video_info(link):
    title = YouTube(link).title
    author = YouTube(link).author
    return title, author

# Lots of Youtube videos have stuff like "BBY GOYARD - Run Shannon Run (Official Music Video)", where we clearly don't want the "Official Music Video" part for querying
def remove_parens_junk(strings):
    pattern = re.compile(r'\[(.*?\b(?:Closed-Captioned|Music|Video|Clip|Audio|shot by|hq|hd|enhanced|4k)\b.*?|.*?)\]|\((.*?\b(?:Music|Video|Clip|Audio|shot by|hq|hd|enhanced|4k)\b.*?|.*?)\)')
    # Also replace any instances of 2 spaces with 1, delete quotes, and replace | with - 
    return [pattern.sub('', string).replace("  ", " ").replace("\"", "").replace("|", "-") for string in strings]

"""
 Pytube Part
"""

# Get url, check if valid. Note, caveman logic
url = console.input('[bold medium_purple4]Paste in Youtube Playlist URL here!!: ')

regex = r"https://(www.)?youtube.com/playlist\?list=[a-zA-Z0-9]{17}_[a-zA-Z0-9]{16}"
while not re.search(regex, url):
    url = console.input('[bold dark_red]!!!!Needs to be a valid Youtube Playlist URL!!!: ')
print()
console.print('[bold medium_purple4]Valid URL, processing videos... ')

# Processing timing
start = time()

# Start our processing animation
proc_anim = animation.Loading().start()

# Get youtube playlist
playlist = Playlist(url)
video_links = playlist.video_urls
playlist_name = playlist.title


console.print(f"[italic light_slate_grey]Found [underline]{len(video_links)}[/underline] tracks!~            ")


# Multithreading getting each video with 10 workers
processes = []
with ThreadPoolExecutor(max_workers=10) as executor:
    for url in video_links:
        processes.append(executor.submit(get_video_info, url))

# Do our process, well, processing. Puts into the correct format to be processed by our OpenAI prompt
videos = []
for task in as_completed(processes):
    # The song title 
    result = str(task.result()[0].encode('utf-8').decode('ascii', 'ignore'))
    # In many case, if theres no dash, we don't have the author of the song in the title and we just use the uploader
    if "-" not in result:
        result.replace("\n", "")
        # If we don't have -, append our song uploader as the author. 
        author = str(task.result()[1].encode('utf-8').decode('ascii', 'ignore')).replace("\n", "")
        result = result + " - " + author
    
    videos.append(result)

# Clean out strings
videos = remove_parens_junk(videos)

# Stop our processing animation
proc_anim.stop()
print()
console.print(f'[bold pale_turquoise4]Time taken to get our draft of song names + artists: [bold blue]{round(time() - start, 2)}s')

"""
 OpenAI + Spotify RAG Part
"""
# RAG timing
start = time()

# Start our processing animation
proc_anim = animation.Loading().start()

result_tracks = []
# For each "theoretically correct" artist + title in videos, we do retrieval augmented generation from Spotify and OpenAI. Costs about $0.004 per query.
for theory in videos:
    query_list = spotipy_searcher.search_res(theory)
    rag_output = rag_helper.query(theory, query_list)
    result_tracks.append(rag_output)

# Simplest way I could think of grouping by artist and by album within each artist
result_tracks.sort()
console.print(f'[bold pale_turquoise4]Time taken to search Spotify, then query GPT-4: [bold blue]{round(time() - start, 2)}s')

# Write our final titles, artists and albums out!
with open(f'./output/{playlist_name}.txt', 'w', encoding='utf-8') as file:
    for track in result_tracks:
        file.write(f"{track}\n")

# Stop our processing animation
proc_anim.stop()

print()
console.print(f"[bold pale_turquoise4]Output send to: {playlist_name}.txt (inside output)")


