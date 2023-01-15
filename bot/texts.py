from typing import Union, Callable
from aiogram.utils.i18n import gettext, lazy_gettext

def _(text: str):
    def getargstranslation(**kwargs):
        return gettext(text).format(**kwargs)
    return getargstranslation
    
def __(text:str, text_plural: str):
    """
    Use keyword number to automatically substitude number
    """
    def getnumtranslation(number: int):
        return gettext(text, text_plural, number).format(number=number)
    return getnumtranslation

class TranslationTexts:
    HELLO_WORLD = _("Hello, world!")
    HELLO_WORLD_PLURALIZATION = __("Hello, {number} world!", "Hello, {number} worlds!")
    HELLO_WORLD_PARAMS = _("{hello_text}, world!")
    HELLO_WORLD_PARAMS_PLURALIZATION = _("{hello_text}, {worlds_plural}!")
    WORLDS_PLURAL = __("{number} world", "{number} worlds!")