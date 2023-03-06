from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
import main.views
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', main.views.auth, name='login'),
    path('registration/', main.views.registration, name='registration'),
    path('', main.views.home, name='home'),
    path('logout/', LogoutView.as_view, name='logout')
]
