from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login as auth_login
from django.http import HttpResponseRedirect,HttpResponse
from .forms import UserRegistrationForm
from django.utils.html import escape


def login(request):
    message = 'Enter your username and password'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                message = 'Your account is not activated'
        else:
            message = 'Invalid login, please try again.'
    context = {'message': message}
    return render(request, 'accounts/login.html', context)


def register(request):
    user_form = UserRegistrationForm(request.POST)
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #HttpResponse("i mam in ja")
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'accounts/register_done.html')
    return render(request, 'accounts/signup.html', {'form':user_form})
