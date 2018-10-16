from django import template
register = template.Library()

@register.filter(name='error_pipe')
def error_pipe(value):
    return 'danger' if value == 'error' else value