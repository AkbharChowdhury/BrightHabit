import json


class HttpRequest:
    def __init__(self, request):
        self.request = request

    def __is_fetch_request(self):
        return self.request.headers.get('X-Csrftoken') is not None

    def __is_ajax(self):
        return self.request.headers.get('x-requested-with') == 'XMLHttpRequest'

    def is_http_request(self):
        return self.__is_fetch_request() or self.__is_ajax()

    def get_post_id(self, post_id):
        return self.request.POST.get(post_id) or json.loads(self.request.body.decode('utf-8'))[post_id]
