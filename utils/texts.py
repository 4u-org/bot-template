from utils.translations import _, __

# _ is for general texts
# __ is for texts with pluralisation, use keyword {number} to automatically substitute number

# To get value use .value (texts.HELLO_WORLD.value)
# To get plural value use .value(number) (texts.HELLO_WORLD.value(5))

# In decorators use .lazy (F.text == texts.HELLO_WORLD.lazy)
# Don't use pluralisation in decorators, but if you do: F.text == texts.PLURAL.lazy(static_number)

class TranslationTexts:
    # Only singular
    HELLO_WORLD = _("Hello, world!")
    ERROR = _("Something went wrong...")
    # Singular and plural
    HELLO_WORLD_PLURALIZATION = __("Hello, {number} world!", "Hello, {number} worlds!")
    
texts = TranslationTexts