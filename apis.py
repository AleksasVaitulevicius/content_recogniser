from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from logic import main_service as ms


class ContentRecognizerController(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return render(request, 'documentation.html')

    def put(self, request):
        result = ms.process(request.data)
        print(result)
        return Response(status=204)

