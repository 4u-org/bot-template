from enum import Enum
from functools import partial

from babel.support import LazyProxy
from aiogram.utils.i18n import gettext

class TranslatableText():
    def __init__(self, text: str):
        self.text = text
    @property
    def value(self) -> str:
        """Get translated value"""
        return gettext(self.text)
    @property
    def lazy(self) -> LazyProxy:
        """Lazy proxy for decorators and filters"""
        return LazyProxy(gettext, self.text)
    def __str__(self):
        return self.value
    
def _(text: str) -> TranslatableText:
    return TranslatableText(text)
    
class TranslatableTextPlural():
    def __init__(self, text: str, text_plural: str):
        self.text = text
        self.text_plural = text_plural

    def value(self, number: int) -> str:
        """Formats translated text using provided number"""
        return gettext(self.text, self.text_plural, number).format(number=number)
    
    def lazy(self, number: int) -> LazyProxy:
        """Lazy proxy for decorators and filters"""
        return LazyProxy(self.value, number)
        
def __(text: str, text_plural: str) -> TranslatableTextPlural:
    """
    Use keyword number to automatically substitude number
    """
    return TranslatableTextPlural(text, text_plural)