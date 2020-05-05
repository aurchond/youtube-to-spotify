import os
import json
import requests
import youtube_dl

from google_auth_oauthlib import flow
from googleapiclient import discovery, errors

from spotify_credentials import user_id, OAuth_token


class PlaylistConverter:

    def __init__(self, playlist_name):
        self.playlist_name = playlist_name
        self.youtube_client = self.get_youtube_client()

        self.spotify_user_id = user_id
        self.bearer_token = "Bearer {}".format(OAuth_token)
        # the following is a dictionary with a singular key being set to an array of URIs
        # since this is the format that the Spotify API uses for playlist modification requests
        self.spotify_URIs = {"uris": []}

    # get the youtube client
    # code in this function is based on code from Youtube Data API
    def get_youtube_client(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        client_secrets_file = "client_id.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        youtube_flow = flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)

        youtube_credentials = youtube_flow.run_console()

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
    def get_songs_from_youtube(self):
        playlist_id = ""
        all_song_URIs = []

        # make a request to the API to get all of the channel's playlists
        playlists_request = self.youtube_client.playlists().list(
            part="snippet,contentDetails",
            mine="true"
        )
        playlists_response = playlists_request.execute()

        # find the desired playlist by it's name
        for item in playlists_response["items"]:
            if item["snippet"]["title"] == self.playlist_name:
                playlist_id = item["id"]

        # using the playlist ID, make another request to get all of the videos from the playlist
        if playlist_id != "":
            videos_request = self.youtube_client.playlistItems().list(
                part="contentDetails,id",
                playlistId=playlist_id
            )
            videos_response = videos_request.execute()

            for video in videos_response["items"]:
                # get the youtube URL for each video in the playlist
                youtube_url = "https://www.youtube.com/watch?v={}".format(
                    video["contentDetails"]["videoId"])

                # get the song name and artist
                song = youtube_dl.YoutubeDL({}).extract_info(
                    youtube_url, download=False)
                song_name = song["track"]
                song_artist = song["artist"]

                # add song URIs to array
                if song_name is not None and song_artist is not None:
                    song_uri = self.get_spotify_song_uri(
                        song_name, song_artist)

                    if song_uri != "":
                        all_song_URIs.append(song_uri)
        else:
            print("invalid playlist id")

        return all_song_URIs

    # get the corresponding spotify_uri for each song in the youtube playlist
    def get_spotify_song_uri(self, song, artist):
        # format the song and artists strings for the query
        song.replace(" ", "+")
        artist.replace(" ", "+")
        query = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track".format(
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

        song_uri = ""
        # check that the list has items before using the first song in the list by default
        if len(songs_with_same_name) > 0:
            song_uri = songs_with_same_name[0]["uri"]

        return song_uri

    # convert songs from the Youtube playlist into songs for the Spotify playlist
    def convert_to_spotify_playlist(self):

        # make a new playlist and get it's id for the query
        playlist_id = self.make_spotify_playlist()
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(
            playlist_id)

        # create the two required header fields using the spotify OAuth token
        header_fields = {
            "Content-Type": "application/json",
            "Authorization": self.bearer_token
        }

        # grab videos from the youtube playlist
        self.spotify_URIs["uris"] = self.get_songs_from_youtube()

        # format the URIs to make the request
        request_body = json.dumps(self.spotify_URIs, indent=2)

        response = requests.post(
            query,
            data=request_body,
            headers=header_fields
        )
        response_json = response.json()
        print(response_json)

        # check for valid response status
        if response.status_code != 200:
            print("invalid response")

        return response_json


if __name__ == "__main__":
    new_playlist = PlaylistConverter("music")
    new_playlist.convert_to_spotify_playlist()
