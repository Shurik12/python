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

    # return list of play_list ()    
    def get_playlists(self):
        playlists = self.client.users_playlists_list()
        return [f'"{playlist.title}": "{playlist.playlist_id.split(":")[1]}"' for playlist in playlists]

    def download_tracks(self, tracks, lyrics_dir, tracks_dir):
        bitrates = []
        for i in tqdm(range(len(tracks)), "Loading..."):
            track = tracks[i]
            artist = ", ".join(track.artists_name()).strip().replace("/", "\\")
            file_name = artist + " - " + track.title.replace("/", "\\")
            if track.available:
                download_info = track.get_download_info()
                bitrates = [x["bitrate_in_kbps"] for x in download_info]
                # duration = '{:.2f}'.format(track.duration_ms/60000)            
                if len(file_name) > 100:
                    file_name = file_name[:100]
                if track.lyrics_available:
                    supplement = track.get_supplement()
                    #  + "\n\n" + "Duration: " + str(duration)                
                    file_lyrics = lyrics_dir + file_name + ".txt"
                    if supplement.lyrics and supplement.lyrics.full_lyrics:
                        with open(file_lyrics, "w") as f_w:
                            f_w.write(supplement.lyrics.full_lyrics)
                            self.logger.info(f'Lyrics: {file_lyrics}')
                    else:
                        self.logger.info(f'No lyrics: {file_lyrics}')
                else:
                    self.logger.info(f'No lyrics: {file_name}')
                file_track = tracks_dir + file_name + ".mp3"
                # check bitrates
                if 320 in bitrates:
                    track.download(file_track, 'mp3', 320)
                    self.logger.info(f'{file_track}\t320')
                elif 192 in bitrates:
                    track.download(file_track, 'mp3', 192)
                    self.logger.info(f'{file_track}\t192')
                elif 128 in bitrates:
                    track.download(file_track, 'mp3', 128)
                    self.logger.info(f'{file_track}\t128')
                else:
                    self.logger.info(f'{file_track}\tnot 320 129 128')
            else: 
                self.logger.warning(f'Track unavaliable: {file_name}')

    def download_playlist(self, playlist):
        print (playlist.title)
        playlist_dir = f'output/playlists/{playlist.title}/'
        tracks_dir = f'output/playlists/{playlist.title}/tracks/'
        lyrics_dir = f'output/playlists/{playlist.title}/lyrics/'

        if playlist.title not in set(os.listdir("output/playlists")): 
            os.mkdir(playlist_dir)
            os.mkdir(tracks_dir)
            os.mkdir(lyrics_dir)
        tracks_ids = [track["id"] for track in playlist.fetch_tracks()]
        tracks = self.client.tracks(tracks_ids)
        tracks_for_download = []
        loaded_tracks = set(os.listdir(tracks_dir))

        for track in tqdm(tracks, "Get tracks for download"):
            artist = ", ".join(track.artists_name()).strip().replace("/", "\\")
            name = artist + " - " + track.title.replace("/", "\\")
            name = len(name) > 100 and name[:100] + ".mp3" or name + ".mp3" 
            if name not in loaded_tracks:		
                tracks_for_download.append(track)
        print ("Got %d tracks" % len(tracks_for_download))
        self.download_tracks(tracks_for_download, lyrics_dir, tracks_dir)
        return 0

    @decorator_time_execution
    def download_playlists(self):
        playlists = self.client.users_playlists_list()
        if "playlists" not in set(os.listdir("output/")): 
            os.mkdir('output/playlists')
        return [self.download_playlist(playlist) for playlist in playlists]

    @decorator_time_execution
    def download_like_tracks(self):
        tracks_dir = "output/tracks/"
        lyrics_dir = "output/lyrics/"
        tracks_ids = list(map(lambda track: track["id"], self.client.users_likes_tracks().tracks))
        tracks = self.client.tracks(tracks_ids)
        tracks_for_download = []
        loaded_tracks = set(os.listdir(tracks_dir))

        for track in tqdm(tracks, "Get tracks for download"):
            artist = ", ".join(track.artists_name()).strip().replace("/", "\\")
            name = artist + " - " + track.title.replace("/", "\\") + ".mp3"
            if name not in loaded_tracks:		
                tracks_for_download.append(track)
        print ("Got %d tracks" % len(tracks_for_download))
        self.download_tracks(tracks_for_download, lyrics_dir, tracks_dir)