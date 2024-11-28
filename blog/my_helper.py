from abc import ABC

from django.utils.safestring import mark_safe


class MyHelper(ABC):
    @staticmethod
    def list_is_not_empty(lst):
        return list(filter(None, lst))

    @staticmethod
    def clean_text(text):
        return mark_safe(text.removeprefix('<pre>').removesuffix('</pre>'))
