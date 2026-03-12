from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q


User = get_user_model()


class CustomAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(
                models.Q(username=username) |
                models.Q(email=username) |
                models.Q(phone=username)
            )
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

        return None