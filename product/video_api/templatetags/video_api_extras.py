from django import template

register = template.Library()

@register.filter
def sec_to_min(value):
    try:
        return int(value/60)
    except (ValueError, ZeroDivisionError):
        return None

