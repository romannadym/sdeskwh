from django.contrib.auth import get_user_model

from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(label = 'E-mail:', write_only = True)
    password = serializers.CharField(label = 'Пароль:',style = {'input_type': 'password'}, trim_whitespace = False, write_only = True)

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(label = "Старый пароль", style = {'input_type': 'password'}, trim_whitespace = False, write_only = True)
    new_password1 = serializers.CharField(label = "Новый пароль", style = {'input_type': 'password'}, trim_whitespace = False, write_only = True)
    new_password2 = serializers.CharField(label = "Подтверждение нового пароля", style = {'input_type': 'password'}, trim_whitespace = False, write_only = True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = '__all__'

class AdminPasswordChangeSerializer(serializers.Serializer):
    password1 = serializers.CharField(label = "Новый пароль", style = {'input_type': 'password'}, trim_whitespace = False, write_only = True)
    password2 = serializers.CharField(label = "Подтверждение нового пароля", style = {'input_type': 'password'}, trim_whitespace = False, write_only = True)

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True)

class PasswordResetConfirmSerializer(serializers.Serializer):
    password1 = serializers.CharField(label = "Новый пароль", style = {'input_type': 'password'}, trim_whitespace = False, write_only = True)
    password2 = serializers.CharField(label = "Подтверждение нового пароля", style = {'input_type': 'password'}, trim_whitespace = False, write_only = True)
