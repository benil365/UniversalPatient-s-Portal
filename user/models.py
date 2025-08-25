from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser, BaseUserManager

class Hospital(models.Model):
    name = models.CharField(max_length=100)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, user_type, password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')

        user = self.model(username=username, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_doctor(self, username, reg_number, name, password=None, **extra_fields):
        return self.create_user(username, 'doctor', reg_number, name, password=password, **extra_fields)

    def create_patient(self, username, password=None, **extra_fields):
        return self.create_user(username, 'patient', password=password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.create_user(username, 'superuser', password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
    
class CustomUser(AbstractUser):
    # Add any additional fields or methods you need for your custom user model
    user_type_choices = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]
    user_type = models.CharField(max_length=20, choices=user_type_choices)
    hospitals = models.ManyToManyField(Hospital, related_name='patients')
    reg_number=models.CharField(max_length=20, null=True)
    name =models.CharField(max_length=100, null=True)
    user_id = models.IntegerField(null= True)
    hospital_name = models.CharField(max_length=100, blank=True, null=True)
    # Add any other fields specific to hospitals or patients
    # For example, if hospitals have a 'hospital_name' field:
    
    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    Username = models.CharField(max_length=50, unique=True, null=True, default='')
    Password = models.CharField(max_length=16, null=True)
    reg_number=models.CharField(max_length=20, null=True)
    name =models.CharField(max_length=100, null=True)
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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Add patient data fields

# Create your models here.

