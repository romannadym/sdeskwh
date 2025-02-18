from datetime import datetime, timedelta

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model, password_validation
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException

<<<<<<< HEAD
from drf_spectacular.utils import extend_schema
=======
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse
>>>>>>> 0b86e9e586987b8a392d3f43c66c2fbb91b80e10

from login.api.serializers import *

from integrator.apps.functions import get_user_by_id

from accounts.models import UserTokenModel

@extend_schema(
    tags = ['Аутентификация пользователя (Done)', ]
)
class LoginAPIView(APIView):
    permission_classes = [AllowAny,]

    @extend_schema(
<<<<<<< HEAD
        request = LoginSerializer(),
        summary = 'Вход в учетную запись'
=======
        summary = 'Вход в учетную запись',
        description = '<ol><li>"email" - Адрес электронной почты пользователя</li><li>"password" - Пароль пользователя</li></ol>',
        request = LoginSerializer(),
        responses = {(202, 'application/json'): None}
>>>>>>> 0b86e9e586987b8a392d3f43c66c2fbb91b80e10
    )
    def post(self, request, format = None):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = authenticate(username = serializer.validated_data['email'], password = serializer.validated_data['password'])
            if user is not None:
                login(request, user)
                return Response(status = status.HTTP_202_ACCEPTED)
        # return Response(serializer.validated_data, status = status.HTTP_401_UNAUTHORIZED)
        return Response("Ошибка авторизации: указан неверный логин или пароль", status = status.HTTP_401_UNAUTHORIZED)

    @extend_schema(
<<<<<<< HEAD
          summary = 'Выход из учетной записи'
=======
          summary = 'Выход из учетной записи',
          description = 'Response - переадресация на домашную страницу приложения'
>>>>>>> 0b86e9e586987b8a392d3f43c66c2fbb91b80e10
    )
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')

<<<<<<< HEAD
=======
@extend_schema(
    tags = ['Аутентификация пользователя (Done)', ]
)
>>>>>>> 0b86e9e586987b8a392d3f43c66c2fbb91b80e10
class PasswordChangeAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    @extend_schema(
<<<<<<< HEAD
        request = PasswordChangeSerializer(),
        tags = ['Изменение пароля пользователя (Done)', ]
=======
        summary = 'Изменение пароля пользователя (Функционал доступен только клиентам)',
        description = '<ol><li>"old_password" - Старый пароль</li><li>"new_password1" - Новый пароль</li>\
        <li>"new_password2" - Новый пароль (подтверждение)</li></ol>',
        request = PasswordChangeSerializer(),
        responses = {(200, 'application/json'): None}
>>>>>>> 0b86e9e586987b8a392d3f43c66c2fbb91b80e10
    )
    def put(self, request, *args, **kwargs):
        user = request.user
        form = PasswordChangeForm(user, request.data)
        if form.is_valid():
            form.save()
            return Response(None, status = status.HTTP_200_OK)
        else:
            return Response(form.errors.as_data(), status = status.HTTP_406_NOT_ACCEPTABLE)

<<<<<<< HEAD
=======
@extend_schema(
    tags = ['Аутентификация пользователя (Done)', ]
)
>>>>>>> 0b86e9e586987b8a392d3f43c66c2fbb91b80e10
class AdminPasswordChangeAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    @extend_schema(
<<<<<<< HEAD
        request = AdminPasswordChangeSerializer(),
        tags = ['Изменение пароля пользователя администратором (Done)', ]
=======
        summary = 'Изменение пароля пользователя администратором (Функционал доступен только администраторам)',
        description = '<ol><li>"password1" - Новый пароль</li><li>"password2" - Новый пароль (подтверждение)</li></ol>',
        parameters = [
            OpenApiParameter(name = 'user_id', description = 'Идентификатор пользователя', type = int, required = True, location = OpenApiParameter.PATH),
        ],
        request = AdminPasswordChangeSerializer(),
        responses = {(200, 'application/json'): None}
>>>>>>> 0b86e9e586987b8a392d3f43c66c2fbb91b80e10
    )
    def put(self, request, user_id, *args, **kwargs):
        if not request.user.groups.filter(name = 'Администратор').exists():
            return Response({'message': 'Функционал доступен только администраторам'}, status = status.HTTP_403_FORBIDDEN)

        serializer = AdminPasswordChangeSerializer(data = request.data)
        if serializer.is_valid():
            password1 = serializer.validated_data['password1']
            password2 = serializer.validated_data['password2']
            if password1 and password2:
                if password1 != password2:
                    raise APIException('Пароли не совпадают')

                user = get_user_by_id(user_id)
                user.set_password(password1)
                user.save()

                return Response(None, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_406_NOT_ACCEPTABLE)

@extend_schema(
    tags = ['Аутентификация пользователя (Done)', ]
)
class PasswordResetView(APIView):
    permission_classes = [AllowAny,]

    @extend_schema(
<<<<<<< HEAD
        summary = 'Восстановление пароля'
=======
        summary = 'Запрос на восстановление пароля - отправка сообщения, содержащего ссылку на форму смены пароля, на электронный адрес пользователя',
        description = '"email" - Адрес электронной почты пользователя',
        request = PasswordResetSerializer(),
        responses = {(200, 'application/json'): None}
>>>>>>> 0b86e9e586987b8a392d3f43c66c2fbb91b80e10
    )
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data = request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = get_user_model().objects.get(email = email)
            if not user:
                raise APIException('Пользователь с указанным адресом не найден')
            token = get_random_string(length = 32)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            UserTokenModel.objects.filter(uid = uid).delete()
            record = UserTokenModel.objects.create(uid = uid, token = token)

            params = {
                'home': request.get_host(),
                'link': request.build_absolute_uri(reverse('password_reset_confirm', kwargs = {'uidb64': uid, 'token': token}))
            }
            text = render_to_string('accounts/password.html', params)
            mail = EmailMessage('Восстановление пароля', text, settings.EMAIL_HOST_USER, [email])
            mail.content_subtype = "html"
            try:
                mail.send()
            except:
                raise APIException('Не удалось отправить сообщение на указанный адрес')

            return Response(None, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_403_FORBIDDEN)

@extend_schema(
    tags = ['Аутентификация пользователя (Done)', ]
)
class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny,]

    @extend_schema(
<<<<<<< HEAD
        summary = 'Восстановление пароля'
=======
        summary = 'Восстановление пароля',
        description = '<ol><li>"password1" - Новый пароль</li><li>"password2" - Новый пароль (подтверждение)</li></ol>',
        parameters = [
            OpenApiParameter(name = 'uid', description = 'Идентификатор пользователя (закодированный в base 64), указанный в ссылке, пришедшей в сообщении о восстановлении пароля', type = str, required = True, location = OpenApiParameter.PATH),
            OpenApiParameter(name = 'token', description = 'Токен, указанный в ссылке, пришедшей в сообщении о восстановлении пароля', type = str, required = True, location = OpenApiParameter.PATH),
        ],
        request = PasswordResetConfirmSerializer(),
        responses = {(200, 'application/json'): None}
>>>>>>> 0b86e9e586987b8a392d3f43c66c2fbb91b80e10
    )
    def put(self, request, uid, token, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data = request.data)

        if serializer.is_valid():
            password1 = serializer.validated_data['password1']
            password2 = serializer.validated_data['password2']

            if password1 and password2:
                if password1 != password2:
                    raise APIException('Пароли не совпадают')

            delta = datetime.now() - timedelta(hours = 3)
            try:
                record = UserTokenModel.objects.filter(uid = uid, token = token, pubdate__gte = delta).exists()
            except:
                raise APIException('Пользователь не найден или истек срок действия ссылки')

            try:
                user_id = int(urlsafe_base64_decode(uid))
                user = get_user_model().objects.get(id = user_id)
            except:
                raise APIException('Пользователь не найден')

            password_validation.validate_password(password1, user)
            user.set_password(password1)
            user.save()

            return Response(None, status = status.HTTP_200_OK)

        return Response(serializer.errors, status = status.HTTP_406_NOT_ACCEPTABLE)
