import requests

API_URL = "https://api.imagga.com/v2/tags"
API_KEY = 'acc_96b4deed7fce633'
API_SECRET = '3ca8e1e572616149abef85c9c2309a9c'


def process(images):
	response = requests.post(API_URL, auth=(API_KEY, API_SECRET), files=()
	).text
	print(response)
	return {key: '----' for key in images}
