import os
from yandex_music import Client
from Loader import Loader

# from yandex_music import ClientAsync

def main():

	client = Client(os.environ["YANDEX_MUSIC_TOKEN"]).init()
	
	alex = Loader(client)

	alex.download_like_tracks()

if __name__ == '__main__':
	main()