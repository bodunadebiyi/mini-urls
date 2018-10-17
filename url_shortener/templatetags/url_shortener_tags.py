from django import template
register = template.Library()

@register.filter(name='error_pipe')
def error_pipe(value):
    return 'danger' if value == 'error' else value

@register.filter(name='form_icon')
def form_icon(value):
    return 'fa fw fa-user' if value == 'username' else 'fa fw fa-lock'

@register.filter(name='form_type')
def form_type(value):
    return 'text' if value == 'username' else 'password'

@register.filter(name='form_placeholder')
def form_placeholder(value):
    if value == 'password1':
        return 'password'
    elif value == 'password2':
        return 'confirm password'
    else:
        return value