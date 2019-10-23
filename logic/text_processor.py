import detectlanguage as dl

dl.configuration.api_key = '1f64cbddd63bd66c8f0052d072d2c36e'

ACTION_LIST = [
	('language_detection', lambda contents: [content[0] for content in detect_languages(contents)]),
]


def detect_languages(contents):
	try:
		return dl.detect(contents)
	except Exception:
		return "Unavailable"


def merge_results(results):
	return [
		{action_name: res for (action_name, _), res in zip(ACTION_LIST, result)}
		for result in results
	]


def process(texts):
	contents = list(texts.values())
	keys = list(texts.keys())
	results = list(zip(*[action(contents) for _, action in ACTION_LIST]))
	results = merge_results(results)
	return dict(zip(keys, results))
