import os
from django import template

register = template.Library()

@register.filter(name='basename')
def basename(value):
    """Return the base filename from a file path or FieldFile object."""
    if not value:
        return ''
    try:
        # If it's a FieldFile, it will have 'name'
        name = getattr(value, 'name', value)
        return os.path.basename(name)
    except Exception:
        return str(value)
