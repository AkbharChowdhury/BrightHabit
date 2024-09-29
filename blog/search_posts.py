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

    # def search1(self):
    #     # return self.model.objects.filter(tags__contains='coding')
    #     # print(self.model.objects.filter(title__contains='Coding'))
    #
    #     # return self.model.objects.filter(Q(title__icontains='coding'))
    #     title = self.__title
    #     author = self.__author_id
    #     # article_filter = self.model.objects.filter
    #     author_id = str(Author.get_author(author).id) if author else None
    #     # search = SearchPosts(title=title, author=author_id, tags=self.__tags)
    #
    #     return self.model.objects.filter(
    #         self.full_text_search() |
    #         self.author_search() |
    #         self.tags_search()
    #     )
    #
    #     # return (
    #     #     self.model.objects.filter(Q(title__icontains=title) | Q(body__icontains=title))
    #     #     .filter(Q(author=self.__author_id))
    #     # )
    #
    #     # tags = self.model.objects.filter(tags__name__contains='coding')
    #     # tags = self.model.objects.filter(tags__name__in=self.__tags)
    #
    #     # if title and author:
    #     #     return article_filter(search.full_text_search() & search.author_search())
    #     # if author:
    #     #     return search.author_search()
    #     # if title:
    #     #     return article_filter(search.full_text_search())
