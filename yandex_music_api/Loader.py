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
        self.output = "/home/alex/yandex_disk/Music"

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
                    if supplement.lyrics and supplement.lyrics.full_lyrics:
                        with open(lyrics_dir+ "/" + file_name + ".txt", "w") as file_lyrics:
                            file_lyrics.write(supplement.lyrics.full_lyrics)
                            self.logger.info(f'Lyrics: {file_lyrics}')
                    else:
                        self.logger.warning(f'No lyrics: {lyrics_dir}/{file_name}.txt')
                else:
                    self.logger.info(f'No lyrics: {file_name}')
                file_track = tracks_dir + "/" + file_name + ".mp3"
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
        self.logger.info(f'Playlist to download: {playlist.title}')
        playlist_dir = f'{self.output}/{playlist.title}'
        tracks_dir = f'{playlist_dir}/tracks'
        lyrics_dir = f'{playlist_dir}/lyrics'

        # Create playlist directory if not exists
        if playlist.title not in set(os.listdir(self.output)): 
            os.mkdir(playlist_dir)
            os.mkdir(tracks_dir)
            os.mkdir(lyrics_dir)

        # Get already loaded tracks (already on yandex disk and file system)
        tracks_ids = [track["id"] for track in playlist.fetch_tracks()]
        if (len(tracks_ids) == 0):
            self.logger.warning(f'No tracks in playlist: {playlist.title}')
            return 0

        tracks = self.client.tracks(tracks_ids)
        self.logger.info(f'All tracks in playlist {playlist.title}: {len(tracks)}')
        loaded_tracks = set(os.listdir(tracks_dir))
        self.logger.info(f'Already loaded tracks in playlist {playlist.title}: {len(loaded_tracks)}')

        # Download new tracks
        tracks_for_download = []
        for track in tqdm(tracks, "Get tracks for download"):
            artist = ", ".join(track.artists_name()).strip().replace("/", "\\")
            name = artist + " - " + track.title.replace("/", "\\")
            name = len(name) > 100 and name[:100] + ".mp3" or name + ".mp3" 
            if name not in loaded_tracks:		
                tracks_for_download.append(track)
        self.logger.info(f'Tracks for download: {len(tracks_for_download)}')
        self.download_tracks(tracks_for_download, lyrics_dir, tracks_dir)

        return 0

    @decorator_time_execution
    def download_playlists(self):
        playlists = self.client.users_playlists_list()
        return [self.download_playlist(playlist) for playlist in playlists]

    @decorator_time_execution
    def download_like_tracks(self):

        playlist_dir = f'{self.output}/Like'
        tracks_dir = f'{playlist_dir}/tracks'
        lyrics_dir = f'{playlist_dir}/lyrics'

        # Create Like playlist directory if not exists
        if playlist.title not in set(os.listdir(self.output)): 
            os.mkdir(playlist_dir)
            os.mkdir(tracks_dir)
            os.mkdir(lyrics_dir)

        # Get already loaded tracks (already on yandex disk and file system)
        tracks_ids = list(map(lambda track: track["id"], self.client.users_likes_tracks().tracks))
        tracks = self.client.tracks(tracks_ids)
        self.logger.info(f'All tracks in playlist {playlist.title}: {len(tracks)}')
        loaded_tracks = set(os.listdir(tracks_dir))
        self.logger.info(f'Already loaded tracks in playlist {playlist.title}: {len(loaded_tracks)}')

        # Download new tracks
        tracks_for_download = []
        for track in tqdm(tracks, "Get tracks for download"):
            artist = ", ".join(track.artists_name()).strip().replace("/", "\\")
            name = artist + " - " + track.title.replace("/", "\\") + ".mp3"
            if name not in loaded_tracks:		
                tracks_for_download.append(track)
        self.logger.info(f'Tracks for download: {len(tracks_for_download)}')
        self.download_tracks(tracks_for_download, lyrics_dir, tracks_dir)