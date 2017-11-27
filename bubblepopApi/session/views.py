from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from apiapp.models import UserProfile,UserBlackList
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request,user)
            profile = UserProfile.objects.get(user=user)
            black_list = UserBlackList.objects.filter(user=user)

            return JsonResponse({
                'result':True,
                'black_list':[n.media.mid for n in list(black_list)],
                'token': profile.save_token(),
            })

    return JsonResponse({
        'result': False,
        'black_list': [],
    })


@csrf_exempt
def user_register(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_check = request.POST['password_check']

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'result': False,
                'duplicated': True
            })

        user = User.objects.create_user(
                username=username,
                password=password
        )
        profile = UserProfile.objects.create(user=user)
        token = profile.save_token()

        return JsonResponse({
            'result': True,
            'duplicated': False,
            'token': token,
        })

