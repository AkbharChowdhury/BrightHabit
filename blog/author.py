from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404


class Author:
    @staticmethod
    def get_author_by_username(username: str) -> User:
        return get_object_or_404(User, username=username)

    @staticmethod
    def get_author_by_id(author_id: str) -> Q:
        return Q(author=author_id)
        # return get_object_or_404(User, id=id)



