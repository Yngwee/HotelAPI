from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from .myauth import AuthBackend
from server.models import Room, User


def auth(request):
    if request.method == 'POST':
        auth = {}
        for key, value in request.POST.items():
            auth[key] = value
        user = AuthBackend.authenticate(request=request, username=auth['username'], password=auth['password'])
        if user is not None:
            AuthBackend.get_user(user.pk)
            login(request, user, backend='myauth.AuthBackend')
            response = HttpResponseRedirect('')
            response.set_cookie('username', user.username)
            return response
        return render(request, 'login/login.html', {'title': 'Авторизация', 'err': 'Пользователь не найден', 'request': request})
    else:
        return render(request, 'login/login.html', {'title': 'Авторизация', 'request': request})


def registration(request):
    if request.method == 'POST':
        new_user = {}
        for key, value in request.POST.items():
            new_user[key] = value
        user = User.objects.create(
            username=new_user['username'],
            email=new_user['email'],
            login=new_user['login'],
            password=new_user['password1']
        )
        # # Перенаправление пользователя на страницу регистрации
        return redirect('home')
    else:
        return render(request, 'login/registration.html', {'title': 'Регистрация', 'request': request})
def home(request):
    sort_by = request.GET.get('sort')
    price_from = request.GET.get('price_filter_from')
    price_to = request.GET.get('price_filter_to')
    capacity = request.GET.getlist('cap')
    capacity_objects = Q()
    for c in capacity:
        capacity_objects |= Q(capacity=c)

    if 'save_session' in request.session and sort_by:
        rooms = Room.objects.filter(pk__in=[item['id'] for item in request.session['save_session']])
    else:

        # В GET запросе присутствуют все фильтры
        if price_from and price_to and capacity:
            rooms = Room.objects.filter(capacity_objects, price__gte=price_from, price__lte=price_to)

        # В GET запросе только мин. и мак. цена
        elif price_from and price_to and not capacity:
            rooms = Room.objects.filter(price__gte=price_from, price__lte=price_to)

        # В GET запросе только мин. цена и кол-во комнат
        elif price_from and not price_to and capacity:
            rooms = Room.objects.filter(capacity_objects, price__gte=price_from)

        # В GET запросе только мин. цена
        elif price_from and not price_to and not capacity:
            rooms = Room.objects.filter(price__gte=price_from)

        # В GET запросе только макс. цена и кол-во комнат
        elif not price_from and price_to and capacity:
            rooms = Room.objects.filter(capacity_objects, price__lte=price_to)

        # В GET запросе только макс. цена
        elif not price_from and price_to and not capacity:
            rooms = Room.objects.filter(price__lte=price_to)

        # В GET запросе только кол-во комнат
        elif not price_from and not price_to and capacity:
            rooms = Room.objects.filter(capacity_objects)

        # В GET запросе нет параметров
        else:
            rooms = Room.objects.all()
    if sort_by:
        rooms = rooms.order_by(sort_by)
    params = {'from': price_from, 'to': price_to, 'cap': capacity,
              'sort': sort_by, 'rooms': rooms, 'num_rooms': len(rooms), 'title': 'Главная страница', 'request': request}

    request.session['save_session'] = list(rooms.values())
    if request.user.is_authenticated:
        print('Пользователь авторизирован: ', request.user.username)
    return render(request, 'main/home.html', params)
