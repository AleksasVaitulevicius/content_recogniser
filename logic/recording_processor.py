from concurrent.futures.thread import ThreadPoolExecutor
from acrcloud import ACRcloud

SLAVES = 5
re = ACRcloud
re.host = 'identify-eu-west-1.acrcloud.com'
re.key = '9e9a124e292b7d0161e4ea997fff8f6b'
re.secret = 'fLtsJPamnjz6nlCiTO7aaXivZR4VYxNSgFOu4V8e'


def slave(recs):
	print(recs[1])
	return {
		recs[0]: re.recognizer(recs[1], recs[1])
	}


def process(recordings):
	with ThreadPoolExecutor(SLAVES) as executor:
		result = executor.map(slave, recordings.items())
	return {key: description for result in result for key, description in result.items()}
