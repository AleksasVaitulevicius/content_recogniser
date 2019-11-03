from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.shortcuts import render
from logic import main_service as ms


class ContentRecognizerController(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request):
        return render(request, 'documentation.html')

    @staticmethod
    def put(request):
        if not request.user.is_authenticated:
            return HttpResponse(status=401)
        result = ms.process(request.data)
        return JsonResponse(result, safe=False)

