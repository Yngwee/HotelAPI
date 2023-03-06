from django.contrib import admin
from django.urls import path, include
from server.views import RegisterView, LoginView  # loginAPIView
import main.views
from rest_framework import routers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', main.views.auth, name='login'),
    path('registration/', main.views.registration, name='registration'),
    path('', main.views.home, name='home'),
    path('registration/register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),

]
