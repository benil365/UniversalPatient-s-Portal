from django.db import models
from django.contrib.auth.models import User
from user.models import Patient
from django.conf import settings



class MedicalRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    # Other fields for the medical record


# Create your models here.
class Hospital_user_Registration(models.Model):
    Name= models.CharField(max_length=50)
    Registration_number=models.CharField(max_length=16,null=False)
    Hospital_Email=models.EmailField()
    username=models.CharField(max_length=16, null=False, default='')
    Gender=models.CharField(max_length=12)
    Password=models.CharField(max_length=8)

    def __str__(self):
      return f"{self.Name}{self.Registration_number}{self.Hospital_Email}{self.Gender}{self.Password}"

class HospitalPatient_registration(models.Model):
    First_name = models.CharField(max_length=12, null=True)
    Second_name = models.CharField(max_length=12, null=True)
    Other_name = models.CharField(max_length=12, null=True)
    Identity_No = models.IntegerField(null= True)
    Date_of_birth = models.DateField(null=True, blank=True)
    Gender = models.CharField(max_length=16, null=True)
    Residence=models.CharField(max_length=50)
    email = models.EmailField(null=True, blank=True)
    Hospital = models.CharField(max_length=50, unique=True, null=True, default='')
    Username = models.CharField(max_length=12, null=True)
    Password = models.CharField(max_length=16, null=True)

    def __str__(self):
        return f"{self.Username} {self.Password}{self.First_name}{self.Second_name}{self.Other_name}{self.Identity_No}{self.Residence}"

class Patient_Medical_Record(models.Model):
    Date=models.DateTimeField()
    Symptoms=models.TextField(max_length=1200)
    Tests=models.TextField(max_length=550)
    Results=models.TextField(max_length=550)
    Diagnosis=models.CharField(max_length=100)
    Prescription=models.CharField(max_length=300)
    Recomendations=models.TextField(max_length=250)
    Image=models.ImageField(null=True)


    def __str__(self):
        return f"{self.Date}{self.Symptoms}{self.Tests}{self.Results}{self.Diagnosis}{self.Prescription}{self.Recomendations}"
