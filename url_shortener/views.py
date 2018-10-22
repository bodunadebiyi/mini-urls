from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Urls
from .helpers import custom_url_is_valid, get_greeting, url_is_valid, get_admin_user, get_shortened_url, get_full_url, generate_success_message, username_is_valid

def home(request):
    return render(request, 'url_shortener/home.html')

def shorten_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')

        if url_is_valid(original_url) is not True:
            messages.add_message(request, messages.ERROR, '{0} is not a valid URL'.format(original_url))
            return redirect('home')

        success_message = process_url_to_shorten(request, original_url)

        if success_message is not None:
            messages.add_message(request, 50, success_message)

    return redirect('home')

def process_url_to_shorten(request, original_url):
    success_message = None
    try:
        already_shortened_url = Urls.objects.filter(original_url=original_url, is_custom=False).first()
        success_message = generate_success_message(request, already_shortened_url.shortened_url)
    except ObjectDoesNotExist:
        model_payload = {}
        model_payload['original_url'] = original_url
        model_payload['shortened_url'] = get_shortened_url()
        model_payload['hits'] = 0

        model_payload['creator'] = request.user if request.user.is_authenticated else get_admin_user()

        new_model_record = Urls(**model_payload)    
        new_model_record.save()
        success_message = generate_success_message(request, new_model_record.shortened_url)

    return success_message

def redirect_to_original_url(request, slug):
    try:
        if slug == 'admin':
            return redirect('admin/')
        original_url_record = Urls.objects.get(shortened_url=slug)
        original_url_record.hits = original_url_record.hits + 1
        original_url_record.save()

        return redirect(original_url_record.original_url)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, "{0} is not a valid shortened url".format(get_full_url(request, slug)))
        return redirect('home')

def register(request):
    if request.user.is_authenticated:
        return redirect('goto_dashboard')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('goto_dashboard')
    else:
        form = UserCreationForm()

    return render(request, 'url_shortener/register.html', { 'form': form })

@login_required(login_url='login')
def shorten_customized_url(request):
    if not request.method == 'POST':
        return redirect('home')

    original_url = request.POST.get('original_url')
    customized_url = request.POST.get('custom_url')

    if not original_url or not url_is_valid(original_url):
        messages.add_message(request, messages.ERROR, 'Your URL is invalid')
        return redirect('goto_dashboard')

    if not customized_url or not customized_url.strip():
        success_message = process_url_to_shorten(request, original_url)
        messages.add_message(request, 50, success_message)
        return redirect('goto_dashboard')

    custom_url_validity = custom_url_is_valid(customized_url)

    if not custom_url_validity['passed']:
        messages.add_message(request, messages.ERROR, custom_url_validity['err_message'])
    else:
        shortened_url = Urls(
            original_url=original_url,
            shortened_url=customized_url,
            creator=request.user,
            hits=0
        )
        shortened_url.save()
        messages.add_message(request, 50, generate_success_message(request, customized_url))

    return redirect('goto_dashboard')

@login_required(login_url='login')       
def goto_dashboard(request):
    greeting = get_greeting(datetime.now().hour)
    urls = request.user.created_urls.all()
    full_url = 'https://' if request.is_secure() else 'http://'
    full_url += request.get_host() + '/'
    view_context = {
        'greeting': greeting,
        'urls': urls,
        'full_url': full_url
    }

    return render(request, 'url_shortener/dashboard.html', view_context)

@login_required(login_url='login')
def update_username(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        username_validation = username_is_valid(username)

        if username_validation['passed']:
            request.user.username = username
            request.user.save()
            messages.add_message(request, messages.SUCCESS, 'username updated')
        else:
            messages.add_message(request, messages.ERROR, username_validation['err_message'])

    return redirect('goto_dashboard')

@login_required(login_url='login')
def update_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not password == confirm_password:
            messages.add_message(request, messages.ERROR, 'passwords do not match!')
        else:
            try:
                validate_password(password, request.user)
                messages.add_message(request, messages.SUCCESS, 'password updated!')
                request.user.set_password(password)
            except ValidationError as err:
                for err_message in err.messages:
                    messages.add_message(request, messages.ERROR, err_message)

    return redirect('goto_dashboard')

@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        try:
            user.created_urls.all().delete()
            user.delete()
            messages.add_message(request, messages.SUCCESS, 'Account Successfully Delete!')
        except Exception:
            messages.add_message(request, messages.ERROR, 'Something went wrong!')
            
    return redirect('home')