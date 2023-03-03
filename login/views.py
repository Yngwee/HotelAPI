from django.shortcuts import render

def auth(request):
    return render(request, 'login/login.html', {'title': 'Авторизация'})

def registration(request):
    return render(request, 'login/registration.html', {'title': 'Регистрация'})