from concurrent.futures.thread import ThreadPoolExecutor
from acrcloud.recognizer import ACRCloudRecognizer
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

SLAVES = 5
re = ACRCloudRecognizer({
	'host': 'identify-eu-west-1.acrcloud.com',
	'access_key': '9e9a124e292b7d0161e4ea997fff8f6b',
	'access_secret': 'fLtsJPamnjz6nlCiTO7aaXivZR4VYxNSgFOu4V8e',
	'timeout': 10  # seconds
})
ibm_auth = IAMAuthenticator('s4Od7pNSAaRJbDVJnck1P3R3OonJzdhK11RGYuDOYZPl')
stt = SpeechToTextV1(authenticator=ibm_auth)
stt.set_service_url('https://gateway-lon.watsonplatform.net/speech-to-text/api')


def slave(recs):
	return {
		recs[0]: {
			'music': json.loads(re.recognize_by_filebuffer(recs[1].read(), 0, 600)),
			'speech': stt.recognize(
				recs[1],
				content_type=recs[1].content_type,
				word_alternatives_threshold=0.9
			).get_result()
		}
	}


def process(recordings):
	with ThreadPoolExecutor(SLAVES) as executor:
		result = executor.map(slave, recordings.items())
	return {key: description for result in result for key, description in result.items()}
