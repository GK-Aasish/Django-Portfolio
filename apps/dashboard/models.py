from django.db import models
from django.utils.text import slugify # Import this to turn titles into slugs

class Project(models.Model):
    title = models.CharField(max_length=200)
    # We keep unique=True to protect your SEO/URLs
    slug = models.SlugField(max_length=250, unique=True) 
    description = models.TextField()
    technologies = models.CharField(max_length=250)
    image = models.ImageField(upload_to='portfolio_projects/', blank=True, null=True)
    live_preview_url = models.URLField(blank=True, null=True)
    source_code_url = models.URLField(blank=True, null=True)
    date_completed = models.DateField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_tags_list(self):
        if self.technologies:
            return [tag.strip() for tag in self.technologies.split(',')]
        return []

    def __str__(self):
        return self.title

    # --- THE MAGIC FIX ---
    def save(self, *args, **kwargs):
        # 1. Automatically generate the slug from the title if it's empty
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            
            # 2. PREVENT DUPLICATES: Check if slug exists, if so, add a number (e.1, e.2...)
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
            
        super().save(*args, **kwargs)