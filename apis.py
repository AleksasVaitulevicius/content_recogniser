from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class ContentRecognizerController(APIView):
    permission_classes = (AllowAny,)

    def put(self, request):
        with open(request.data['file']._get_name(), 'wb') as file, request.data['file'] as file_obj:
            file.write(file_obj.read())
        return Response(status=204)
