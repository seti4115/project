from django.contrib.auth import login, get_user_model
from django.utils.translation import gettext as _
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from user.authentications import authenticate
from user.serializers import UserLoginSerializer, RegisterSerializer, ProfileSerializer

User = get_user_model()


class LoginAPIView(APIView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'login': True}, status=status.HTTP_200_OK)
        return Response({"login": False}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            serializer = UserLoginSerializer(data=request.data)
            if serializer.is_valid():

                print(serializer.errors)
                phone = serializer.validated_data.get('phone')
                password = serializer.validated_data.get('password')
                user = authenticate(phone, password)
                if user is not None:
                    login(request, user)
                    return Response({'message': _("Logged in")}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": _('you are logged in.')}, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            vd = serializer.validated_data
            first_name = vd.get('first_name')
            last_name = vd.get('last_name')
            username = vd.get('username')
            phone = vd.get('phone')
            email = vd.get('email', None)
            password = vd.get('password')

            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                phone=phone,
            )
            user.set_password(password)
            user.save()
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        serializer = ProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data={
                'message': _("Profile updated"),
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=request.user.id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
