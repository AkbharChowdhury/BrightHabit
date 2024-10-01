class MyHelper:
    @staticmethod
    def list_is_not_empty(lst):
        return list(filter(None, lst))