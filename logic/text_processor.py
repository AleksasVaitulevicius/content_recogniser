from concurrent.futures.thread import ThreadPoolExecutor

import detectlanguage as dl

dl.configuration.api_key = '1f64cbddd63bd66c8f0052d072d2c36e'

ACTION_LIST = [
	# ('language_detection', lambda contents: detect_languages(contents)),
	('test_text', lambda contents: ['text' for _ in contents]),
]
N_SLAVES = 2


def detect_languages(contents):
	try:
		return [content[0] for content in dl.detect(contents)]
	except Exception:
		return "Unavailable"


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
	results = list(zip(*execute_in_parallel(contents)))
	results = merge_results(results)
	return dict(zip(keys, results))
