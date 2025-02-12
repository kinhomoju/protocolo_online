from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    """
    Adiciona uma classe CSS a um campo de formulário.
    """
    if hasattr(value, 'as_widget'):  # Verifica se o campo é um campo de formulário
        return value.as_widget(attrs={"class": css_class})
    return value  # Caso contrário, retorna o valor sem alteração
