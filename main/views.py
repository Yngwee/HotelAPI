from django.shortcuts import render
from django.db.models import Q
from server.models import Room


def auth(request):
    return render(request, 'login/login.html', {'title': 'Авторизация'})


def registration(request):
    return render(request, 'login/registration.html', {'title': 'Регистрация'})


def home(request):
    price_from = request.GET.get('price_filter_from')
    price_to = request.GET.get('price_filter_to')
    capacity = request.GET.getlist('cap')
    capacity_objects = Q()
    for c in capacity:
        capacity_objects |= Q(capacity=c)
    sort_by = request.GET.get('sort')

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
              'sort': sort_by, 'rooms': rooms, 'num_rooms': len(rooms), 'title': 'Главная страница'}

    request.session['save_session'] = list(rooms.values())
    return render(request, 'main/home.html', params)
