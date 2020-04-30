import json
import requests

from spotify_credentials import user_id, OAuth_token


class PlaylistConverter:

    def __init__(self):
        self.user_id = user_id
        self.OAuth_token = OAuth_token

    # get the youtube client
    def youtube_login(self):
        pass

    # create a new spotify playlist
    def make_spotify_playlist(self):
        request_body = json.dumps({
            "name": "Youtube Playlist",
            "description": "This playlist was created from your corresponding Youtube playlist",
            "public": True
        })
        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            self.user_id)

        bearerToken = "Bearer {}".format(OAuth_token)
        content_headers = {
            "Content-Type": "application/json",
            "Authorization": bearerToken,
        }
        response = requests.post(
            query,
            data=request_body,
            headers=content_headers
        )
        response_json = response.json()

        # return the playlist id
        return response_json["id"]

    # get the existing playlist from youtube
    def get_youtube_playist(self):
        pass

    # get the corresponding spotify_url for each song in the youtube playlist
    def get_spotify_song_url(self):
        pass

    # add the list of songs into the spotify playlist
    def add_to_spotify_playlist(self):
        pass


newPlaylist = PlaylistConverter()
print(newPlaylist.make_spotify_playlist())
