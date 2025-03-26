
from django.db import models

class Story(models.Model):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('oncologist', 'Oncologist'),
        ('survivor', 'Survivor'),
    ]

    name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    story = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.get_role_display()}"
