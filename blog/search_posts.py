from django.db.models import Q


class SearchPosts:

    def __init__(self, title: str, author_id: str):
        self.__title = title
        self.__author_id = author_id

    def __str__(self):
        return f'Title: {self.__title}, Author: {self.__author_id}'

    def full_text_search(self):
        title = self.__title
        return Q(title__icontains=title) | Q(body__icontains=title)

    def author_search(self):
        return Q(author=self.__author_id)