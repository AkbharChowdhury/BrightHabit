from django.views.generic.base import ContextMixin

from blog.custom_tags import CustomTagsMixin
from blog.search_params import SearchParams

from BrightHabit.settings import APP_NAME


class Params(ContextMixin):
    def __init__(self, request):
        self.request = request

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_name'] = APP_NAME
        context['selected_tags'] = self.request.GET.getlist('tags')
        context['tag_colour'] = CustomTagsMixin.tag_colour()
        context['search_params'] = SearchParams(self.request).search_params()
        return context
