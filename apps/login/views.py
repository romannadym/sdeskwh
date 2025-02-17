from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, AdminPasswordChangeForm
from django.urls import reverse

from login.api.api import LoginAPIView, PasswordChangeAPIView

from integrator.apps.functions import is_admin_or_engineer, get_user_by_id

def LoginView(request):
    link = reverse('home')
    if request.GET:
        link = request.GET['next']
    context = {'show': is_admin_or_engineer(request.user), 'link': link}
    return render(request, 'login/login.html', context)

def PasswordChangeView(request, link):
    form = PasswordChangeForm(user = request.user)
    context = {'form': form, 'action': reverse('api-change-password'), 'link': link}
    return render(request, 'login/password_change.html', context)

def AdminPasswordChangeView(request, user_id, link):
    form = AdminPasswordChangeForm(user = get_user_by_id(user_id))
    context = {'form': form, 'action': reverse('api-admin-change-password', kwargs = {'user_id': user_id}), 'link': link}
    return render(request, 'login/password_change.html', context)
