from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from request.models import Type, ConsultingRequest
from request.serializers import UserRequestConsultingSerializer, ViewRequestConsultingSerializer


class UserRequestConsultingAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRequestConsultingSerializer(data=request.data)
        if serializer.is_valid():
            request_consulting = serializer.save()
            if request.user.is_authenticated:
                request_consulting.user = request.user
            request_consulting.type = Type.CONSULTING
            request_consulting.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        requests = ConsultingRequest.objects.filter(phone=request.user.phone, type=Type.CONSULTING)
        serializer = ViewRequestConsultingSerializer(requests, many=True)
        return Response(serializer.data)
