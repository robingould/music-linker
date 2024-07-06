from time import time
from rich.console import Console
from soundcloud import SoundCloud
import tools.proc_animation as animation

console = Console()

soundcloud = SoundCloud()

# user instructions
print()
console.print("[bold green]Convert Soundcloud Playlists to txt for importing by Jellyfin later!")
user = console.input('[bold medium_purple4]Paste Soundcloud Username: ')
me = soundcloud.get_user_by_username(user)
id = me.id
assert me.permalink == user

# Processing timing
start = time()

# Start our processing animation
proc_anim = animation.Loading().start()
playlists = soundcloud.get_user_playlists(id)
for playlist in playlists:
    with open(f"output/{playlist.title}.txt", "w", encoding='utf-8') as file:
        for track in playlist.tracks:
            track_cleaned = soundcloud.get_track(track.id)
            # normal - or en dash (?)
            if '-' in track_cleaned.title or '–' in track_cleaned.title:
                # replace en dashes in title
                track_cleaned.title.replace('–', '-')
                file.write(f"{track_cleaned.title} \n")
            else:
                file.write(f"{track_cleaned.user.username} - {track_cleaned.title} \n")
            
# Stop our processing animation
proc_anim.stop()
print()
console.print(f'[bold pale_turquoise4]Time taken: [bold blue]{round(time() - start, 2)}s')
console.print("[italic light_slate_grey]*Reminder, formatting for Jellyfin: Artist Name - Album Name - Song Name")