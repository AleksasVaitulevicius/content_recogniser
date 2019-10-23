from json import JSONDecodeError

import requests

API_URL = "https://api.imagga.com/v2/"
API_KEY = 'acc_96b4deed7fce633'
API_SECRET = '3ca8e1e572616149abef85c9c2309a9c'
UPLOAD_URL = API_URL + 'uploads'
BATCH_URL = API_URL + 'batches'
TICKET_URL = API_URL + 'tickets/'

BATCH_TEMPLATE = {
	'/tags': [],
	'/text': [],
	'/colors': [],
}
BATCH_PARAMS_TEMPLATE = {
	'params': {
		'image_upload_id': '',
	}
}


def upload_image(image):
	try:
		return requests\
			.post(UPLOAD_URL, auth=(API_KEY, API_SECRET), files={'image': image})\
			.json()['result']['upload_id']
	except (KeyError, JSONDecodeError):
		return


def prepare_batch_param(img_id):
	param = BATCH_PARAMS_TEMPLATE.copy()
	param['params'] = param['params'].copy()
	param['params']['image_upload_id'] = img_id
	return param


def submit_batch(img_ids):
	params = [prepare_batch_param(img_id) for img_id in img_ids]
	body = {endpoint: params for endpoint in BATCH_TEMPLATE}
	try:
		print(body)
		response = requests\
			.post(BATCH_URL, auth=(API_KEY, API_SECRET), json=body)
		print('response:', response)
		ticket = response.json()['result']['ticket_id']

		print('ticket:', ticket)

		response = requests\
			.get(TICKET_URL + ticket, auth=(API_KEY, API_SECRET))
		print('response:', response)
		return response.json()['result']['ticket_result']['final_result']
	except (KeyError, JSONDecodeError):
		print('caught error :/')
		return


def process(images):
	img_ids = [upload_image(images[image]) for image in images]
	img_ids = [img_id for img_id in img_ids if img_id is not None]
	response = submit_batch(img_ids)
	print(response)
	return response
