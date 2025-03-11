from abc import ABC

from django.contrib.auth.models import User


class CustomValidation(ABC):
    @staticmethod
    def email_exists(email: str, excluded_email: str = None) -> bool:
        return User.objects.filter(email=email).exclude(email=excluded_email if excluded_email else '').exists()

    @staticmethod
    def email_exists_error_message() -> str:
        return "Sorry, this email is already registered. Please use a different email"
