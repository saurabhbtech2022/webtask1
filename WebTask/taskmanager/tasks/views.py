# tasks/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
import random

# View for OTP login
def otp_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = random.randint(100000, 999999)
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        request.session['otp'] = otp
        request.session['email'] = email
        return redirect('otp_verify')
    return render(request, 'tasks/otp_login.html')

# View for OTP verification
def otp_verify(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        if int(otp) == request.session['otp']:
            email = request.session['email']
            user = User.objects.get(email=email)
            login(request, user)
            return redirect('task_list')
        else:
            return redirect('otp_login')
    return render(request, 'tasks/otp_verify.html')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_edit(request, pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('task_list')

@login_required
def task_complete(request, pk):
    task = Task.objects.get(pk=pk)
    task.completed = True
    task.save()
    return redirect('task_list')

@login_required
def task_events(request):
    tasks = Task.objects.filter(user=request.user)
    events = []
    for task in tasks:
        events.append({
            'title': task.title,
            'start': task.scheduled_time.isoformat(),
            'end': task.scheduled_time.isoformat(),
        })
    return JsonResponse(events, safe=False)
