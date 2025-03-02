import logging
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import pandas as pd

from utils import CLIENT_ID
from utils import CLIENT_SECRET
from utils import REDIRECT_URI
from utils import PLAYLIST_ID


class ExtractSpotifyPlaylist:
    def __init__(
        self,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="playlist-read-collaborative",
    ):
        self.scope = scope
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=self.scope,
            )
        )

    def _get_tracks_id_and_name(self, playlist_id=PLAYLIST_ID) -> pd.DataFrame:
        """
        Get a dataframe of track IDs and track name.
        """
        result_playlist_tracks = self.sp.playlist_tracks(
            playlist_id, fields="items(track(id, name))"
        )
        list_tracks = []
        for track in result_playlist_tracks["items"]:
            info = {"id": track["track"]["id"], "name": track["track"]["name"]}
            list_tracks.append(info)
        return pd.DataFrame(data=list_tracks)

    def _get_list_of_track_id(self, tracks_df) -> list:
        """
        Get a unique list of track IDs.
        """
        if len(tracks_df) == tracks_df["id"].nunique():
            logging.warning(
                "There are track duplications in playlist. Review and remove duplications in app."
            )
        return list(tracks_df["id"].unique())

    def _get_track_release_date(self, list_tracks: list) -> pd.DataFrame:
        """
        Get track release date. Since a track is tied to an album, and only album has release date,
        we proxy the album's release date as track's release date.
        """
        result_tracks = self.sp.tracks(list_tracks)
        tracks = []
        for track in result_tracks["tracks"]:
            info = {
                "id": track["id"],
                "album_release_date": track["album"]["release_date"],
            }
            tracks.append(info)
        return pd.DataFrame(data=tracks)

    def _get_audio_features(self, list_tracks: list) -> pd.DataFrame:
        """
        DEPRECATED AFTER SPOTIFY DEPRECATING THE END POINT IN NOVEMBER 2024
        https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api

        Get audio features from a json resulted from API call for tracks. Features include:
        - Duration in minutes
        - Dancability: how suitable a track is for dancing
        - Tempo: overall estimated tempo of a track in beats per minute (BPM)
        - Energy: represents a perceptual measure of intensity and activity
        - Musical positiveness
        More info for these features in Spotify API's documentation: https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features
        """
        result_tracks_audio_features = self.sp.audio_features(list_tracks)
        track_audio_features = []
        for track in result_tracks_audio_features:
            audio_features_info = {
                "id": track["id"],
                "duration_mins": round(track["duration_ms"] / 60000, 2),
                "danceability": track["danceability"],
                "tempo": track["tempo"],
                "energy": track["energy"],
                "musical_positiveness": track["valence"],
            }
            track_audio_features.append(audio_features_info)
        return pd.DataFrame(track_audio_features)

    def extract_track_info_and_audio_features(self) -> pd.DataFrame:
        tracks_df = self._get_tracks_id_and_name()
        list_tracks = self._get_list_of_track_id(tracks_df)

        tracks_release_date_df = self._get_track_release_date(list_tracks)

        tracks_with_features_df = tracks_df.merge(
            tracks_release_date_df, how="left", on="id"
        )
        tracks_with_features_df["album_release_date"] = pd.to_datetime(tracks_with_features_df["album_release_date"])
        return tracks_with_features_df
