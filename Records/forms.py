from django import forms
from .models import Hospital_user_Registration,HospitalPatient_registration,Patient_Medical_Record, MedicalRecord

class Hospital_user_RegistrationForm(forms.ModelForm):
     class Meta:
          model= Hospital_user_Registration
          fields= ['Name','Registration_number','Hospital_Email','username','Gender','Password']

class HospitalPatient_registrationForm(forms.ModelForm):
     class Meta:
          model = HospitalPatient_registration 
          fields =['First_name','Second_name','Other_name','Identity_No','Date_of_birth','Gender','Residence','email','Hospital','Username','Password']

class Patient_Medical_recordForm(forms.ModelForm):
     class Meta:
          model=Patient_Medical_Record
          fields=['Date','Symptoms','Tests','Results','Diagnosis','Prescription','Recomendations', 'Image']
class PatientSearchForm(forms.Form):
    Username = forms.CharField(max_length=30, label='Identity Number', required=False)
    # Add other search fields as needed

