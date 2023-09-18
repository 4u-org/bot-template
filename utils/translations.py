from babel.support import LazyProxy
from aiogram.utils.i18n import gettext

from middlewares import i18n

class TranslatableText():
    def __init__(self, text: str):
        self.text = text
    def get_value(self, locale: str = None) -> str:
        """Get translated value"""
        if locale:
            return i18n.i18n.gettext(self.text, locale=locale)
        return self.value
    @property
    def value(self) -> str:
        """Get translated value"""
        return gettext(self.text)
    @property
    def lazy(self) -> LazyProxy:
        """Lazy proxy for decorators and filters"""
        return LazyProxy(gettext, self.text, enable_cache=False)
    def __str__(self):
        return self.value
    
def _(text: str) -> TranslatableText:
    return TranslatableText(text)
    
class TranslatableTextPlural():
    def __init__(self, text: str, text_plural: str):
        self.text = text
        self.text_plural = text_plural

    def get_value(self, number: int, locale: str = None) -> str:
        """Get translated value"""
        if locale:
            return i18n.i18n.gettext(self.text, self.text_plural, number, locale)
        return self.value(number)
    def value(self, number: int) -> str:
        """Formats translated text using provided number"""
        return gettext(self.text, self.text_plural, number).format(number=number)
    
    def lazy(self, number: int) -> LazyProxy:
        """Lazy proxy for decorators and filters"""
        return LazyProxy(self.value, number, enable_cache=False)
        
def __(text: str, text_plural: str) -> TranslatableTextPlural:
    """
    Use keyword number to automatically substitude number
    """
    return TranslatableTextPlural(text, text_plural)