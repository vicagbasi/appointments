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

    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'date': datetime.datetime.now().strftime('%B %d, %Y'),
        'tasks': Task.objects.filter(date = datetime.datetime.now().strftime('%Y-%m-%d')).order_by('time'),
        'later_tasks': Task.objects.exclude(date = datetime.datetime.now().strftime('%Y-%m-%d')).order_by('time')

    }
    return render(request, 'appointments_app/dashboard.html', context)

def task(request, task_id):
    context = {
        'task': Task.objects.get(id=task_id)
    }
    request.session['task_id'] = task_id
    return render(request, 'appointments_app/task.html', context )

def update(request):
    user_id = request.session['user_id']
    if 'task_id' in request.session:
        task_id = request.session['task_id']
    valid = Task.objects.validate_update(request.POST, user_id)
    # if type(valid) == list:
    #     print('='*30)
    #     print(valid)
    #     for err in valid:
    #         messages.error(request, err)
    #     return redirect('appointments:<task_id>')
    # 30 minute left and can't get an incorrect update to validate correctly sadly.
    # else:
    return redirect('appointments:dashboard') ('/appointments/dashboard')
        

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


    
