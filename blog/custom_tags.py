from django.db.models import QuerySet, Q
from django.views.generic.base import ContextMixin
from blog.author import Author
from blog.models import Post, Tag


class CustomTagsMixin(ContextMixin):
    def __min_num_tags(self):
        return 3

    @staticmethod
    def tag_colour():
        return 'secondary'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['username'] = username

        if username:
            author_username = Q(author=Author.get_author_by_username(username))
            context['tags'] = Tag.objects.filter(Q(tags__in=Post.objects.filter(author_username))).distinct()
            return context
        context['tags'] = self.__toggle_tags(show_all_tags='show_all_tags' in self.request.GET)
        return context

    def __toggle_tags(self, show_all_tags: bool = False) -> QuerySet[Tag]:
        tags: QuerySet[Tag] = Tag.objects.filter(Q(tags__in=Post.objects.all())).distinct()
        return tags if show_all_tags else tags[:self.__min_num_tags()]

