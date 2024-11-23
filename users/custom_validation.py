from abc import ABC
from django.contrib.auth.models import User


class CustomValidation(ABC):
    @staticmethod
    def email_exists(email):
        return User.objects.filter(email=email).exists()
