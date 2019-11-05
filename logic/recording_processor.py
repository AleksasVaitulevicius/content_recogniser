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


ACTION_LIST = [
	('music', process_music),
	('speech', process_speech),
]


def slave(rec):
	if len(ACTION_LIST) == 0:
		return {rec[0]: ""}
	action_value_tuples = [(action, rec[1]) for _, action in ACTION_LIST]
	with ThreadPoolExecutor(len(ACTION_LIST)) as executor:
		future = executor.map(lambda action_value: action_value[0](action_value[1]), action_value_tuples)
	return {
		rec[0]: {key: result for (key, _), result in zip(ACTION_LIST, future)}
	}


def process(recordings):
	with ThreadPoolExecutor(SLAVES) as executor:
		result = executor.map(slave, recordings.items())
	return {key: description for result in result for key, description in result.items()}
