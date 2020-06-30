from django import template

register = template.Library()

@register.simple_tag
def cart(value, val1, val2):
    """Removes all values of arg from the given string"""
    return value + val1 * len(val2)

@register.simple_tag
def adder(val1,val2):
    return val1 + val2

@register.simple_tag
def multiplier(val1,val2):
    return val1 * val2

@register.simple_tag
def length(items):
    return len(items)
