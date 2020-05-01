import json
import requests

from spotify_credentials import user_id, OAuth_token


class PlaylistConverter:

    def __init__(self):
        self.spotify_user_id = user_id
        # self.spotify_OAuth_token = OAuth_token
        self.bearer_token = "Bearer {}".format(OAuth_token)

    # get the youtube client
    def youtube_login(self):
        pass

    # create a new spotify playlist
    def make_spotify_playlist(self):
        # format the query using guidelines from the API documentation
        query = "https://api.spotify.com/v1/users/{}/playlists".format(
            self.spotify_user_id)

        # create the request body and convert it to JSON
        request_body = json.dumps({
            "name": "Youtube Playlist",
            "description": "This playlist was created from your corresponding Youtube playlist",
            "public": True,
            "collaborative": False
        }, indent=2)

        # create the two required header fields using the spotify OAuth token
        header_fields = {
            "Content-Type": "application/json",
            "Authorization": self.bearer_token
        }

        # make a post request using the given parameters (to the Spotify API) and get the response
        response = requests.post(
            query,
            data=request_body,
            headers=header_fields
        )

        # get the json content from the response
        response_json = response.json()

        # return the playlist id from the response
        return response_json["id"]

    # get the existing playlist from youtube
    def get_youtube_playlist(self):
        pass

    # get the corresponding spotify_uri for each song in the youtube playlist
    def get_spotify_song_uri(self, song, artist):
        query = "https://api.spotify.com/v1/search?q={}+{}&type=track".format(
            song, artist)

        header_field = {
            "Authorization": self.bearer_token
        }

        # make a get request
        response = requests.get(
            query,
            headers=header_field
        )
        response_json = response.json()

        # we have to go two levels within the dictionary to get all songs with the same name and artist
        songs_with_same_name = response_json["tracks"]["items"]

        # print(json.dumps(song_uri, indent=2))

        # get the URI from the first song in the list
        song_uri = songs_with_same_name[0]["uri"]

        return song_uri

    # add the list of songs into the spotify playlist

    def add_to_spotify_playlist(self):
        pass


newPlaylist = PlaylistConverter()
newPlaylist.get_spotify_song_uri("advice", "kehlani")
# print(newPlaylist.make_spotify_playlist())
