from django.db.models import Q
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from request.models import Type, ConsultingRequest, SprayingRequest
from request.serializers import UserRequestConsultingSerializer, ViewRequestConsultingSerializer, \
    SprayingRequestSerializer, ViewSprayingRequestSerializer
from user.throttles import DailyPostThrottle
from utils.methods import filter_queryset, jalali_to_gregorian


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
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        requests = ConsultingRequest.objects.filter(phone=request.user.phone, type=Type.CONSULTING)
        requests = filter_queryset(request.query_params, ["id", "status"], requests)
        search = request.query_params.get("search")
        order = request.query_params.get("ordering")
        date_after = request.query_params.get("start_date")
        date_before = request.query_params.get("end_date")
        try:
            if order:
                if order.startswith("-"):
                    requests = requests.order_by(f"-{order}")
                else:
                    requests = requests.order_by(order)
            if date_after and date_before:
                date_after = jalali_to_gregorian(date_after)
                date_before = jalali_to_gregorian(date_before)
                requests = requests.filter(created_at__range=[date_after, date_before])
            elif date_after:
                date_after = jalali_to_gregorian(date_after)
                requests = requests.filter(created_at__gte=date_after)
            elif date_before:
                date_before = jalali_to_gregorian(date_before)
                requests = requests.filter(created_at__lte=date_before)

            if search:
                requests = requests.filter(
                     Q(
                        province__icontains=search) | Q(city__icontains=search) | Q(land_product__icontains=search) | Q(
                        message__icontains=search))
        except Exception as e:
            return Response({"error": "bad query sent."}, status=status.HTTP_400_BAD_REQUEST)
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
        requests = filter_queryset(request.query_params, ["id", "status"], requests)
        search = request.query_params.get("search")
        order = request.query_params.get("ordering")
        date_after = request.query_params.get("start_date")
        date_before = request.query_params.get("end_date")
        try:
            if order:
                if order.startswith("-"):
                    requests = requests.order_by(f"-{order}")
                else:
                    requests = requests.order_by(order)
            if date_after and date_before:
                date_after = jalali_to_gregorian(date_after)
                date_before = jalali_to_gregorian(date_before)
                requests = requests.filter(created_at__range=[date_after, date_before])
            elif date_after:
                date_after = jalali_to_gregorian(date_after)
                requests = requests.filter(created_at__gte=date_after)
            elif date_before:
                date_before = jalali_to_gregorian(date_before)
                requests = requests.filter(created_at__lte=date_before)

            if search:
                requests = requests.filter(
                    Q(province__icontains=search) | Q(city__icontains=search) | Q(land_product__icontains=search) |
                    Q(message__icontains=search) | Q(address__icontains=search))
        except Exception as e:
            return Response({"error": "bad query sent."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ViewSprayingRequestSerializer(requests, many=True)
        return Response(serializer.data)
