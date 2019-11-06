import io
import os
import requests


class ContentRecogniserSDK:

	# __host = 'http://127.0.0.1:8000/'
	__host = 'https://aleksas.pythonanywhere.com/'
	__cookies = None

	def __init__(self, user=None, password=None):
		if not isinstance(user, dict):
			user = {
				'username': user,
				'password': password,
			}
		response = requests.post(url=self.__host + 'login', json=user)
		if len(response.cookies) == 0:
			raise Exception('Unauthorized')
		self.__cookies = response.cookies

	def recognise(self, data):
		files = {key: record for key, record in data.items() if isinstance(record, io.IOBase)}
		data = {key: record for key, record in data.items() if not isinstance(record, io.IOBase)}
		response = requests.put(
			url=self.__host,
			data=data,
			headers={
				'Referer': self.__host,
				'X-CSRFToken': self.__cookies.get_dict()['csrftoken']
			},
			files=files,
			cookies=self.__cookies
		)
		if response:
			return response.json()
		else:
			raise Exception('HTTP status=' + str(response.status_code) + ':' + response.reason)

	def recognise_from_directory(self, path):
		data = {
			file: open(os.path.join(path, file), 'rb')
			for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))
		}
		return self.recognise(data)
