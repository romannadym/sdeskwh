from django.urls import path
from admin.views import IndexView

urlpatterns = [
    path('', IndexView, name = 'admin-index'),
]
