from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep
from config import Imagga
import requests

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
			.post(Imagga.UPLOAD_URL, auth=(Imagga.API_KEY, Imagga.API_SECRET), files={'image': image})\
			.json()['result']['upload_id']
	except Exception:
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
		try:
			response = requests\
				.get(Imagga.TICKET_URL + ticket, auth=(Imagga.API_KEY, Imagga.API_SECRET))\
				.json()
		except Exception:
			return "error occurred"
	return response['result']['ticket_result']['final_result']


def submit_batch(img_ids):
	params = [prepare_batch_param(img_id) for img_id in img_ids]
	body = {endpoint: params for endpoint in BATCH_TEMPLATE}
	try:
		response = requests\
			.post(Imagga.BATCH_URL, auth=(Imagga.API_KEY, Imagga.API_SECRET), json=body)
		ticket = response.json()['result']['ticket_id']
		return get_ticket_result(ticket)
	except Exception:
		return "error occurred"


def extract_data(keys, results):
	extracted = {key: BATCH_TEMPLATE.copy() for key in keys}
	for result_key in BATCH_TEMPLATE.keys():
		if isinstance(results, str):
			for key in keys:
				extracted[key][result_key] = results
		for key, result in zip(keys, results[result_key]):
			if 'result' in result.keys() and 'ticket_id' in result['result'].keys():
				result = get_ticket_result(result['result']['ticket_id'])
			extracted[key][result_key] = result
	return extracted


def process(images):
	keys = images.keys()
	if len(keys) == 0:
		return {}
	contents = images.values()
	img_ids = upload_in_parallel(contents)
	img_ids = [img_id for img_id in img_ids if img_id is not None]
	response = submit_batch(img_ids)
	return extract_data(keys, response)
