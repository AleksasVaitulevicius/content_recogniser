from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep
from config import Imagga
import requests
import json

N_SLAVES = 5

BATCH_TEMPLATE = {
	'/tags': [],
	'/text': [],
	'/colors': [],
}


def send_request(func, retries, url, json_data, extract_by_keys, return_on_err, **kwargs):
	for try_no in range(1, retries + 1):
		try:
			if func == requests.get:
				result = requests.get(url=url, **kwargs)
			else:
				result = func(url, None, json_data, **kwargs)
			if not result:
				print(result.content)
				raise Exception(result.reason + ': ' + str(result.status_code))
			result = result.json()['result']
			for key in extract_by_keys:
				result = result[key]
			return result
		except Exception as e:
			print('exception:', e)
			continue
	return return_on_err


def upload_image(image):
	return send_request(
		requests.post, 1, Imagga.UPLOAD_URL, None, ['upload_id'], None,
		auth=(Imagga.API_KEY, Imagga.API_SECRET), files={'image': image}
	)


def upload_in_parallel(images):
	with ThreadPoolExecutor(N_SLAVES) as executor:
		future = executor.map(upload_image, images)
	if len(list(future)) == 0:
		raise Exception('Error occurred while uploading image')
	return future


def prepare_batch_param(img_id):
	return {
		'params': {
			'image_upload_id': img_id
		}
	}


def get_ticket_result(ticket):
	response = {'is_final': False}
	while isinstance(response, dict) and not response['is_final']:
		sleep(5)
		response = send_request(
			requests.get, 1, Imagga.TICKET_URL + ticket, None, [], 'error occurred while getting ticket',
			auth=(Imagga.API_KEY, Imagga.API_SECRET)
		)
	if isinstance(response, str):
		return response
	return response['ticket_result']['final_result']


def submit_batch(img_ids):
	params = [prepare_batch_param(img_id) for img_id in img_ids]
	body = {endpoint: params for endpoint in BATCH_TEMPLATE}
	ticket = send_request(
		requests.post, 1, Imagga.BATCH_URL, body, ['ticket_id'], 'error occurred while submitting batch',
		auth=(Imagga.API_KEY, Imagga.API_SECRET)
	)
	if ticket == 'error occurred while submitting batch':
		raise Exception('error occurred while submitting batch')
	return get_ticket_result(ticket)


def extract_data(keys, results, unloaded_img_ids):
	extracted = {key: BATCH_TEMPLATE.copy() for key in keys}
	for result_key in BATCH_TEMPLATE.keys():
		for key, result in zip(keys, results[result_key]):
			if key in unloaded_img_ids:
				extracted[key][result_key] = 'error occurred while uploading image'
				continue
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
	# with open('img_ids.json', 'r') as img_ids_file:
	# 	img_ids = json.load(img_ids_file)
	unloaded_img_ids = [img_id for key, img_id in zip(keys, img_ids) if img_id is None]
	img_ids = [img_id for img_id in img_ids if img_id is not None]
	try:
		response = submit_batch(img_ids)
	except Exception as e:
		return {key: str(e) for key in keys}
	return extract_data(keys, response, unloaded_img_ids)
