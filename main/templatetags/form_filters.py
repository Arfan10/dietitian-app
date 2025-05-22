from django import template
from django.utils.html import format_html

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    return field.as_widget(attrs={"class": css_class})


@register.filter(name='add_attrs')
def add_attrs(field, attr_string):
    """
    Usage: {{ field|add_attrs:"class=input-field,id=date,placeholder=Pick a date" }}
    """
    attrs = {}
    for attr in attr_string.split(","):
        key, val = attr.split("=")
        attrs[key.strip()] = val.strip()
    return field.as_widget(attrs=attrs)
