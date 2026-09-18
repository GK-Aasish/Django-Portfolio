from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from .models import Project
from .forms import ProjectForm
from apps.core.models import ContactMessage


# =========================================================
# SECURITY
# =========================================================

def is_admin(user):
    """
    Allow access only to authenticated superusers.
    """
    return user.is_authenticated and user.is_superuser


# =========================================================
# LOGIN
# =========================================================

def login_view(request):
    """
    Custom admin login view.
    """

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard:index")

        else:

            return render(
                request,
                "dashboard/login.html",
                {
                    "error": "Invalid username or password."
                }
            )

    return render(request, "dashboard/login.html")


# =========================================================
# LOGOUT
# =========================================================

def logout_view(request):
    """
    Logout the current user and return to the homepage.
    """

    logout(request)

    return redirect("index")


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@user_passes_test(is_admin)
def admin_dashboard(request):
    """
    Main admin dashboard.
    """

    return render(
        request,
        "dashboard/admin.html"
    )


# =========================================================
# PROJECT LIST
# =========================================================

@user_passes_test(is_admin)
def project_list(request):
    """
    Display all projects.
    """

    projects = Project.objects.all()

    return render(
        request,
        "dashboard/project_list.html",
        {
            "projects": projects
        }
    )


# =========================================================
# CREATE PROJECT
# =========================================================

@user_passes_test(is_admin)
def project_create(request):
    """
    Create a new project.
    """

    if request.method == "POST":

        form = ProjectForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect(
                "dashboard:project_list"
            )

    else:

        form = ProjectForm()

    return render(
        request,
        "dashboard/project_form.html",
        {
            "form": form
        }
    )


# =========================================================
# UPDATE PROJECT
# =========================================================

@user_passes_test(is_admin)
def project_update(request, project_id):
    """
    Update an existing project.
    """

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if request.method == "POST":

        form = ProjectForm(
            request.POST,
            request.FILES,
            instance=project
        )

        if form.is_valid():

            form.save()

            return redirect(
                "dashboard:project_list"
            )

    else:

        form = ProjectForm(
            instance=project
        )

    return render(
        request,
        "dashboard/project_form.html",
        {
            "form": form,
            "project": project
        }
    )


# =========================================================
# DELETE PROJECT
# =========================================================

@user_passes_test(is_admin)
def project_delete(request, project_id):
    """
    Delete an existing project.
    """

    project = get_object_or_404(
        Project,
        id=project_id
    )

    if request.method == "POST":

        project.delete()

        messages.success(
            request,
            "Project deleted successfully."
        )

        return redirect(
            "dashboard:project_list"
        )

    return render(
        request,
        "dashboard/delete_confirm.html",
        {
            "project": project
        }
    )


# =========================================================
# MESSAGE INBOX
# =========================================================

@user_passes_test(is_admin)
def message_inbox(request):
    """
    Display contact messages.

    The left side contains the inbox.
    The right side displays the selected message.
    """

    all_messages = ContactMessage.objects.all()

    selected_message = None

    message_id = request.GET.get("message")

    if message_id:

        selected_message = get_object_or_404(
            ContactMessage,
            id=message_id
        )

        # Mark the message as read
        if not selected_message.is_read:

            selected_message.is_read = True

            selected_message.save(
                update_fields=["is_read"]
            )

    return render(
        request,
        "dashboard/messages.html",
        {
            "messages": all_messages,
            "selected_message": selected_message,
        }
    )


# =========================================================
# DELETE MESSAGE
# =========================================================

@user_passes_test(is_admin)
def message_delete(request, message_id):
    """
    Delete a contact message.
    """

    message = get_object_or_404(
        ContactMessage,
        id=message_id
    )

    if request.method == "POST":

        message.delete()

        messages.success(
            request,
            "Message deleted successfully."
        )

        return redirect(
            "dashboard:messages"
        )

    return redirect(
        "dashboard:messages"
    )