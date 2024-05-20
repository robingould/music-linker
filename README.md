# music-linker
 
Has this ever happened to you? 

"Oh no! My new friend just sent me a Spotify playlist but I don't even have Spotify premium!! Damn... that sucks... If ONLY there was an easy way to copy and paste that link and get the music sorted into playlists by similarity on my self-hosted Jellyfin server in under 15 mins, also I have seperate Spotify, Youtube, Soundcloud and downloaded playlists, it really sucks that they're all seperate and I can only listen to one at a time"

(The first thing has never happened to me I was just imagining what it would be like if someone asked me, haha if you wanna send me a Spotify playlist you can be the first pplease)

## Steal all your friends music easily with a single copy-paste! Connect your cross-platform music together, with the click of a button(s)! 

Uses RAG with GPT-4 ($0.004 per song basically) to fix Youtube "junk" names and get album names (for Jellyfin file system). (For example: Kylie Minogue - Can't Get You Out Of My Head (Official Video) -> Kylie Minogue - Fever - Can't Get You Out Of My Head) 
Uses Spotipy search as the service to augment GPT-4 responses.

```
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
```
