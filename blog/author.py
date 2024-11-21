from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class Author:
    @staticmethod
    def get_author_by_username(username: str) -> User:
        return get_object_or_404(User, username=username)
