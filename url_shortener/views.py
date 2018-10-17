import re
import uuid 
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Urls

def home(request):
    return render(request, 'url_shortener/home.html')

def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')

        if url_is_valid(original_url) is not True:
            messages.add_message(request, messages.ERROR, '{0} is not a valid URL'.format(original_url))
            return redirect('home')

        try:
            already_shortened_url = Urls.objects.get(original_url=original_url)
            success_message = generate_success_message(request, already_shortened_url.shortened_url)
        except ObjectDoesNotExist:
            model_payload = {}
            model_payload['original_url'] = original_url
            model_payload['shortened_url'] = get_shortened_url()
            model_payload['hits'] = 0

            if request.user.is_authenticated:
                model_payload['creator'] = request.user
            else:
                model_payload['creator'] = get_admin_user()

            new_model_record = Urls(**model_payload)    
            new_model_record.save()
            success_message = generate_success_message(request, new_model_record.shortened_url)
        finally:
            if success_message is not None:
                messages.add_message(request, 50, success_message)

            return redirect('home')

@login_required(login_url='login')       
def goto_dashboard(request):
    return render(request, 'url_shortener/dashboard.html')




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

def generate_success_message(request, url_code):
    shortened_url = 'https://' if request.is_secure() else 'http://'
    shortened_url +=  request.get_host() + '/' + url_code
    success_message = 'Your Url is ready: '
    success_message += '<em><a href="{0}">{1}</a></em>'.format(shortened_url, shortened_url)

    return success_message