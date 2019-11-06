import re
from concurrent.futures.thread import ThreadPoolExecutor

from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from . import file_processor, text_processor

TEXT_EXTENSIONS = ['docx', 'txt']


def is_text(content):
	return 'text' in content.content_type or re.search(r'\.(.*)?', content.name).group(1) in TEXT_EXTENSIONS


def process_in_parallel(functions, contents):
	with ThreadPoolExecutor(2) as executor:
		future = executor.map(lambda func, params: func(params), functions, contents)
	return future


def process(data_list):
	files = {}
	texts = {}
	for key in data_list:
		if isinstance(data_list[key], TemporaryUploadedFile) or isinstance(data_list[key], InMemoryUploadedFile):
			if is_text(data_list[key]):
				texts[key] = data_list[key].read().decode('utf-8')
			files[key] = data_list[key]
		else:
			texts[key] = data_list[key]

	results = process_in_parallel([text_processor.process, file_processor.process], [texts, files])
	return {key: description for result in results for key, description in result.items()}
