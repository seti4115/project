from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from request.models import Type, ConsultingRequest, SprayingRequest
from request.serializers import UserRequestConsultingSerializer, ViewRequestConsultingSerializer, \
    SprayingRequestSerializer, ViewSprayingRequestSerializer
from user.throttles import DailyPostThrottle


class UserRequestConsultingAPIView(APIView):
    throttle_classes = [DailyPostThrottle]
    def post(self, request: Request, *args, **kwargs):
        serializer = UserRequestConsultingSerializer(data=request.data)
        if serializer.is_valid():
            request_consulting = serializer.save()
            if request.user.is_authenticated:
                request_consulting.user = request.user
            request_consulting.type = Type.CONSULTING
            request_consulting.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request, *args, **kwargs):
        if request.GET.get("search", None):
            pass
            # todo: search code
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        requests = ConsultingRequest.objects.filter(phone=request.user.phone, type=Type.CONSULTING)
        serializer = ViewRequestConsultingSerializer(requests, many=True)
        return Response(serializer.data)

    # def get_throttles(self):
    #     if self.request.method == 'POST':
    #         return [DailyPostThrottle,]
    #     else:
    #         return super().get_throttles()


class UserRequestSprayingAPIView(APIView):
    throttle_classes = [DailyPostThrottle]
    def post(self, request: Request, *args, **kwargs):
        serializer = SprayingRequestSerializer(data=request.data)
        if serializer.is_valid():
            request_spraying = serializer.save()
            if request.user.is_authenticated:
                request_spraying.user = request.user
            request_spraying.type = Type.SPRAYING
            request_spraying.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request: Request, *args, **kwargs):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        requests = SprayingRequest.objects.filter(phone=request.user.phone, type=Type.SPRAYING)
        serializer = ViewSprayingRequestSerializer(requests, many=True)
        return Response(serializer.data)
