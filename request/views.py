from django.db.models import Q
from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from request.models import Type, ConsultingRequest, SprayingRequest
from request.serializers import UserRequestConsultingSerializer, ViewRequestConsultingSerializer, \
    SprayingRequestSerializer, ViewSprayingRequestSerializer
from utils.methods import date_filter, filter_queryset, get_user_agent, ip_address, jalali_to_gregorian, ordering_filter


class UserRequestConsultingAPIView(APIView):
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
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        requests = ConsultingRequest.objects.filter(phone=request.user.phone, type=Type.CONSULTING)
        requests = filter_queryset(request.query_params, ["id", "status"], requests)
        requests = ordering_filter(request.query_params, requests)
        requests = date_filter(request.query_params, requests, "created_at")
        serializer = ViewRequestConsultingSerializer(requests, many=True)
        return Response(serializer.data)



class UserRequestSprayingAPIView(APIView):

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
        requests = filter_queryset(request.query_params, ["id", "status"], requests)
        requests = ordering_filter(request.query_params, requests)
        requests = date_filter(request.query_params, requests, "created_at")
        serializer = ViewSprayingRequestSerializer(requests, many=True)
        return Response(serializer.data)



class UserRequestPanelAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request: Request, *args, **kwargs):
        count_c = ConsultingRequest.objects.filter(phone=request.user.phone).count()
        count_s = SprayingRequest.objects.filter(phone=request.user.phone).count()
        # todo: تعداد خریدهاش
        return Response({"consulting_count": count_c, "spraying_count": count_s}, status=status.HTTP_200_OK)