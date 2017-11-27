from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return JsonRequset({'result':True})
    return JsonRequest({'result':False})

def user_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_check = request.POST['password_check']
        if User.filter(username=username).exists():
            return JsonRequest({'result':False,'duplicated':True})
        user = User.objects.create_user(username=username,password=password)
        return JsonRequest({'result':True,'duplicated':False})





