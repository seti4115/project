from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q
from rest_framework import permissions, filters, status
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from admin_panel.serializers import AdminPanelSerializer, ChangePassUserAdminPanelSerializer, UserEditSerializer
from product.models import Product
from product.serializers import ProductAllFieldSerializer, ProductShowSerializer
from request.models import ConsultingRequest, SprayingRequest
from request.serializers import RequestConsultingAdminPanelSerializer, SprayingRequestAdminPanelSerializer
from site_settings.models import SiteSettings
from site_settings.serializers import ListSiteSettingsSerializer, SiteSettingsSerializer
from utils.methods import date_filter, filter_queryset, get_user_agent, ip_address, jalali_to_gregorian
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
        product_count = Product.objects.count()
        adminB_count = User.objects.filter(Q(is_superuser=True) | Q(is_staff=True)).count()
        admin_panel_count = AdminPanel.objects.count()
        return Response({
            'users_count': users_count,
            'consulting_count': consulting_count,
            'spraying_count': spraying_count,
            'product_count': product_count,
            'admin_backend_count': adminB_count,
            'admin_front_count': admin_panel_count,
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
        queryset = date_filter(params, queryset, "created_at")
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
        q = date_filter(params, q, "created_at")
        q = filter_queryset(params, ["id", "status", "phone"], q)
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
        q = filter_queryset(params, ["id", "status", "phone"], q)
        q = date_filter(params, q, "created_at")
        if search:
            search_vector = SearchVector("id","first_name","last_name",weight="A",config="simple") + SearchVector("province","city","land_product","message", weight="B", config="simple")
            search_query = SearchQuery(search, config="simple")
            q = (
                q.annotate(rank=SearchRank(search_vector, search_query))
                .filter(rank__gte=0.1)
                .order_by("-rank")
                )
        return q

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]


class RetrieveUpdateDestroySprayingAdminPanel(RetrieveUpdateDestroyAPIView):
    queryset = SprayingRequest.objects.all()
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


class ListCreateProductAdminPanelAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductAllFieldSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.GET
        search = params.get("search")
        queryset = filter_queryset(params, ["id", "status", "phone"], queryset)
        queryset = date_filter(params, queryset, "created_at")
        if search:
            search_vector = SearchVector("id", "title", "slug", "tags", weight="A", config="simple") + SearchVector(
                "title_en", "brand", "description", weight="B", config="simple")
            search_query = SearchQuery(search, config="simple")
            queryset = (
                queryset.annotate(rank=SearchRank(search_vector, search_query))
                .filter(rank__gte=0.1)
                .order_by("-rank")
            )
        return queryset


class RetrieveUpdateDestroyProductAdminPanelAPIView(RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "slug"
    lookup_field = "slug"
    queryset = Product.objects.all()
    serializer_class = ProductAllFieldSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]


class ChangePassUserAdminPanelView(APIView):
    permission_classes = [IsSuperAdminPanelPermission]

    def post(self, request:Request, *args, **kwargs):
        end_index = self.request.get_full_path()[19::].find("/")
        pk = self.request.get_full_path()[19:19 + end_index]
        user = get_object_or_404(User, pk=pk)
        serializer = ChangePassUserAdminPanelSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data["password1"])
            user.save()
            return Response({"change password": "success"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SiteSettingsAdminPanelView(ListCreateAPIView):
    queryset = SiteSettings.objects.all()

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ListSiteSettingsSerializer
        else:
            return SiteSettingsSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]


class RetrieveUpdateDestroySiteSettingsAdminPanelAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = SiteSettingsSerializer
    queryset = SiteSettings.objects.all()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [IsFrontAdminPanelPermission()]
        else:
            return [IsSuperAdminPanelPermission()]