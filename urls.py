from django.urls import path
from . import views

app_name = 'promane'

urlpatterns = [
    path('', views.IndexView, name='dashboard'),
    path('<uuid:prj_id>/', views.ProjectView, name='project_detail'),
    path('<uuid:prj_id>/middle/create/<str:title>/', views.MiddleCreateView, name='middle_create'),
    path('<uuid:prj_id>/task/create/<str:title>/', views.TaskCreateView, name='task_create'),
    path('<uuid:prj_id>/large/edit/<str:title>/', views.LargeEditView, name='large_edit'),
    path('<uuid:prj_id>/middle/edit/<str:title>/', views.MiddleEditView, name='middle_edit'),
    path('<uuid:prj_id>/task/edit/<str:title>/', views.TaskEditView, name='task_edit'),
    path('<uuid:prj_id>/task/start/<uuid:task_id>/', views.TaskStartView, name='task_start'),
    path('<uuid:prj_id>/task/finish/<uuid:task_id>/', views.TaskFinishView, name='task_finish'),
    path('<uuid:prj_id>/task/delete/<uuid:task_id>/', views.TaskDeleteView, name='task_delete'),
    path('<uuid:prj_id>/middle/delete/<uuid:middle_id>/', views.MiddleDeleteView, name='middle_delete'),
    path('<uuid:prj_id>/large/delete/<uuid:large_id>/', views.LargeDeleteView, name='large_delete'),
]
