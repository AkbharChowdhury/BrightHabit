from blog.models import Post


class CustomSearch:
    is_Author = False

    def __init__(self, model: Post):
        self.model = model

    def search(self, query):
        pass

    @staticmethod
    def records_per_page():
        return 5
