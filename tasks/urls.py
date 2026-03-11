from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:pk>/delete/', views.delete_task, name='delete_project'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('stats/', views.stats, name='stats'),
    path('profile/', views.profile, name='profile'),
    path('projects/<int:pk>/add_member/', views.add_member, name='add_member'),
]