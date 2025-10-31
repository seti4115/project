from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext as _
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from config import settings
from user.authentications import authenticate, CsrfExemptSessionAuthentication
from user.serializers import UserLoginSerializer, RegisterSerializer, ProfileSerializer, ForgotPasswordSerializer
from user.tasks import send_email

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
            send_email.delay('زراعتی نو با زراعتینو',f'سلام  {first_name} عزیز! از اینکه زراعتینو رو انتخاب کردید از شما سپاسگذاریم!' , email)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
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


class ForgotPasswordAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                print(f'uid {uid} \n token {token}')
                send_mail('reset password',
                          f'url for reset your password : http://127.0.0.1:8000/reset-password/{uid}/{token}/',
                          from_email=settings.EMAIL_HOST, recipient_list=[email, ],
                          fail_silently=False, )
                return Response(status=status.HTTP_200_OK)
            return Response({"message": _('کاربری با این ایمیل یافت نشد!')}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(APIView):
    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            print(f'uidb64 {uid} \n token {token} \n uid {uid}')
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'لینک نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'توکن منقضی شده یا نامعتبر است'}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')
        if not password:
            return Response({'error': 'رمز جدید وارد نشده'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        return Response({'message': 'رمز عبور با موفقیت تغییر یافت'}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            logout(request)
            return Response({"logout": "success"}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
