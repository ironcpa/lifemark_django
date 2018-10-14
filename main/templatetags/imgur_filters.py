from django import template

register = template.Library()


@register.filter
def to_imgur_thumbnail(big_image_url):
    if big_image_url.endswith('.jpg'):
        name_only = big_image_url[:big_image_url.index('.jpg')]
        return f'{name_only}s.jpg'

    return ''
