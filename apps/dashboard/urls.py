from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [

    # Authentication
    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # Dashboard
    path(
        "",
        views.admin_dashboard,
        name="index"
    ),

    # Projects
    path(
        "projects/",
        views.project_list,
        name="project_list"
    ),

    path(
        "projects/create/",
        views.project_create,
        name="project_create"
    ),

    path(
        "projects/<int:project_id>/edit/",
        views.project_update,
        name="project_update"
    ),

    path(
        "projects/<int:project_id>/delete/",
        views.project_delete,
        name="project_delete"
    ),

    # Messages
    path(
        "messages/",
        views.message_inbox,
        name="messages"
    ),

    path(
        "messages/<int:message_id>/delete/",
        views.message_delete,
        name="message_delete"
    ),
]