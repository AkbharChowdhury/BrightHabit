from abc import ABC

from django.contrib.auth.models import User


class CustomValidation(ABC):
    @staticmethod
    def email_exists(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    def email_exists_with_exclusion(email: str, excluded_email: str):
        return User.objects.filter(email=email).exclude(email=excluded_email).exists()

    @staticmethod
    def email_exists_error_message() -> str:
        return "Sorry, this email is already registered. Please use a different email"
