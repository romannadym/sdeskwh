from django.urls import path
from main.views import IndexView, ServicesView, GetInTouchView, NotificationsView#, CaptchaView

urlpatterns = [
    path('', IndexView, name = 'home'),
    path('services/', ServicesView, name = 'services'),
    path('contacts/', GetInTouchView, name = 'contacts'),
    #path('captcha/', CaptchaView, name = 'captcha'),
    path('notifications/', NotificationsView),
]
