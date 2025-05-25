from abc import ABC

from django.contrib.auth import get_user_model


class CustomValidation(ABC):
    @staticmethod
    def email_exists(email: str, excluded_email: str = None) -> bool:
        return get_user_model().objects.filter(email=email).exclude(
            email=excluded_email if excluded_email else '').exists()

    @staticmethod
    def email_exists_error_message() -> str:
        return "Sorry, this email is already registered. Please use a different email"
