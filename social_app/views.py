from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.


def log_out(request):
    logout(request)
    return HttpResponse('شما خارج شدید!')


def profile(request):
    return HttpResponse('شما وارد شدید!')
