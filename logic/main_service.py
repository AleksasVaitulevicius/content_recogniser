from django.core.files.uploadedfile import InMemoryUploadedFile
from . import file_processor, text_processor


def process(data_list):
	files = {}
	texts = {}
	for key in data_list:
		if isinstance(data_list[key], InMemoryUploadedFile):
			files[key] = data_list[key]
		else:
			texts[key] = data_list[key]
	texts = text_processor.process(texts)
	files = file_processor.process(files)
	return dict(files, **texts)
