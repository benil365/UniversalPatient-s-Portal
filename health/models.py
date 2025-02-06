from django.db import models ,migrations
from django.contrib.auth import get_user_model
User= get_user_model()
from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import CustomUser
from django.conf import settings

class PatientUpload(models.Model):
    Identity_No = models.PositiveIntegerField(null=True)
    email = models.CharField(max_length=50)
    hospital = models.TextField()
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return f"{self.Identity_No} {self.email} {self.hospital}{self.file}"


class Doctor_registration(models.Model):
    CHOICE1 = (('public', 'Public'), ('private', 'Private'))
    name = models.CharField(max_length=100)
    reg_number=models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=15, default='')
    category = models.CharField(max_length=10, choices=CHOICE1)

    def __str__(self):
        return f"{self.name}{self.reg_number} {self.email} {self.category}"


class HospitalUpload(models.Model):
    name = models.CharField(max_length=100)
    Patient_Id = models.CharField(max_length=50)
    category = models.TextField()
    file = models.FileField(upload_to='uploads/')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return f"{self.name} {self.Patient_Id} {self.category}{self.file}"


class Patient_registration(models.Model):
    First_name = models.CharField(max_length=12, null=True)
    Second_name = models.CharField(max_length=12, null=True)
    Other_name = models.CharField(max_length=12, null=True)
    Identity_No = models.IntegerField(null= True)
    Date_of_birth = models.DateField(null=True, blank=True)
    Gender = models.CharField(max_length=16, null=True)
    email = models.EmailField(null=True, blank=True)
    Hospital = models.CharField(max_length=50, unique=True, null=True, default='')
    Username = models.CharField(max_length=12, null=True)
    Password = models.CharField(max_length=16, null=True)

    def __str__(self):
        return f"{self.Username} {self.Password}{self.First_name}{self.Second_name}{self.Other_name}{self.Identity_No}{self.Residence}"
def set_default_user(apps, schema_editor):
    HospitalUpload = apps.get_model('health', 'HospitalUpload')
    User = get_user_model()
    for upload in HospitalUpload.objects.all():
        upload.user = User.objects.first()  
        upload.save()

class Migration(migrations.Migration):

    dependencies = [
        # Your dependencies
    ]

    operations = [
        migrations.AddField(
            model_name='hospitalupload',
            name='user',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE),
            preserve_default=False,
        ),
    ]

    def set_default_user(apps, schema_editor):
        HospitalUpload = apps.get_model('health', 'HospitalUpload')
        User = get_user_model()
        for upload in HospitalUpload.objects.all():
            upload.user = User.objects.first()  # Replace with your desired logic
            upload.save()

    migrations.RunPython(set_default_user),
class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

@receiver(post_save, sender=Patient_registration)
@receiver(post_save, sender=Doctor_registration)
def create_or_update_user(sender, instance, created, **kwargs):
    if created:
        if isinstance(instance, Patient_registration):
            CustomUser.objects.create(username=instance.Username, user_type='patient')
        elif isinstance(instance, Doctor_registration):
            CustomUser.objects.create(username=instance.Username, user_type='doctor')
    else:
        if isinstance(instance, Patient_registration):
            instance.user.customuser.user_type = 'patient'
            instance.user.customuser.save()
        elif isinstance(instance, Doctor_registration):
            instance.user.customuser.user_type = 'doctor'
            instance.user.customuser.save()
