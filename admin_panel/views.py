from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from rest_framework import permissions, filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_panel.serializers import AdminPanelSerializer, UserEditSerializer
from request.models import ConsultingRequest, SprayingRequest
from request.serializers import RequestConsultingAdminPanelSerializer, SprayingRequestAdminPanelSerializer
from utils.methods import filter_queryset, get_user_agent, ip_address, jalali_to_gregorian
from .models import AdminPanel
from .permissions import IsFrontAdminPanelPermission, IsSuperAdminPanelPermission

User = get_user_model()


class AdminPanelAPIView(APIView):
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]

    def get(self, request, *args, **kwargs):
        users_count = User.objects.count()
        consulting_count = ConsultingRequest.objects.count()
        spraying_count = SprayingRequest.objects.count()
        # users = User.objects.all()
        # consulting_requests = ConsultingRequest.objects.all().order_by("-created_at")
        # spraying_requests = SprayingRequest.objects.all().order_by("-created_at")
        # serializer = AllSerializer(
        #     {
        #         "users": UserDetailSerializer(users, many=True).data,
        #         "consulting_requests": ViewRequestConsultingSerializer(consulting_requests, many=True).data,
        #         "spraying_requests": ViewSprayingRequestSerializer(spraying_requests, many=True).data,
        #     }
        # )
        return Response({
            'users_count': users_count,
            'consulting_count': consulting_count,
            'spraying_count': spraying_count,
        }, status=status.HTTP_200_OK)



class UserListAdminPanel(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserEditSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'phone', 'id', 'email', 'last_name']
    ordering_fields = ['phone', 'last_name', 'date_joined', 'last_login']

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.GET
        queryset = filter_queryset(params, ["id", "phone", "is_active", "is_admin", "username"], queryset)
        date_after = params.get("start_date")
        date_before = params.get("end_date")
        if date_after and date_before:
            date_after = jalali_to_gregorian(date_after)
            date_before = jalali_to_gregorian(date_before)
            queryset = queryset.filter(date_joined__range=[date_after, date_before])
        elif date_after:
            date_after = jalali_to_gregorian(date_after)
            queryset = queryset.filter(date_joined__gte=date_after)
        elif date_before:
            date_before = jalali_to_gregorian(date_before)
            queryset = queryset.filter(date_joined__lte=date_before)
        return queryset.all()


class UserDetailUpdateDestroyAdminPanel(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserEditSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]



class ConsultingListAdminPanelView(ListAPIView):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id", "phone", "status", "created_at"]
    serializer_class = RequestConsultingAdminPanelSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]

    def get_queryset(self):
        q = ConsultingRequest.objects.all()
        params = self.request.GET
        search = params.get("search")
        date_after = params.get("start_date")
        date_before = params.get("end_date")
        q = filter_queryset(params, ["id", "status", "phone"], q)
        try:
            if date_after and date_before:
                date_after = jalali_to_gregorian(date_after)
                date_before = jalali_to_gregorian(date_before)
                q = q.filter(created_at__range=[date_after, date_before])
            elif date_after:
                date_after = jalali_to_gregorian(date_after)
                q = q.filter(created_at__gte=date_after)
            elif date_before:
                date_before = jalali_to_gregorian(date_before)
                q = q.filter(created_at__lte=date_before)

            if search:
                q = q.filter(
                    Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(
                        province__icontains=search) | Q(city__icontains=search) | Q(land_product__icontains=search) | Q(
                        message__icontains=search))
                # search_vector = SearchVector("id","first_name","last_name",weight="A",config="simple") + SearchVector("province","city","land_product","message", weight="B", config="simple")
                # search_query = SearchQuery(search, config="simple")
                # q = (
                #     q.annotate(rank=SearchRank(search_vector, search_query))
                #     .filter(rank__gte=0.1)
                #     .order_by("-rank")
                # )
        except Exception as e:
            return Response({"error": "bad query sent."}, status=status.HTTP_400_BAD_REQUEST)
        return q



class RetrieveUpdateDestroyConsultingAdminPanel(RetrieveUpdateDestroyAPIView):
    queryset = ConsultingRequest.objects.all()
    model = ConsultingRequest
    serializer_class = RequestConsultingAdminPanelSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]



class SprayingListAdminPanelView(ListAPIView):
    serializer_class = SprayingRequestAdminPanelSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id", "phone", "status", "created_at"]

    def get_queryset(self):
        q = SprayingRequest.objects.all()
        params = self.request.GET
        search = params.get("search")
        date_after = params.get("start_date")
        date_before = params.get("end_date")
        q = filter_queryset(params, ["id", "status", "phone"], q)
        try:
            if date_after and date_before:
                date_after = jalali_to_gregorian(date_after)
                date_before = jalali_to_gregorian(date_before)
                q = q.filter(created_at__range=[date_after, date_before])
            elif date_after:
                date_after = jalali_to_gregorian(date_after)
                q = q.filter(created_at__gte=date_after)
            elif date_before:
                date_before = jalali_to_gregorian(date_before)
                q = q.filter(created_at__lte=date_before)

            if search:
                q = q.filter(
                    Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(
                        province__icontains=search) | Q(city__icontains=search) | Q(land_product__icontains=search) | Q(
                        message__icontains=search) | Q(address__icontains=search))
                # search_vector = SearchVector("id","first_name","last_name",weight="A",config="simple") + SearchVector("province","city","land_product","message", weight="B", config="simple")
                # search_query = SearchQuery(search, config="simple")
                # q = (
                #     q.annotate(rank=SearchRank(search_vector, search_query))
                #     .filter(rank__gte=0.1)
                #     .order_by("-rank")
                # )
        except Exception as e:
            return Response({"error": "bad query sent."}, status=status.HTTP_400_BAD_REQUEST)
        return q

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]


class RetrieveUpdateDestroySprayingAdminPanel(RetrieveUpdateDestroyAPIView):
    queryset = SprayingRequest.objects.all()
    model = SprayingRequest
    serializer_class = SprayingRequestAdminPanelSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]


class IsAdminPanel(APIView):
    def get(self, request, *args, **kwargs):
        admin = AdminPanel.objects.filter(user=request.user).exists()
        return Response({'admin': admin}, status=status.HTTP_200_OK)


class ListCreateAdminPanelAPIView(ListCreateAPIView):
    queryset = AdminPanel.objects.all()
    serializer_class = AdminPanelSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]



class RetrieveUpdateDestroyAdminPanelAPIView(RetrieveUpdateDestroyAPIView):
    queryset = AdminPanel.objects.all()
    serializer_class = AdminPanelSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]

