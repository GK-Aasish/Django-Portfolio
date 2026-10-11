from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from apps.core.models import ContactMessage
from .forms import ProjectForm
from .models import Project


def is_admin(user):
    """Only authenticated superusers."""
    return user.is_authenticated and user.is_superuser


# ---------------- AUTH ----------------

def login_view(request):
    next_url = request.POST.get("next") or request.GET.get("next", "")

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password"),
        )

        if user is not None and user.is_superuser:
            login(request, user)
            if next_url and url_has_allowed_host_and_scheme(
                next_url, allowed_hosts={request.get_host()}
            ):
                return redirect(next_url)
            return redirect("dashboard:index")

        return render(
            request,
            "dashboard/login.html",
            {"error": "Invalid username or password.", "next": next_url},
        )

    return render(request, "dashboard/login.html", {"next": next_url})


def logout_view(request):
    logout(request)
    return redirect("index")


# ---------------- DASHBOARD ----------------

@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        "project_count": Project.objects.count(),
        "featured_count": Project.objects.filter(is_featured=True).count(),
        "message_count": ContactMessage.objects.count(),
        "unread_count": ContactMessage.objects.filter(is_read=False).count(),
        "recent_messages": ContactMessage.objects.all()[:5],
        "recent_projects": Project.objects.order_by("-created_at")[:5],
    }
    return render(request, "dashboard/admin.html", context)


# ---------------- PROJECTS ----------------

@user_passes_test(is_admin)
def project_list(request):
    projects = Project.objects.order_by("-created_at")
    return render(request, "dashboard/project_list.html", {"projects": projects})


@user_passes_test(is_admin)
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Project created successfully.")
            return redirect("dashboard:project_list")
    else:
        form = ProjectForm()

    return render(request, "dashboard/project_form.html", {"form": form})


@user_passes_test(is_admin)
def project_update(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully.")
            return redirect("dashboard:project_list")
    else:
        form = ProjectForm(instance=project)

    return render(
        request, "dashboard/project_form.html", {"form": form, "project": project}
    )


@user_passes_test(is_admin)
def project_delete(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project deleted successfully.")
        return redirect("dashboard:project_list")

    return render(request, "dashboard/delete_confirm.html", {"project": project})


# ---------------- MESSAGES ----------------

@user_passes_test(is_admin)
def message_inbox(request):
    all_messages = ContactMessage.objects.all()
    selected_message = None

    message_id = request.GET.get("message", "")

    # isdigit() stops ?message=abc from crashing the page
    if message_id.isdigit():
        selected_message = get_object_or_404(ContactMessage, id=int(message_id))

        if not selected_message.is_read:
            selected_message.is_read = True
            selected_message.save(update_fields=["is_read"])

    return render(
        request,
        "dashboard/messages.html",
        {"messages": all_messages, "selected_message": selected_message},
    )


@user_passes_test(is_admin)
def message_delete(request, message_id):
    message = get_object_or_404(ContactMessage, id=message_id)

    if request.method == "POST":
        message.delete()
        messages.success(request, "Message deleted successfully.")

    return redirect("dashboard:messages")
