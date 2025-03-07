from django import template
from django.forms import BoundField

register = template.Library()

@register.filter(name='add_attr')
def add_attr(field, attrs):
    if isinstance(field, BoundField):
        attrs_dict = {}
        for attr in attrs.split(","):
            parts = attr.split(":", 1)  # Garante apenas uma divisão no primeiro ':'
            if len(parts) == 2:
                key, value = parts
                attrs_dict[key.strip()] = value.strip()
        return field.as_widget(attrs=attrs_dict)
    return field
