from django.db.models import Q

from blog.models import Post


class SearchPosts:
    @staticmethod
    def records_per_page():
        return 5

    def __init__(self, title: str, author: str, tags: list[str] = None):
        self.model = Post
        self.__title = title
        self.__author_id = author
        self.__tags = tags if tags else []

    def __str__(self):
        return f'Title: {self.__title}, Author: {self.__author_id}, Tags: {self.__tags}'

    def __full_text_search(self):
        title = self.__title
        return Q(title__icontains=title) | Q(body__icontains=title)

    def __author_search(self):
        return Q(author=self.__author_id)

    def __tags_search(self):
        return Q(tags__name__in=self.__tags)

    def search(self):
        qs = self.model.objects.filter(self.__full_text_search() | self.__author_search())
        if self.__tags:
            qs = qs.filter(tags__name__in=self.__tags)
        return qs
