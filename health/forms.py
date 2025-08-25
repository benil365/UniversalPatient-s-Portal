from django import forms
from .models import Doctor_registration , PatientUpload , Patient_registration, HospitalUpload
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from user.models import Doctor, Patient,CustomUser

class Hospital_registrationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['Username', 'Password']

class Patient_registrationForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['Username', 'password', 'Hospital']
        widgets = {
            'password': forms.PasswordInput(),
        }


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Change Password'))

class AuthenticationForm(forms.ModelForm):
        model = AuthenticationForm
        fields= ['Username','Password']

class MyAuthenticationForm(AuthenticationForm):
    class Meta:
        model =CustomUser
        fields=['user_type','hospital_name']
        
class Doctor_registrationForm(forms.ModelForm):
    class Meta:
       model = Doctor_registration
       fields =['name','reg_number','email','Username','Password','category']

class HospitalUploadForm(forms.ModelForm):
     class Meta:
          model=HospitalUpload
          fields=['name', 'Patient_Id','category','file']

class PatientUploadForm(forms.ModelForm):
    class Meta:
        model = PatientUpload
        fields=['Identity_No','email','hospital','file']

class Patient_registrationForm(forms.ModelForm):
     class Meta:
          model = Patient_registration 
          fields =['First_name','Second_name','Other_name','Identity_No','Date_of_birth','Gender','email','Hospital','Username','Password']
