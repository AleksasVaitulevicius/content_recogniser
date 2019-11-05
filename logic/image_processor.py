from concurrent.futures.thread import ThreadPoolExecutor

from ibm_watson import VisualRecognitionV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from config import WatsonVR

N_SLAVES = 5

authenticator = IAMAuthenticator(WatsonVR.API_KEY)
visual_recognition = VisualRecognitionV3(version='2018-03-19', authenticator=authenticator)
visual_recognition.set_service_url(WatsonVR.SERVICE_URL)


def send_request(key, image):
	try:
		return {
			key: visual_recognition.classify(
				images_file=image
			).get_result()
		}
	except Exception as e:
		print(e)
		return {key: str(e)}


def process(images):
	if len(images.items()) == 0:
		return {}
	with ThreadPoolExecutor(len(images.items())) as executor:
		future = executor.map(send_request, images.keys(), images.values())
	return {key: description for result in list(future) for key, description in result.items()}
