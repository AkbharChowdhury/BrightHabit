import json


class HTTP_JS:
    def __init__(self, request):
        self.request = request

    def is_fetch_request(self):
        return self.request.headers.get('X-Csrftoken') is not None

    def is_ajax(self):
        return self.request.headers.get('x-requested-with') == 'XMLHttpRequest'

    def get_id_form_data(self, id):
        return json.loads(self.request.body.decode('utf-8'))[id]
