import os
import json
from time import time
from yandex_music.track import track
from tqdm import tqdm
import logging

class Loader:
    def __init__(self, client, logger):
        self.client = client
        self.logger = logger

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
        bitrates = []
        tracks_for_download = []
        loaded_tracks = set(os.listdir("output/tracks/"))

        for track in tqdm(tracks, "Get tracks for download"):
            artist = ", ".join(track.artists_name()).strip().replace("/", "\\")
            name = artist + " - " + track.title.replace("/", "\\") + ".mp3"
            if name not in loaded_tracks:		
                tracks_for_download.append(track)
        print ("Got %d tracks" % len(tracks_for_download))

        for i in tqdm(range(len(tracks_for_download)), "Loading..."):
            track = tracks_for_download[i]
            if track.available:
                download_info = track.get_download_info()
                bitrates = [x["bitrate_in_kbps"] for x in download_info]
                duration = '{:.2f}'.format(track.duration_ms/60000)
                artist = ", ".join(track.artists_name()).strip().replace("/", "\\")
                file_name = artist + " - " + track.title.replace("/", "\\")
                # print(len(file_name))
                if len(file_name) > 100:
                    file_name = file_name[:100]
                if track.lyrics_available:
                    supplement = track.get_supplement()
                    #  + "\n\n" + "Duration: " + str(duration)                
                    file_lyrics = 'output/lyrics/' + file_name + ".txt"
                    if supplement.lyrics and supplement.lyrics.full_lyrics:
                        with open(file_lyrics, "w") as f_w:
                            f_w.write(supplement.lyrics.full_lyrics)
                            self.logger.info(f'Lyrics: {file_lyrics}')
                    else:
                        self.logger.info(f'No lyrics: {file_lyrics}')
                else:
                    self.logger.info(f'No lyrics: {file_name}')
                file_track = 'output/tracks/' + file_name + ".mp3"
                if 320 in bitrates:
                    track.download(file_track, 'mp3', 320)
                    self.logger.info(f'{file_track}\t320')
                elif 192 in bitrates:
                    track.download(file_track, 'mp3', 192)
                    self.logger.info(f'{file_track}\t192')
                else:
                    track.download(file_track, 'mp3', 128)
                    self.logger.info(f'{file_track}\t128')
            else:
                artist = ", ".join(track.artists_name()).strip().replace("/", "\\")
                file_name = artist + " - " + track.title.replace("/", "\\")
                self.logger.warning(f'Track unavaliable: {file_name}')