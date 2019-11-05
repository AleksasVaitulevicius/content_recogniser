import re
from concurrent.futures.thread import ThreadPoolExecutor

from . import image_processor as img_vid_prc, recording_processor as rec_prc

CONTENT_TYPES = {
	'image': img_vid_prc.process,
	'audio': rec_prc.process,
}


def process_in_parallel(objects):
	with ThreadPoolExecutor(len(CONTENT_TYPES.items())) as executor:
		future = executor.map(lambda key: CONTENT_TYPES[key](objects[key]), objects.keys())
	return future


def get_content_type(content):
	content_type = re.search(r'(.*)?/', content.content_type).group(1)
	return content_type


def process(contents):
	objects = {content_type: {} for content_type in list(CONTENT_TYPES.keys())}
	for key in contents:
		content_type = get_content_type(contents[key])
		if content_type in list(CONTENT_TYPES.keys()):
			objects[content_type][key] = contents[key]
	results = process_in_parallel(objects)
	results = {key: description for result in results for key, description in result.items()}
	return results
