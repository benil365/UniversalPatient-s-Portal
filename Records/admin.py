from django.contrib import admin
from .models import Hospital_user_Registration,HospitalPatient_registration,Patient_Medical_Record
# Register your models here
class Hospital_user_RegistrationAdmin(admin.ModelAdmin):
    list_display=['Name','Registration_number','Hospital_Email','Gender','Password']

class HospitalPatientRegistrationAdmin(admin.ModelAdmin):
    list_display = ['First_name','Second_name','Other_name','Identity_No','Date_of_birth','Gender','Residence','email','Hospital','Username','Password']

class Patient_Medical_RecordAdmin(admin.ModelAdmin):
    list_display=['Date','Symptoms','Tests','Results','Diagnosis','Prescription','Recomendations','Image']


admin.site.register(Hospital_user_Registration, Hospital_user_RegistrationAdmin)
admin.site.register(HospitalPatient_registration, HospitalPatientRegistrationAdmin)
admin.site.register(Patient_Medical_Record, Patient_Medical_RecordAdmin)