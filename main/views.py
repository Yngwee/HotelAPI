from datetime import date, timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Room, BookedRoom


def auth(request):
    if request.method == 'POST':
        auth_user = {}
        for key, value in request.POST.items():
            auth_user[key] = value

        try:
            user = User.objects.get(username=auth_user['username'])
            password_correct = user.check_password(auth_user['password'])
        except:
            return render(request, 'login/login.html', {'title': 'Регистрация', 'err': 'Пользователь не найден'})
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
    min_date = date.today()
    max_date = date.today() + timedelta(days=1)
    if request.GET.get('date_from') and request.GET.get('date_to'):
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        request.session['date_from'] = date_from
        request.session['date_to'] = date_to

    elif 'date_from' in request.session and 'date_to' in request.session:
        date_from = request.session['date_from']
        date_to = request.session['date_to']

    else:
        return render(request, 'main/home.html', {'date': 'Выберите дату для поиска комнат', 'min_date': min_date,
                                                  'max_date': max_date})

    sort_by = request.GET.get('sort')
    price_from = request.GET.get('price_filter_from')
    price_to = request.GET.get('price_filter_to')
    capacity = request.GET.getlist('cap')
    capacity_objects = Q()

    for c in capacity:
        capacity_objects |= Q(capacity=c)

    if 'save_rooms' in request.session and sort_by:
        rooms = Room.objects.filter(pk__in=[item['id'] for item in request.session['save_rooms']])
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

    booked_rooms = BookedRoom.objects.all()
    booked_date = []
    for br in booked_rooms:
        if br.bookedDateFrom and br.bookedDateTo and date_from and date_to:
            if date_to > str(br.bookedDateFrom) and date_from < str(br.bookedDateTo):
                q = BookedRoom.objects.filter(bookedRoom=br.bookedRoom)
                booked_date.append(q)

    if booked_date:
        rooms = rooms.exclude(number__in=[item.get().bookedRoom for item in booked_date])
    if sort_by:
        rooms = rooms.order_by(sort_by)
    params = {'from': price_from, 'to': price_to, 'cap': capacity,
              'sort': sort_by, 'rooms': rooms, 'num_rooms': len(rooms), 'title': 'Главная страница', 'request': request}

    request.session['save_rooms'] = list(rooms.values())
    return render(request, 'main/home.html', params)


def my_rooms(request):
    booked_info = BookedRoom.objects.filter(username=request.user.username).values()
    print(booked_info)

    my_booked_rooms = Room.objects.filter(number__in=[item['bookedRoom_id'] for item in BookedRoom.objects.filter(
        username=request.user.username).values()])

    return render(request, 'main/my_rooms.html', {'num_rooms': len(my_booked_rooms), 'my_rooms': my_booked_rooms,
                                                  'booked_info': booked_info})


def booking(request):
    booking_room = {}
    for key, value in request.POST.items():
        booking_room[key] = value
    room = Room.objects.get(number=booking_room['number_room'])

    room = BookedRoom.objects.create(username=request.user.username,
                                     bookedDateFrom=booking_room['date_from'],
                                     bookedDateTo=booking_room['date_to'],
                                     bookedRoom=room)
    print(room)
    room.save()
    return redirect('home')


def cancel_book(request):
    if request.method == 'POST':
        number_room = request.POST.get('number_room')
        print(number_room)
        delete = BookedRoom.objects.get(username=request.user.username, bookedRoom=number_room)
        BookedRoom.delete(delete)
        my_booked_rooms = Room.objects.filter(number__in=[item['bookedRoom_id'] for item in BookedRoom.objects.filter(
            username=request.user.username).values()])
        return render(request, 'main/my_rooms.html', {'num_rooms': len(my_booked_rooms), 'my_rooms': my_booked_rooms})
