from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    # Add a CPF field (assuming CPF is a unique identifier)
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    
    # Add an image field for the user profile picture
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    # Enables the user access to the application
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.username

