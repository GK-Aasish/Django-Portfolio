from django.db import models
import uuid


class ContactMessage(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField()

    subject = models.CharField(
        max_length=200,
        blank=True
    )

    message = models.TextField()

    # Unique token for each form submission
    submission_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_read = models.BooleanField(
        default=False
    )

    class Meta:

        ordering = ['-created_at']

    def __str__(self):

        return f"{self.name} - {self.subject or 'No Subject'}"