from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Project

# Security function: Returns True only if the user is an admin/superuser
def login_view(request):
    """ Custom login view to redirect users after logging in """
    from django.contrib.auth import authenticate, login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to the dashboard index page after successful login
            return redirect('dashboard:index')  # Redirects to the dashboard index page after login
        else:
            # Invalid login credentials
            return render(request, 'dashboard/login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'dashboard/login.html')
    
def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'dashboard/admin.html')

def logout_view(request):
    """ Custom logout view to redirect users after logging out """
    from django.contrib.auth import logout
    logout(request)
    # Return to the apps.core index page after logout
    return redirect('index')  # Redirects to the core index page after logout