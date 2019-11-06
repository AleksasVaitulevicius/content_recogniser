import requests


class ContentRecogniserSDK:

	__cookies = None

	def __init__(self, username, password):
		response = requests.post(
			url='https://aleksas.pythonanywhere.com/login',
			json={
				'username': username,
				'password': password
			}
		)
		if len(response.cookies) == 0:
			raise Exception('Unauthorized')
		self.__cookies = response.cookies

	def recognise(self, data):
		response = requests.put(
			url='https://aleksas.pythonanywhere.com/',
			data=data,
			headers={
				'Content-Type': 'application/x-www-form-urlencoded',
				'Referer': 'https://aleksas.pythonanywhere.com',
				'X-CSRFToken': self.__cookies.get_dict()['csrftoken']
			},
			cookies=self.__cookies
		)
		if response:
			return response.json()
		else:
			raise Exception('HTTP status=' + str(response.status_code) + ':' + response.reason)
