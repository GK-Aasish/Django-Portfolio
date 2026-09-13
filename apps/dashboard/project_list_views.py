from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from .forms import ProjectForm
from .models import Project

# Security function: Returns True only if the user is an admin/superuser
def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def project_list(request):
    """ View to list all projects """
    projects = Project.objects.all()
    return render(request, 'dashboard/project_list.html', {'projects': projects})

def project_create(request):
    """ View to create a new project """
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard:project_list')
    else:
        form = ProjectForm()
    return render(request, 'dashboard/project_form.html', {'form': form})

def project_update(request, project_id):
    """ View to update an existing project """
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('dashboard:project_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'dashboard/project_form.html', {'form': form, 'project': project})

def project_delete(request, project_id):
    """ View to delete an existing project """
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        project.delete()
        return redirect('dashboard:project_list')
    return render(request, 'dashboard/project_delete_confirm.html', {'project': project})