from django.contrib.auth import get_user_model

from rest_framework import serializers

class EngineerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(label = 'ФИО')

    class Meta:
        model = get_user_model()
        fields = ['id', 'name']
