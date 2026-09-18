from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from uuid import UUID

from apps.dashboard.models import Project
from .models import ContactMessage


def index(request):
    return render( request,'core/index.html')

def projects(request):

    # Only show featured projects
    projects = Project.objects.filter(is_featured=True)

    return render(request,'core/projects.html',{'projects': projects})

def about(request):
    return render(request,'core/about.html')

def contact(request):
    if request.method == "POST":
        # -------------------------------------------------
        # GET FORM DATA
        # -------------------------------------------------
        name = request.POST.get("name","").strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        subject = request.POST.get(
            "subject",
            ""
        ).strip()

        message = request.POST.get(
            "message",
            ""
        ).strip()

        submission_token = request.POST.get(
            "submission_token"
        )


        # -------------------------------------------------
        # VALIDATE SUBMISSION TOKEN
        # -------------------------------------------------

        if not submission_token:

            return render(
                request,
                "core/contact.html",
                {
                    "error": "Invalid form submission. Please try again."
                }
            )


        try:

            token = UUID(submission_token)

        except (ValueError, TypeError):

            return render(
                request,
                "core/contact.html",
                {
                    "error": "Invalid form submission. Please try again."
                }
            )


        # -------------------------------------------------
        # CHECK IF THIS EXACT SUBMISSION WAS ALREADY PROCESSED
        # -------------------------------------------------

        if ContactMessage.objects.filter(
            submission_token=token
        ).exists():

            return redirect(
                "contact_success"
            )


        # -------------------------------------------------
        # BASIC VALIDATION
        # -------------------------------------------------

        if not name or not email or not message:

            return render(
                request,
                "core/contact.html",
                {
                    "error": "Please fill in all required fields."
                }
            )


        # -------------------------------------------------
        # SAVE MESSAGE
        # -------------------------------------------------

        ContactMessage.objects.create(

            name=name,

            email=email,

            subject=subject,

            message=message,

            submission_token=token

        )


        # -------------------------------------------------
        # SEND EMAIL NOTIFICATION
        # -------------------------------------------------

        send_mail(

            subject=(
                f"Portfolio Contact: "
                f"{subject or 'New Message'}"
            ),

            message=f"""
            You received a new message from your portfolio.

            Name: {name}
            Email: {email}
            Subject: {subject or 'No Subject'}

            Message:

            {message}
            """,

            from_email=settings.DEFAULT_FROM_EMAIL,

            recipient_list=[
                settings.CONTACT_EMAIL
            ],

            fail_silently=False,

        )


        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        return redirect(
            "contact_success"
        )


    return render(
        request,
        "core/contact.html"
    )


def contact_success(request):

    return render(
        request,
        "core/contact_success.html"
    )