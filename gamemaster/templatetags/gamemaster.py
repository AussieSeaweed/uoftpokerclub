from django.template import Library

register = Library()


@register.filter
def times(value):
    return range(value)
