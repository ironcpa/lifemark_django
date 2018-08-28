from django import template
from django.utils.safestring import mark_safe

register = template.Library()

LIFEMARK_TD_CLASS_REF = 'bg-success'
LIFEMARK_TD_CLASS_TODO = 'bg-danger'
LIFEMARK_TD_CLASS_WORKING = 'bg-warning'
LIFEMARK_TD_CLASS_COMPLETE = 'bg-info'


@register.simple_tag
def lifemark_field(id, name, value, label):
    if value:
        return mark_safe(f'<p>{label}: <span id="row_{id}_{name}">{value}</span></p>')
    return ''


@register.filter
def td_class(lifemark):
    if lifemark.category == 'ref':
        return LIFEMARK_TD_CLASS_REF
    elif lifemark.state == 'todo':
        return LIFEMARK_TD_CLASS_TODO
    elif lifemark.state == 'working':
        return LIFEMARK_TD_CLASS_WORKING
    elif lifemark.state == 'complete':
        return LIFEMARK_TD_CLASS_COMPLETE

    return ''
