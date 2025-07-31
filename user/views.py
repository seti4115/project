from django.contrib.auth import login, get_user_model
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from user.authentications import authenticate
from user.serializers import UserLoginSerializer, RegisterSerializer

User = get_user_model()


class LoginAPIView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            return Response({'message': _('You are already logged in.')})
        return Response({'message': _('Please enter your phone number')}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            password = serializer.validated_data.get('password')
            user = authenticate(phone, password)

            if user is not None:
                login(request, user)
                return Response({'message': _("Logged in")}, status=status.HTTP_200_OK)

        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            vd = serializer.validated_data
            first_name = vd.get('first_name')
            last_name = vd.get('last_name')
            username = vd.get('username')
            phone = vd.get('phone')
            email = vd.get('email')
            password = vd.get('password')

            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=username,
                phone=phone,
                email=email,
            )
            user.set_password(password)
            user.save()
            return redirect(reverse('login'))

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
