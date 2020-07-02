from django import template
from ..models import Cart

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

@register.simple_tag()
def get_cart(user):
    carts = Cart.objects.filter(user=user).select_related('user','item')
    return len(carts)


