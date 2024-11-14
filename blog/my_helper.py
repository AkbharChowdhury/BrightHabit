from abc import ABC


class MyHelper(ABC):
    @staticmethod
    def list_is_not_empty(lst):
        return list(filter(None, lst))
    # @staticmethod
