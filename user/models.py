from django.db import models

# User model for the application
class User(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.last_name}"

    # Minimal auth interface so DRF's IsAuthenticated and others work
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
