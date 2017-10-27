from django.shortcuts import render, redirect
from django.contrib import messages
from apps.login_app.models import User, UserManager
from .models import Task, TaskManager
import datetime

# Create your views here.
def dashboard(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')

    print("=================User ID: {}=================".format(request.session['user_id']))
    current_user = request.session['user_id']
    now = datetime.datetime.now().strftime('%Y-%m-%d')

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'date': datetime.datetime.now().strftime('%B %d, %Y'),
        'today': User.objects.get(id=current_user).personal_tasks.filter(date=now).order_by('time'),
        'later_tasks': User.objects.get(id=current_user).personal_tasks.exclude(date=now).order_by('date')

    }
    return render(request, 'appointments_app/dashboard.html', context)

def task(request, task_id):
    print(type(Task.objects.get(id=task_id).date))
    print(type(Task.objects.get(id=task_id).time))
    date = Task.objects.get(id=task_id).date
    context = {
        'task': Task.objects.get(id=task_id),
        'date': ''
    }
    
    return render(request, 'appointments_app/task.html', context )

def update(request, task_id):
    user_id = request.session['user_id']
    
    valid = Task.objects.validate_update(request.POST, user_id, task_id)
    if type(valid) == list:
        print('='*30)
        print(valid)
        for err in valid:
            messages.error(request, err)
        return redirect('appointments:task', task_id=task_id)
    # 30 minute left and can't get an incorrect update to validate correctly sadly.
    else:
        return redirect('appointments:dashboard') 
        

def add(request):
    user_id = request.session['user_id']
    valid = Task.objects.validate_create(request.POST, user_id)
    return redirect('appointments:dashboard')

# def edit(request):
#     return render(request, 'appointments_app/task.html', context)

def delete(request, task_id):
    task = Task.objects.get(id=task_id)
    task.delete()
    return redirect('appointments:dashboard')


    
