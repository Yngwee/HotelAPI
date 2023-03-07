from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.models import User
from server.models import Room, BoockedRoom


def auth(request):
    if request.method == 'POST':
        auth_user = {}
        for key, value in request.POST.items():
            auth_user[key] = value
            print(key, ': ', auth_user[key])

        user = User.objects.get(username=auth_user['username'])
        password_correct = user.check_password(auth_user['password'])
        try:
            if password_correct:
                login(request, user)
                response = HttpResponseRedirect('../')
                response.set_cookie('username', auth_user['username'])
                return response
        except:
            return render(request, 'login/login.html', {'title': 'Регистрация', 'err': 'Пользователь не найден'})
        return redirect('home')
    return render(request, 'login/login.html', {'title': 'Авторизация'})

def log_out(request):
    logout(request)
    return redirect('home')

def registration(request):
    if request.method == 'POST':
        new_user = {}
        for key, value in request.POST.items():
            new_user[key] = value
        try:
            user = User.objects.create_user(username=new_user['username'], email=new_user['email'],
                                            first_name=new_user['first_name'], last_name=new_user['last_name'],
                                            password=new_user['password1'])
            user.save()
        except:
            return render(request, 'login/registration.html', {'title': 'Регистрация', 'request': request,
                                                               'err': 'Не удалось создать учетную запись. Возможно, '
                                                                      'пользователь с таким логином или '
                                                                      'электронной почтой уже существует'})
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
    return render(request, 'main/home.html', params)

def booking(request):
    if request.method == 'POST':
        booking_room = {}
        for key, value in request.POST.items():
            booking_room[key] = value
        try:
            room = BoockedRoom.objects.create(username=request.user.username, )
            room.save()
        except:
            return render(request, 'login/registration.html', {'title': 'Регистрация', 'request': request,
                                                               'err': 'Не удалось создать учетную запись. Возможно, '
                                                                      'пользователь с таким логином или '
                                                                      'электронной почтой уже существует'})
        return redirect('home')
    else:
        return render(request, 'login/registration.html', {'title': 'Регистрация', 'request': request})


