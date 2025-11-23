import re
from django import template

register = template.Library()

@register.filter(name='phone_whatsapp')
def phone_whatsapp(value, default_country='56'):
    """Return a normalized phone number suitable for WhatsApp links.

    Behavior:
    - Remove all non-digit characters.
    - If the cleaned number already starts with the default country code, return it as-is.
    - Else, if the cleaned number starts with '0', strip leading zeros then prepend default country code.
    - Else, if it starts with '9' (typical Chile mobile without country code), prepend default country code.
    - Otherwise, prepend default country code as a sensible fallback.

    This prevents duplicating the country code when templates also prepend it.
    """
    if not value:
        return ''
    s = re.sub(r'\D', '', str(value))
    if not s:
        return ''
    # If already has country code
    if s.startswith(default_country):
        return s
    # Strip leading zeros
    s_stripped = s.lstrip('0')
    if s_stripped.startswith('9'):
        return default_country + s_stripped
    # Fallback: if number length matches typical local (8-9), prepend country
    if 8 <= len(s_stripped) <= 12:
        return default_country + s_stripped
    # Otherwise return digits as-is
    return s
