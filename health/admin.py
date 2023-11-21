from django.contrib import admin
from .models import Doctor_registration, HospitalUpload, PatientUpload, Patient_registration 

class UserAdmin(admin.ModelAdmin):
    pass

# Register your models here.
class Doctor_registrationAdmin(admin.ModelAdmin):
    list_display = ['name','reg_number','email', 'category']
 
# Register your models here.
class HospitalUploadAdmin(admin.ModelAdmin):
    list_display = ['name', 'Patient_Id', 'category','file']

class PatientUploadAdmin(admin.ModelAdmin):
    list_display = ['Identity_No', 'email', 'hospital']

class PatientRegistrationAdmin(admin.ModelAdmin):
    list_display = ['First_name','Second_name','Other_name','Identity_No','Date_of_birth','Gender','email','Hospital','Username','Password']

admin.site.register(PatientUpload, PatientUploadAdmin)
admin.site.register(Doctor_registration, Doctor_registrationAdmin)
admin.site.register(HospitalUpload, HospitalUploadAdmin,)
admin.site.register(Patient_registration, PatientRegistrationAdmin)

# Register your models here.
