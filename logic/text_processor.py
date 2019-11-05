from concurrent.futures.thread import ThreadPoolExecutor

import detectlanguage as dl
from ibm_watson import ToneAnalyzerV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from config import WatsonTA, DetectLanguage

dl.configuration.api_key = DetectLanguage.API_KEY

ibm_auth = IAMAuthenticator(WatsonTA.API_KEY)
ta = ToneAnalyzerV3(authenticator=ibm_auth, version='2017-09-21')
ta.set_service_url(WatsonTA.SERVICE_URL)

ACTION_LIST = [
	# ('language_detection', lambda contents: detect_languages(contents)),
	# ('tone_analysis', lambda contents: detect_tone(contents)),
]
N_SLAVES = 2


def detect_tone(contents):
	try:
		return [ta.tone(content).get_result() for content in contents]
	except Exception as e:
		print(e)
		return "Error occurred"


def detect_languages(contents):
	try:
		return [content[0] for content in dl.detect(contents)]
	except Exception:
		return "Error occurred"


def merge_results(results):
	return [
		{action_name: res for (action_name, _), res in zip(ACTION_LIST, result)}
		for result in results
	]


def execute_in_parallel(contents):
	actions = [action for _, action in ACTION_LIST]
	with ThreadPoolExecutor(N_SLAVES) as executor:
		future = executor.map(lambda action, value: action(value), actions, [contents] * len(actions))
	return future


def process(texts):
	contents = list(texts.values())
	keys = list(texts.keys())
	if len(keys) == 0:
		return {}
	results = list(zip(*execute_in_parallel(contents)))
	results = merge_results(results)
	return dict(zip(keys, results))
