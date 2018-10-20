import re
import uuid 
from .models import Urls
from django.contrib.auth.models import User

def custom_url_is_valid(custom_url):
    response = {}
    regex = re.compile(r'^[a-zA-Z0-9_-]*$', re.IGNORECASE)

    if re.match(regex, custom_url) is None:
        response['passed'] = False
        response['err_message'] = 'Invalid Custom URL (The only special characters allowed are _ and -)'
    elif Urls.objects.filter(shortened_url=custom_url).count():
        response['passed'] = False
        response['err_message'] = 'This Custom URL already exists, please try another'
    else:
        response['passed'] = True

    return response

def get_greeting(current_hour):
    if current_hour < 12:
        return 'Good morning'
    elif 12 <= current_hour < 18:
        return 'Good Afternoon'
    else:
        return 'Good Evening'


def url_is_valid(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return re.match(regex, url) is not None

def get_admin_user():
    return User.objects.get(username='admin')

def get_shortened_url():
    shortened_url = uuid.uuid4().hex[:5].upper()

    if Urls.objects.filter(shortened_url=shortened_url).exists():
        get_shortened_url()
    else:
        return shortened_url.lower()

def get_full_url(request, url_code):
    shortened_url = 'https://' if request.is_secure() else 'http://'
    shortened_url +=  request.get_host() + '/' + url_code

    return shortened_url

def generate_success_message(request, url_code):
    shortened_url = get_full_url(request, url_code)
    success_message = 'Your Url is ready: '
    success_message += '<em><a href="{0}" target="_blank">{1}</a></em>'.format(shortened_url, shortened_url)

    return success_message