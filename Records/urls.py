from . import views
from django.urls import path
from django.contrib.auth.views import LoginView
from .views import HomePage,RegistrationPage,MadicalPage, Hospital_user_Registration, Patient_Medical_Record, search_patient
app_name='Records'
urlpatterns=[
    path("", HomePage.as_view(), name="hospital"),
    path("SignUp/", LoginView.as_view(template_name='SignIn.html'), name="signin"),
    path("accounts/profile/", Patient_Medical_Record, name="Mhr"),
    path("Reg/", RegistrationPage.as_view(), name="register"),
    path("doctor/",Hospital_user_Registration, name="doctor"),
    path("medical/", Patient_Medical_Record, name= "medical form"),
    path('search_patient/', views.search_patient, name='search_patient'),
    
]