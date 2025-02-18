from django.urls import path
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import views as auth_views
from login.views import LoginView, PasswordChangeView, AdminPasswordChangeView
from login.api.api import LoginAPIView, PasswordChangeAPIView, AdminPasswordChangeAPIView, PasswordResetView, PasswordResetConfirmView

urlpatterns = [
    path('user_login/', LoginView, name = 'login'),
    path('user_login/<str:link>', LoginView, name = 'login'),
    path('password/<str:link>', PasswordChangeView, name = 'change-password'),
    path('admin/password/<int:user_id>/<str:link>', AdminPasswordChangeView, name = 'admin-change-password'),
    # path('password/<str:link>/<int:user_id>', PasswordChangeView, name = 'admin-change-password'),
    #password_reset - name заданы в самом django
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'login/password_reset.html'), name = 'reset_password'), #страница ввода e-mail
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name = 'login/password_reset_sent.html'), name = 'password_reset_done'), #e-mail отправлен
    path('password_reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'login/password_reset_form.html'), name = 'password_reset_confirm'), #переход по ссылке из e-mail
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'login/password_reset_done.html'), name = 'password_reset_complete'), #пароль изменен

    path('api/user_login/', LoginAPIView.as_view(), name = 'api-login'),
    path('api/password/', PasswordChangeAPIView.as_view(), name = 'api-change-password'),
    path('api/admin/password/<int:user_id>', AdminPasswordChangeAPIView.as_view(), name = 'api-admin-change-password'),
    path('api/reset_password/', PasswordResetView.as_view(), name = 'api-reset-password'),
    path('api/reset_password_confirm/<uid>/<token>/', PasswordResetConfirmView.as_view(), name = 'api-reset-password-confirm'),
]
