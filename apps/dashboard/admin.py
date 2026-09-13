from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # Columns displayed in the project list view
    list_display = ('title', 'technologies', 'date_completed', 'is_featured', 'created_at')
    
    # Clickable links in the list view
    list_display_links = ('title',)
    
    # Enable filtering by these fields in the right sidebar
    list_filter = ('is_featured', 'date_completed')
    
    # Fields that can be searched using the search bar
    search_fields = ('title', 'description', 'technologies')
    
    # Automatically pre-populates the slug field as you type the title
    prepopulated_fields = {'slug': ('title',)}
    
    # Allows you to check/uncheck 'is_featured' directly from the list view
    list_editable = ('is_featured',)
