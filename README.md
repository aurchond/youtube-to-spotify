# YoutubeToSpotify

Resources used:
Creating Spotify playlists - https://developer.spotify.com/console/post-playlists/

Searching for a song on Spotify - https://developer.spotify.com/console/get-search-item/

Required:
pip install requests
pip install google_auth_oauthlib
pip install --upgrade google-api-python-client

Instructions:
Need to create a Google API key as well as an OAuth 2.0 Client ID, then copy the client_id.json file into the project

Note:
The Spotify OAuth token expires semi-frequently, if a request/response error occurs it is most likely because of this, go to https://developer.spotify.com/console/post-playlists/ and use your Spotify user id to generate a new OAuth token

Inspired by:
https://github.com/TheComeUpCode/SpotifyGeneratePlaylist
