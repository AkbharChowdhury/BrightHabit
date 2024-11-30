from abc import ABC

from django.utils.safestring import mark_safe


class MyHelper(ABC):
    @staticmethod
    def list_is_not_empty(lst) -> list:
        return list(filter(None, lst))

    @staticmethod
    def error_message() -> str:
        return "Whoops, something went wrong."

    @staticmethod
    def clean_text(text) -> mark_safe:
        return mark_safe(text.removeprefix('<pre>').removesuffix('</pre>'))
