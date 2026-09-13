from django.urls import path
from . import views
from . import project_list_views

# Defines the custom dashboard namespace
app_name = 'dashboard'

urlpatterns = [
    path('', views.admin_dashboard, name='index'),
    path('projects/', project_list_views.project_list, name='project_list'),
    path('projects/create/', project_list_views.project_create, name='project_create'),
    path('projects/<int:project_id>/edit/', project_list_views.project_update, name='project_update'),
    path('projects/<int:project_id>/delete/', project_list_views.project_delete, name='project_delete'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
