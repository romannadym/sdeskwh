from django.contrib.auth import get_user_model
from django.db.models import Value, Q, F, Case, When, CharField
from django.db.models.functions import Concat

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema

from integrator.apps.serializers import *

@extend_schema(tags = ['Список инженеров (Done)'],)
class EngineersListAPIView(generics.ListAPIView):
    queryset = get_user_model().objects.filter(groups__name = 'Инженер')\
        .annotate(name = Case(
            When(
                Q(last_name__isnull = False) & ~Q(last_name = ''),
                then = Concat('first_name', Value(' '), 'last_name')
            ),
            When(last_name = '', then = F('email')),
            default = Value(''), output_field = CharField())
        )
    serializer_class = EngineerSerializer
    permission_classes = [IsAuthenticated]
