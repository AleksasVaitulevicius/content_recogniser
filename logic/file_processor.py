import re
from . import image_video_processor as img_vid_prc, recording_processor as rec_prc

CONTENT_TYPES = {
	'image': img_vid_prc.process,
	'audio': rec_prc.process,
}


def get_content_type(content):
	content_type = re.search(r'(.*)?/', content.content_type).group(1)
	if content_type == 'video':
		return 'image'
	return content_type


def process(contents):
	classes = {content_type: {} for content_type in list(CONTENT_TYPES.keys())}
	for key in contents:
		content_type = get_content_type(contents[key])
		if content_type in list(CONTENT_TYPES.keys()):
			classes[content_type][key] = contents[key]
	results = [CONTENT_TYPES[key](classes[key]) for key in list(CONTENT_TYPES.keys())]
	results = {key: description for result in results for key, description in result.items()}
	return results
