from django.shortcuts import render

from apps.dashboard.models import Project

def index(request):
    return render(request, 'core/index.html')

def projects(request):
    # Only show the projects that are marked as is_featured in the database
    projects = Project.objects.filter(is_featured=True)
    return render(request, 'core/projects.html', {'projects': projects})

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')