class Imagga:
	API_URL = "https://api.imagga.com/v2/"
	API_KEY = ''
	API_SECRET = ''
	UPLOAD_URL = API_URL + 'uploads'
	BATCH_URL = API_URL + 'batches'
	TICKET_URL = API_URL + 'tickets/'


AcrCloud = {
	'host': '',
	'access_key': '',
	'access_secret': '',
	'timeout': 10  # seconds
}


class WatsonStt:
	API_KEY = ''
	SERVICE_URL = 'https://gateway-lon.watsonplatform.net/speech-to-text/api'


class WatsonTA:
	API_KEY = ''
	SERVICE_URL = 'https://gateway-lon.watsonplatform.net/tone-analyzer/api'


class DetectLanguage:
	API_KEY = ''
