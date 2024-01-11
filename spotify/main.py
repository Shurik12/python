import os
import logging
import time
import requests

def exception_handler(loop, context):
	print(context)

def create_logger():
	logger = logging.getLogger('Logger')
	logger.setLevel(logging.INFO) 
	handler = logging.FileHandler(f'logs/{time.strftime("%Y-%m-%d")}')
	handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
	logger.addHandler(handler)
	return logger

def main():
	logger = create_logger()
	logger.info(f'Start')

	data = {
	    'grant_type': 'client_credentials',
	    'client_id': '',
	    'client_secret': '',
	}
	response = requests.post('https://accounts.spotify.com/api/token', data=data)
	if response.status_code == 200:
		data = response.json()
		headers = {
	    	'Authorization': f'{data["token_type"]}  {data["access_token"]}',
		}

		response = requests.get('https://api.spotify.com/v1/audio-features/11dFghVXANMlKmJXsNCbNl', headers=headers)
		if response.status_code == 200:
			print (response.json())


	logger.info(f'Finish')

if __name__ == '__main__':
	main()