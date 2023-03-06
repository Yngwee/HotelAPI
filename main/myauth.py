from django.contrib.auth.backends import BaseBackend
from server.models import User

class AuthBackend(BaseBackend):
    @staticmethod
    def authenticate(request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                return user
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user(user_id, **kwargs):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
