class SearchParams:
    def __init__(self, request):
        self.request = request

    def search_params(self):
        default_value = ''
        return f'title={self.request.GET.get('title', default_value)}&tags={self.request.GET.get('tags', default_value)}'
