import os
import json
from time import time
from yandex_music import Client
from yandex_music.track import track
from tqdm import tqdm

class Loader:
    def __init__(self, client):
        self.client = client

    def decorator_time_execution(function):
        def time_execution(*args, **kwargs):
            start_execution = time()
            function(*args, **kwargs)
            end_execution = time()
            execution_time = 'Execution time {:.2f} seconds'.format(end_execution - start_execution)
            print(execution_time)
        return time_execution

    def get_playlists(self):
        playlists = self.client.users_playlists_list()
        for play_list in play_lists:
            print(play_list.title, play_list.track_count)
            traks = play_list.tracks

    @decorator_time_execution
    def download_like_tracks(self):

        tracks_ids = list(map(lambda track: track["id"], self.client.users_likes_tracks().tracks))
        tracks = self.client.tracks(tracks_ids)
        tracks_for_download = []
        loaded_tracks = set(os.listdir("output/tracks/"))

        for track in tqdm(tracks, "Get tracks for download"):
            artist = ", ".join(track.artists_name()).strip()
            name = artist + " - " + track.title + ".mp3"
            if name not in loaded_tracks:		
                tracks_for_download.append(track)
        print ("Got %d tracks" % len(tracks_for_download))

        for i in tqdm(range(10), "Loading..."):
            track = tracks_for_download[i]
            duration = '{:.2f}'.format(track.duration_ms/60000)
            artist = ", ".join(track.artists_name()).strip()
            if track.lyrics_available:
                supplement = track.get_supplement()
                #  + "\n\n" + "Duration: " + str(duration)
                file_lyrics = 'output/lyrics/' + artist + " - " + track.title + ".txt"
                with open(file_lyrics, "w") as f_w:
                    f_w.write(supplement.lyrics.full_lyrics)
            file_track = 'output/tracks/' + artist + " - " + track.title + ".mp3"
            track.download(file_track, 'mp3', 192)
