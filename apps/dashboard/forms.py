from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        # These MUST match your model fields exactly
        fields = ['title', 'description', 'technologies', 'image', 'live_preview_url', 'source_code_url', 'date_completed', 'is_featured']
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Project Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe your work...', 'rows': 4}),
            'technologies': forms.TextInput(attrs={'placeholder': 'e.g. Django, React, PostgreSQL'}),
            'live_preview_url': forms.URLInput(attrs={'placeholder': 'https://...'}),
            'source_code_url': forms.URLInput(attrs={'placeholder': 'https://github.com/...'}),
            'date_completed': forms.DateInput(attrs={'type': 'date'}), # Makes a date picker appear
        }