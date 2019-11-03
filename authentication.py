from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from rest_framework.views import APIView


class Authentication(APIView):

	@staticmethod
	def post(request):
		keys = request.data.keys()
		if 'username' not in keys or 'password' not in keys:
			return HttpResponse(status=401)
		username = request.data['username']
		password = request.data['password']
		user = authenticate(request, username=username, password=password)
		if user is None:
			return HttpResponse(status=401)
		login(request, user)
		return HttpResponse(status=200)
