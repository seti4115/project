from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from rest_framework import permissions, filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from admin_panel.serializers import UserEditSerializer
from request.models import ConsultingRequest, SprayingRequest
from request.serializers import RequestConsultingAdminPanelSerializer, SprayingRequestAdminPanelSerializer
from .models import AdminPanel
from .permissions import IsAdminPanelPermission, IsSuperAdminPanelPermission

User = get_user_model()


class AdminPanelAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminPanelPermission]

    def get(self, request, *args, **kwargs):
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
        return Response({}, status=status.HTTP_200_OK)


class UserListAdminPanel(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserEditSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'phone', 'id', 'email', 'last_name']
    ordering_fields = ['phone', 'last_name', 'date_joined', 'last_login']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminPanelPermission(), ]
        elif self.action in ['destroy', 'update', 'partial_update']:
            return [IsSuperAdminPanelPermission(), ]
        return super().get_permissions()


class ConsultingListAdminPanelView(ListCreateAPIView):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id", "phone", "status", "created_at"]
    serializer_class = RequestConsultingAdminPanelSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminPanelPermission, IsSuperAdminPanelPermission]

    def get_queryset(self):
        q = ConsultingRequest.objects.all()
        params = self.request.GET

        ids = params.getlist("id") or params.get("id")
        phones = params.getlist("phone") or params.get("phone")
        statuses = params.getlist("status") or params.get("status")
        search = params.get("search")
        date_after = params.get("start_date")
        date_before = params.get("end_date")

        if ids:
            if isinstance(ids, str):
                ids = ids.replace(",", " ").split()
            q = q.filter(id__in=ids)

        if phones:
            if isinstance(phones, str):
                phones = phones.replace(",", " ").split()
            q = q.filter(phone__in=phones)

        if statuses:
            if isinstance(statuses, str):
                statuses = statuses.replace(",", " ").split()
            q = q.filter(status__in=statuses)

        if date_after and date_before:
            q = q.filter(created_at__range=[date_after, date_before])
        elif date_after:
            q = q.filter(created_at__gte=date_after)
        elif date_before:
            q = q.filter(created_at__lte=date_before)

        if search:
            search_vector = SearchVector("id","first_name","last_name",weight="A",config="simple") + SearchVector("province","city","land_product","message", weight="B", config="simple")
            search_query = SearchQuery(search, config="simple")
            q = (
                q.annotate(rank=SearchRank(search_vector, search_query))
                .filter(rank__gte=0.1)
                .order_by("-rank")
            )

        return q


class RetrieveUpdateDestroyConsultingAdminPanel(RetrieveUpdateDestroyAPIView):
    queryset = ConsultingRequest.objects.all()
    model = ConsultingRequest
    permission_classes = [permissions.IsAuthenticated, IsAdminPanelPermission, IsSuperAdminPanelPermission]


class SprayingListAdminPanelView(ListCreateAPIView):
    serializer_class = SprayingRequestAdminPanelSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id", "phone", "status", "created_at"]
    permission_classes = [permissions.IsAuthenticated, IsAdminPanelPermission, IsSuperAdminPanelPermission]

    def get_queryset(self):
        q = SprayingRequest.objects.all()
        params = self.request.GET

        ids = params.getlist("id") or params.get("id")
        phones = params.getlist("phone") or params.get("phone")
        statuses = params.getlist("status") or params.get("status")
        search = params.get("search")
        date_after = params.get("start_date")
        date_before = params.get("end_date")

        if ids:
            if isinstance(ids, str):
                ids = ids.replace(",", " ").split()
            q = q.filter(id__in=ids)

        if phones:
            if isinstance(phones, str):
                phones = phones.replace(",", " ").split()
            q = q.filter(phone__in=phones)

        if statuses:
            if isinstance(statuses, str):
                statuses = statuses.replace(",", " ").split()
            q = q.filter(status__in=statuses)

        if date_after and date_before:
            q = q.filter(created_at__range=[date_after, date_before])
        elif date_after:
            q = q.filter(created_at__gte=date_after)
        elif date_before:
            q = q.filter(created_at__lte=date_before)

        if search:
            search_vector = SearchVector("id", "first_name", "last_name", weight="A", config="simple") + SearchVector(
                "province", "city", "land_product", "message", weight="B", config="simple")
            search_query = SearchQuery(search, config="simple")
            q = (
                q.annotate(rank=SearchRank(search_vector, search_query))
                .filter(rank__gte=0.1)
                .order_by("-rank")
            )

        return q


class RetrieveUpdateDestroySprayingAdminPanel(RetrieveUpdateDestroyAPIView):
    queryset = ConsultingRequest.objects.all()
    model = ConsultingRequest
    permission_classes = [permissions.IsAuthenticated, IsAdminPanelPermission, IsSuperAdminPanelPermission]




class IsAdminPanel(APIView):
    def get(self, request, *args, **kwargs):
        admin = AdminPanel.objects.filter(user=request.user).exists()
        return Response({'admin': admin}, status=status.HTTP_200_OK)
