from .hooks import register_hook

@register_hook('before_save_fitnessentry')
def uppercase_title(entry):
    entry.title = entry.title.upper()

