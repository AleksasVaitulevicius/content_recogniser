from concurrent.futures.thread import ThreadPoolExecutor
from acrcloud.recognizer import ACRCloudRecognizer
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from config import AcrCloud, WatsonStt
import json

SLAVES = 5
re = ACRCloudRecognizer(AcrCloud)
ibm_auth = IAMAuthenticator(WatsonStt.API_KEY)
stt = SpeechToTextV1(authenticator=ibm_auth)
stt.set_service_url(WatsonStt.SERVICE_URL)


def slave(rec):
	return {
		rec[0]: {
			'music': process_music(rec[1]),
			'speech': process_speech(rec[1])
		}
	}


def process_speech(rec):
	try:
		return stt.recognize(
			rec,
			content_type=rec.content_type,
			word_alternatives_threshold=0.9
		).get_result()
	except Exception as e:
		print(e)
		return "error occurred:" + str(e)


def process_music(rec):
	try:
		return json.loads(re.recognize_by_filebuffer(rec.read(), 0, 600))
	except Exception as e:
		print(e)
		return "error occurred:" + str(e)


def process(recordings):
	with ThreadPoolExecutor(SLAVES) as executor:
		result = executor.map(slave, recordings.items())
	return {key: description for result in result for key, description in result.items()}
