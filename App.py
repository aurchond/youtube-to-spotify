import os
import json
import requests
import youtube_dl

from google_auth_oauthlib import flow
from googleapiclient import discovery, errors


from spotify_credentials import user_id, OAuth_token

# from googleapiclient.discovery import build


class PlaylistConverter:

    def __init__(self):
        self.spotify_user_id = user_id
        self.bearer_token = "Bearer {}".format(OAuth_token)
        self.youtube_client = self.get_youtube_client()

    # get the youtube client, code in this function is based on code from Youtube Data API
    def get_youtube_client(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        client_secrets_file = "client_id.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        youtube_flow = flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)

        youtube_credentials = youtube_flow.run_console()

        # from the Youtube DATA API
        youtube_client = discovery.build(
            "youtube", "v3", credentials=youtube_credentials)

        return youtube_client

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
    def get_youtube_playlist(self, playlist_name):
        # make a request to the API to get all of the channel's playlists
        playlists_request = self.youtube_client.playlists().list(
            part="snippet,contentDetails",
            mine="true"
        )
        playlists_response = playlists_request.execute()

        playlist_id = ""

        # find the desired playlist by it's name
        for item in playlists_response["items"]:
            print(item["snippet"]["title"])
            if item["snippet"]["title"] == playlist_name:
                playlist_id = item["id"]

        print(playlist_id)

        video_IDs = []

        # using the playlist ID, make another request to get all of the videos from the playlist
        if playlist_id != "":
            videos_request = self.youtube_client.playlistItems().list(
                part="contentDetails,id",
                playlistId=playlist_id
            )
            videos_response = videos_request.execute()

            for video in videos_response["items"]:
                video_IDs.append(video["id"])

            print(json.dumps(videos_response, indent=2))
            print(*video_IDs)
        else:
            print("invalid playlist id")

    # print(json.dumps(response["items"]["snippet"], indent=2))

    # for item in response["items"]:

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

        # get the URI from the first song in the list
        song_uri = songs_with_same_name[0]["uri"]

        return song_uri

    # add the list of songs into the spotify playlist
    def add_to_spotify_playlist(self):
        pass


if __name__ == "__main__":
    newPlaylist = PlaylistConverter()

    newPlaylist.get_youtube_playlist("music")

    # newPlaylist.get_spotify_song_uri("advice", "kehlani")
    # print(newPlaylist.make_spotify_playlist())
