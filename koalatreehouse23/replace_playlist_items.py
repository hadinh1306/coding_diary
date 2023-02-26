import pandas as pd

from utils import PLAYLIST_ID
from extract import ExtractSpotifyPlaylist

if __name__ == "__main__":
    sp_extractor = ExtractSpotifyPlaylist(scope="playlist-read-collaborative")
    # TODO create a separate playlist that will be used as final dance floor
    sp_modifier = ExtractSpotifyPlaylist(scope="playlist-modify-private")

    playlist_df = pd.read_csv("output/tracks_with_features.csv")
    playlist_df["album_release_date"] = pd.to_datetime(
        playlist_df["album_release_date"]
    )

    # LOGIC:
    # Slow songs from the start, gradually go up to fast song
    # Date range ascendingly
    cols_to_round = playlist_df.select_dtypes(include=["number"]).columns.to_list()
    for col in cols_to_round:
        playlist_df[col] = round(playlist_df[col], 2)
    playlist_df = playlist_df.sort_values(
        by=["energy", "tempo", "danceability", "album_release_date"],
    )

    reordered_track_ids = playlist_df["id"].to_list()
    sp_extractor.sp.playlist_replace_items(PLAYLIST_ID, reordered_track_ids)
