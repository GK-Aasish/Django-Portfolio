import logging
from uuid import UUID

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from apps.dashboard.models import Project
from .models import ContactMessage

logger = logging.getLogger(__name__)


def index(request):
    return render(request, "core/index.html")


def projects(request):
    # Only show featured projects
    projects = Project.objects.filter(is_featured=True).order_by("-date_completed")
    return render(request, "core/projects.html", {"projects": projects})


def about(request):
    return render(request, "core/about.html")


def contact(request):
    if request.method != "POST":
        return render(request, "core/contact.html")

    data = {
        key: request.POST.get(key, "").strip()
        for key in ("name", "email", "subject", "message")
    }

    def fail(msg):
        # Keep what the visitor typed so they do not lose it
        return render(request, "core/contact.html", {"error": msg, "form_data": data})

    # Token check (stops double submit)
    try:
        token = UUID(request.POST.get("submission_token", ""))
    except (ValueError, TypeError):
        return fail("Invalid form submission. Please try again.")

    if ContactMessage.objects.filter(submission_token=token).exists():
        return redirect("contact_success")

    # Validation
    if not data["name"] or not data["email"] or not data["message"]:
        return fail("Please fill in all required fields.")
    if len(data["name"]) > 100 or len(data["subject"]) > 200:
        return fail("Name or subject is too long.")
    try:
        validate_email(data["email"])
    except ValidationError:
        return fail("Please enter a valid email address.")

    ContactMessage.objects.create(submission_token=token, **data)

    # Email is a bonus. Message is already saved, so never show a 500 if mail fails.
    try:
        send_mail(
            subject=f"Portfolio Contact: {data['subject'] or 'New Message'}",
            message=(
                "You received a new message from your portfolio.\n\n"
                f"Name: {data['name']}\n"
                f"Email: {data['email']}\n"
                f"Subject: {data['subject'] or 'No Subject'}\n\n"
                f"Message:\n\n{data['message']}\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )
    except Exception:
        logger.exception("Contact email failed to send")

    return redirect("contact_success")


def contact_success(request):
    return render(request, "core/contact_success.html")
