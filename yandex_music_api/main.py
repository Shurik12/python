import os
import logging
from yandex_music import Client
from yandex_music import ClientAsync
from Loader import Loader
from AsyncLoader import Loader as LoaderAsync
import asyncio
import time
from functions import *

# from yandex_music import ClientAsync

def exception_handler(loop, context):
	print(context)

def create_logger():
	logger = logging.getLogger('Logger')
	logger.setLevel(logging.INFO) 
	handler = logging.FileHandler(f'logs/{time.strftime("%Y-%m-%d")}')
	handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
	logger.addHandler(handler)
	return logger

async def main_async():

	logger = create_logger()
	logger.info(f'New launch asynchron')
	loop = asyncio.get_running_loop()
	client_async = await ClientAsync(os.environ["YANDEX_MUSIC_TOKEN"]).init()
	alex = LoaderAsync(client_async, logger)
	await alex.download_like_tracks()
	logger.info(f'Launch finished asynchron')

def main():

	logger = create_logger()
	logger.info(f'New launch synchron')
	client = Client(os.environ["YANDEX_MUSIC_TOKEN"]).init()
	tracks_without_playlist(client, logger)
	# alex = Loader(client, logger)
	# alex.download_playlists()

	logger.info(f'Launch finished synchron')

if __name__ == '__main__':
	main()
	# asyncio.run(main_async())