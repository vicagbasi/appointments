from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^(?P<task_id>\d+)$', views.task, name='task'),
    url(r'^update', views.update, name='update'),
    url(r'^add', views.add, name='add'),
    url(r'^delete/(?P<task_id>\d+)', views.delete, name='delete')
]