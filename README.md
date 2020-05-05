# YoutubeToSpotify

## Table of Contents

- [Setup](#Setup)
- [Troubleshooting](#Troubleshooting)
- [Resources](#Resources)

## Setup

-Install dependencies using `pip install -r requirements.txt`

-Go to https://developer.spotify.com/console/post-playlists/, enter your Spotify user id and click Get Token to get your OAuth token. Enter your user id and OAuth token into the spotify_credentials.py file within the project

-Follow https://developers.google.com/youtube/v3/getting-started/ to enable OAuth for Youtube and download the client_id.json file and copy it into the project

-Run python playlist_converter.py, a URL will appear for you to authorize the application, click the URL and go through the process, you will get an authorization code, paste it back into the terminal

## Troubleshooting

The Spotify OAuth token expires semi-frequently, if a request/response error occurs it is most likely because of this, go to the spotify link above and generate a new OAuth token and copy it into the spotify_credentials.py file

## Resources

Spotify:

Creating Spotify playlists - https://developer.spotify.com/console/post-playlists/

Searching for a song on Spotify - https://developer.spotify.com/console/get-search-item/

Adding items to a Spotify playlist - https://developer.spotify.com/documentation/web-api/reference/playlists/add-tracks-to-playlist/

Youtube:

Getting the Youtube client and getting the user's Youtube playlists - https://developers.google.com/youtube/v3/docs/playlists/list?apix=true

Getting video URLs from a playlist - https://developers.google.com/youtube/v3/docs/playlistItems/list

Youtube DL library - https://github.com/ytdl-org/youtube-dl

Inspired by:

https://github.com/TheComeUpCode/SpotifyGeneratePlaylist
