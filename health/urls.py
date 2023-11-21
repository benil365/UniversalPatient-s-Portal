from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from .views import UploadPage, FileUploadView, HospitalListView
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from .views import HomePage,Aboutpage,Servicespage,Doctor_registration,success,HospitalPage,LogoutView,UploadPage,Patient_registration,CustomLoginView,hospital_dashboard, patient_dashboard, change_password_view

app_name='health'
urlpatterns =[
  
    path("", HomePage.as_view(), name="home"),
    path("about/", Aboutpage.as_view(), name="about"),
    path("service/", Servicespage.as_view(), name="service"),
    path("registration/", Doctor_registration, name="registration"),
    path("patient/",Patient_registration, name="patient"),
    path ("success",LoginView.as_view(template_name='log.html'), name="hospitallog"),
    path("success/",LoginView.as_view(template_name='success.html'), name="Success"),
    path("hospital_login/",LoginView.as_view(template_name='hospitallog.html'), name="Patient_login"),
    path("login/",CustomLoginView.as_view(template_name='log.html'), name="login"),
    path('login/hospital_dashboard/', hospital_dashboard, name='hospital_dashboard'),
    path('login/patient_dashboard/', patient_dashboard, name='patient_dashboard'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home.html'), name='logout'),
    path("hospital_view",HospitalPage.as_view(), name="Hospital"),
    path('get_posts/', views.get_posts_view, name='get_posts'),
    path('search/', views.search_view, name='search'),
    path('dashboard/', UploadPage.as_view(), name='dashboard'),
    path('patients/', HospitalListView.as_view(), name='patient_list'),
    path('Upload/', FileUploadView.as_view(), name='Upload'),
    path('ChangePassword/', views.change_password_view, name='paswd_change'),
     
   
] + static(settings.STATIC_URL)