from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import AuthBackend
from django.urls import reverse
from .serializers import UserSerializer
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model


def user_login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        auth_backend = AuthBackend()
        user = auth_backend.authenticate(request=request, username=username, password=password)
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                login(request, user)
        return redirect('home')
    else:
        login_form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': login_form})


def user_logout(request):
    logout(request)
    return redirect('home')