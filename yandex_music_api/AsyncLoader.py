import os
import json
from time import time
from yandex_music.track import track
from tqdm.asyncio import tqdm
import asyncio
import logging

class Loader:
    def __init__(self, client, logger):
        self.client = client
        self.logger = logger

    def decorator_time_execution(function):
        async def time_execution(*args, **kwargs):
            start_execution = time()
            await function(*args, **kwargs)
            end_execution = time()
            execution_time = 'Execution time {:.2f} seconds'.format(end_execution - start_execution)
            print (execution_time)
        return time_execution

    def get_playlists(self):
        playlists = self.client.users_playlists_list()
        for play_list in play_lists:
            print(play_list.title, play_list.track_count)
            traks = play_list.tracks

    async def make_coro(self, future):
        try:
            return await future
        except asyncio.CancelledError:
            return await future

    @decorator_time_execution
    async def download_like_tracks(self):

        tracks = await self.client.users_likes_tracks()
        tracks_ids = list(map(lambda track: track["id"], tracks.tracks))
        tracks = await self.client.tracks(tracks_ids)
        tracks_for_download = []
        loaded_tracks = set(os.listdir("output/tracks/"))

        for track in tqdm(tracks, "Get tracks for download"):
            artist = ", ".join(track.artists_name()).strip().replace("/", "\\")
            name = artist + " - " + track.title.replace("/", "\\") + ".mp3"
            if name not in loaded_tracks:		
                tracks_for_download.append(track)
        print ("Got %d tracks" % len(tracks_for_download))

        loop = asyncio.get_running_loop() # get current event loop
        tasks = [] # create download tasks for await

        # in this function we create tasks in event loop for downloading songs
        async for i in tqdm(range(len(tracks_for_download)), "Loading..."):
            track = tracks_for_download[i]
            duration = '{:.2f}'.format(track.duration_ms/60000)
            artist = ", ".join(track.artists_name()).strip().replace("/", "\\")
            if track.lyrics_available:
                supplement = await track.get_supplement()
                file_lyrics = 'output/lyrics/' + artist + " - " + track.title.replace("/", "\\") + ".txt"
                if supplement.lyrics and supplement.lyrics.full_lyrics:
                    with open(file_lyrics, "w") as f_w:
                        f_w.write(supplement.lyrics.full_lyrics)
            file_track = 'output/tracks/' + artist + " - " + track.title.replace("/", "\\") + ".mp3"
            tasks.append(loop.create_task(self.wrapper(track.download_async, file_track, 'mp3', 192)))
        
        result = await asyncio.gather(*tasks, return_exceptions=True)
        self.logger.info(f'Result: {result}')

    async def wrapper(self, func, file_name, extension, bitrate):
        try:
            await func(file_name, extension, bitrate)
            return 1
        except Exception as e:
            self.logger.warning(f'{file_name}')
            return -1