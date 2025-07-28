from django.contrib.auth import login
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user.authentications import authenticate
from user.serializers import UserLoginSerializer


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
