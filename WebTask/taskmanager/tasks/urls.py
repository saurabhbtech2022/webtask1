# tasks/urls.py

from django.urls import path
from .views import task_list, task_create, task_edit, task_delete, task_complete, task_events, otp_login, otp_verify

urlpatterns = [
    path('', task_list, name='task_list'),
    path('create/', task_create, name='task_create'),
    path('edit/<int:pk>/', task_edit, name='task_edit'),
    path('delete/<int:pk>/', task_delete, name='task_delete'),
    path('complete/<int:pk>/', task_complete, name='task_complete'),
    path('events/', task_events, name='task_events'),
    path('otp_login/', otp_login, name='otp_login'),
    path('otp_verify/', otp_verify, name='otp_verify'),
]
