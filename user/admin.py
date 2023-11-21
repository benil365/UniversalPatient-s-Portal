from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Doctor, Patient

# Register the CustomUser model with its UserAdmin
admin.site.register(CustomUser, UserAdmin)

# Register Hospital and Patient models if needed
admin.site.register(Doctor)
admin.site.register(Patient)

# Register your models here.
