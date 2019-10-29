from concurrent.futures.thread import ThreadPoolExecutor
from json import JSONDecodeError
from time import sleep

import requests

API_URL = "https://api.imagga.com/v2/"
API_KEY = 'acc_96b4deed7fce633'
API_SECRET = '3ca8e1e572616149abef85c9c2309a9c'
UPLOAD_URL = API_URL + 'uploads'
BATCH_URL = API_URL + 'batches'
TICKET_URL = API_URL + 'tickets/'
N_SLAVES = 5

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


def upload_in_parallel(images):
	with ThreadPoolExecutor(N_SLAVES) as executor:
		future = executor.map(upload_image, images)
	return future


def prepare_batch_param(img_id):
	param = BATCH_PARAMS_TEMPLATE.copy()
	param['params'] = param['params'].copy()
	param['params']['image_upload_id'] = img_id
	return param


def get_ticket_result(ticket):
	response = {'result': {'is_final': False}}
	while not response['result']['is_final']:
		sleep(5)
		response = requests\
			.get(TICKET_URL + ticket, auth=(API_KEY, API_SECRET))\
			.json()
	return response['result']['ticket_result']['final_result']


def submit_batch(img_ids):
	params = [prepare_batch_param(img_id) for img_id in img_ids]
	body = {endpoint: params for endpoint in BATCH_TEMPLATE}
	try:
		response = requests\
			.post(BATCH_URL, auth=(API_KEY, API_SECRET), json=body)
		ticket = response.json()['result']['ticket_id']
		return get_ticket_result(ticket)
	except (KeyError, JSONDecodeError):
		return


def extract_data(keys, results):
	extracted = {key: BATCH_TEMPLATE.copy() for key in keys}
	for result_key in BATCH_TEMPLATE.keys():
		for key, result in zip(keys, results[result_key]):
			if 'ticket_id' in result['result'].keys():
				result = get_ticket_result(result['result']['ticket_id'])
			extracted[key][result_key] = result
	return extracted


def process(images):
	# keys = images.keys()
	# if len(keys) == 0:
	# 	return {}
	# contents = images.values()
	# img_ids = upload_in_parallel(contents)
	# img_ids = [img_id for img_id in img_ids if img_id is not None]
	# response = submit_batch(img_ids)
	# return extract_data(keys, response)
	return {key: 'image' for key in images}
