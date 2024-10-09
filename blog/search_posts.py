from django.db.models import Q

from blog.author import Author
from blog.models import Post
from blog.my_helper import MyHelper


class SearchPosts:
    @staticmethod
    def records_per_page():
        return 5

    def __init__(self, title: str, author: str, tags: list[str] = None,
                 ):
        self.model = Post
        self.__title = title
        self.__author = author
        self.__tags = tags

    def __str__(self):
        return f'Title: {self.__title}, Author: {self.__author}, Tags: {self.__tags}'

    @staticmethod
    def full_text_search(title):
        return Q(title__icontains=title)

    def __author_search(self):
        return Author.get_author_by_id(self.__author)

    @staticmethod
    def tags_search(tags):
        return Q(tags__name__in=tags)

    def search(self):
        qs = self.model.objects.filter(SearchPosts.full_text_search(self.__title) | self.__author_search())
        if MyHelper.list_is_not_empty(self.__tags):
            qs = qs.filter(tags__name__in=self.__tags)
        return qs
