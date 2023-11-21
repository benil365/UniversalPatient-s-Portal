from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Hospital(models.Model):
    name = models.CharField(max_length=100)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, user_type=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        
        user = self.model(username=username, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, user_type, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, user_type, **extra_fields)


class CustomUser(AbstractUser):
    # Add any additional fields or methods you need for your custom user model
    user_type_choices = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    user_type = models.CharField(max_length=20, choices=user_type_choices)
    hospitals = models.ManyToManyField(Hospital, related_name='patients')
    # Add any other fields specific to hospitals or patients
    # For example, if hospitals have a 'hospital_name' field:
    hospital_name = models.CharField(max_length=100, blank=True, null=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    Username = models.CharField(max_length=50, unique=True, null=True, default='')
    Password = models.CharField(max_length=16, null=True)
    # Add hospital-specific fields



class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=False)
    Username = models.CharField(max_length=50, unique=True, null=True, default='')
    password = models.CharField(max_length=16, null=True)
    Hospital= models.CharField(max_length=20, null= True)
    identity= models.CharField(max_length= 10 , null= False, unique= True, default='', primary_key=True)
    # Add patient-specific fields

class DoctorData(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Add hospital data fields


class PatientData(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # Add patient data fields

# Create your models here.

