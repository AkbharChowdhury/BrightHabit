from django.db.models import Q

from blog.author import Author
from blog.models import Post


class SearchPosts:
    @staticmethod
    def records_per_page():
        return 5

    def __init__(self, title: str, author: str):
        self.model = Post
        self.__title = title
        self.__author_id = author

    def __str__(self):
        return f'Title: {self.__title}, Author: {self.__author_id}'

    def full_text_search(self):
        title = self.__title
        return Q(title__icontains=title) | Q(body__icontains=title)

    def author_search(self):
        return Q(author=self.__author_id)

    def search(self):


        # return self.model.objects.filter(tags__contains='coding')
        # print(self.model.objects.filter(title__contains='Coding'))

        # return self.model.objects.filter(Q(title__icontains='coding'))
        title = self.__title
        author = self.__author_id
        article_filter = self.model.objects.filter
        author_id = str(Author.get_author(author).id) if author else None
        search = SearchPosts(title=title, author=author_id)

        # tags = self.model.objects.filter(tags__name__contains='coding')
        if title and author:
            return article_filter(search.full_text_search() & search.author_search())
        if author:
            return search.author_search()
        if title:
            return article_filter(search.full_text_search())
