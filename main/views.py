from django.shortcuts import render

def home(request):
    values = {'title': 'Главная страница', 'min_price': '1000', 'max_price': '10000'}
    return render(request, 'main/home.html', values)
