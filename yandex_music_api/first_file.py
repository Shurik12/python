import os
from yandex_music import Client
# from yandex_music import ClientAsync

def main():


	token = os.environ["YANDEX_MUSIC_TOKEN"]
	client = Client(token)
	client.init()

if __name__ == '__main__':
	main()