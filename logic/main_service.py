from django.core.files.uploadedfile import InMemoryUploadedFile
from . import file_processor, text_processor


def process(data_list):
	print(data_list)
	for key in data_list:
		if isinstance(data_list[key], InMemoryUploadedFile):
			print(data_list[key].content_type)
