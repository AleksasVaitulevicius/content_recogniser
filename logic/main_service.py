from concurrent.futures.thread import ThreadPoolExecutor

from django.core.files.uploadedfile import InMemoryUploadedFile
from . import file_processor, text_processor


def process_in_parallel(functions, contents):
	with ThreadPoolExecutor(2) as executor:
		future = executor.map(lambda func, params: func(params), functions, contents)
	return future


def process(data_list):
	files = {}
	texts = {}
	for key in data_list:
		if isinstance(data_list[key], InMemoryUploadedFile):
			if 'text' in data_list[key].content_type:
				texts[key] = data_list[key].read().decode('utf-8')
			files[key] = data_list[key]
		else:
			texts[key] = data_list[key]

	results = process_in_parallel([text_processor.process, file_processor.process], [texts, files])
	return {key: description for result in results for key, description in result.items()}
