import sqlite3
from extract import ExtractSpotifyPlaylist

if __name__ == "__main__":
    sp_extractor = ExtractSpotifyPlaylist(scope="playlist-read-collaborative")
    tracks_df = sp_extractor.extract_track_info_and_audio_features()

    connection = sqlite3.connect("spotify_db/spotify.db")

    with open('spotify_db/schema/create_playlist_schema.sql', 'r') as file:
        create_table_query = file.read()
    
    connection.execute(create_table_query)

    tracks_df.to_sql('playlist_tracks', connection, if_exists='replace', index=False)

    connection.commit()
    connection.close()