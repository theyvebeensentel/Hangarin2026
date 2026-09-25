from django.urls import path
from . import views

urlpatterns = [
    # Task URLs
    path('', views.task_list, name='task_list'),
    path('add/', views.task_create, name='task_create'),
    path('edit/<int:pk>/', views.task_update, name='task_update'),
    path('delete/<int:pk>/', views.task_delete, name='task_delete'),

    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', views.category_update, name='category_update'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),

    # Priority URLs
    path('priorities/', views.priority_list, name='priority_list'),
    path('priorities/add/', views.priority_create, name='priority_create'),
    path('priorities/edit/<int:pk>/', views.priority_update, name='priority_update'),
    path('priorities/delete/<int:pk>/', views.priority_delete, name='priority_delete'),
]