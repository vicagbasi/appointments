from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserManager
# Create your views here.
def index(request):
    return render(request, 'login_app/index.html')

def register(request):
    errors = User.objects.validate_register(request.POST)
    print(errors)
    if type(errors) == list:
        for error in errors:
            messages.error(request, error)
        return redirect('/')
    else: 
        messages.success(request, "Successfully registered!")
    return redirect('/')
        

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) != list:
        print('========SUCCESS!=============')
        print(result)
        request.session['user_id'] = result.id
        print(request.session['user_id'])

        return redirect('appointments:dashboard')
    else:
        print('='*30)
        print(result)
        for err in result:
            messages.error(request, err)
        return redirect('/')


def logout(request):
    del request.session['user_id']
    request.session.modified = True
    return redirect('/')
    