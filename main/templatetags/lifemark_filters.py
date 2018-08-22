from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def lifemark_field(id, name, value, label):
    if value:
        return mark_safe(f'<p>{label}: <span id="row_{id}_{name}">{value}</span></p>')
    return ''
