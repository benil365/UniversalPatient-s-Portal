from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_patient= models.BooleanField(default=False)
    is_doctor=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_patient:
            self.is_doctor=False
        elif self.is_doctor:
           self.is_patient=False
        super().save(*args, **kwargs)