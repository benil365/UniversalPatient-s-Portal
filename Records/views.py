from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from .forms import  HospitalPatient_registrationForm ,Patient_Medical_recordForm,Hospital_user_RegistrationForm 
from django.contrib.auth.views import LogoutView ,LoginView
import io
from .models import Hospital_user_Registration,Patient_Medical_Record
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from user.models import Patient, Doctor
from django.urls import reverse_lazy
from user.models import CustomUser ,DoctorData
from .forms import PatientSearchForm


class RegistrationPage(TemplateView):
    template_name = "Reg.html"

    def get(self, request, *args, **kwargs):
        form = HospitalPatient_registrationForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = HospitalPatient_registrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['Username']
            identity = form.cleaned_data['Identity_No']
            password = form.cleaned_data['Password']
            hospital = form.cleaned_data['Hospital']

            # Check if the username already exists
            if Patient.objects.filter(identity=identity).exists():
                messages.error(request, 'Identy number already exists. Please request for medical record.')
                return redirect('Reg.html')

            # Create a CustomUser for the patient
            user = Patient.objects.create_user(username=username, password=password, user_type='patient')
            user.set_password(password)
            user.save()

            # Create Patient object and link to the user and hospital
            patient = Patient(user=user)
            patient.save()

            print("Form data:", form.cleaned_data)
            print("User:", user)
            print("Patient:", patient)
            patient.my_hospitals.add(hospital)
            
            # Redirect to the success page
            return redirect("success")
        
        else:
            messages.error(request, "Failed to register")
            print(form.errors)  # Print form errors for debugging
            messages.success(request, "Your registration has been submitted")
            form = HospitalPatient_registrationForm()  # Reset the form
            return render(request, "Reg.html", {'form': form})


def success(request):
    return render(request, "success.html")

class Loginpage(LoginView):
    template_name = "SignIn.html"

class MadicalPage(TemplateView):
    template_name = "record.html"

@login_required(login_url='/SignIn/')
def Patient_Medical_Record(request):
    if request.method == 'POST':
        form = Patient_Medical_recordForm(request.POST, request.FILES)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.user = request.user
            medical_record.patient = request.user.patient
            medical_record.save()

            # Generate PDF
            pdf_data = generate_pdf(request.user, medical_record)

            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = 'filename="medical_record.pdf"'
            
            # Success message
            messages.success(request, 'Medical record saved successfully!')

            return response
        else:
            # Form is not valid, add an error message
            messages.error(request, 'Error saving the medical record. Please check the form.')
    else:
        form = Patient_Medical_recordForm()

    return render(request, 'record.html', {'form': form})

def generate_pdf(user, medical_record):
    template_path = 'log.html'  # Replace with your actual template path
    context = {'user': user, 'medical_record': medical_record}
    
    template = get_template(template_path)
    html = template.render(context)
    
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)
    
    if not pdf.err:
        return result.getvalue()
    return b''
        
class HomePage(TemplateView):
    template_name="base.html"

class DoctorPage(TemplateView):
    template_name="remo.html"

def Hospital_user_Registration(request):
    """
    The function `Hospital_user_reg` is a view function that handles the registration of a
    hospital user, creates a CustomUser and DoctorData object, and authenticates the user.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    user. It contains information such as the method used (GET or POST), the data sent in the request,
    and other metadata
    :return: a rendered HTML template named "remo.html" with the form data passed as context.
    """
    if request.method == "POST":
        form = Hospital_user_RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["Password"]
            doctor_name = form.cleaned_data["Name"]
           

            # Check if the user already exists
            if CustomUser.objects.filter(username=username).exists():
                messages.error(
                    request, "Username already exists. Please choose a different one."
                )
                return redirect("Records:doctor")
            else:
                # Create a CustomUser for the doctor
                user = CustomUser.objects.create_user(
                    username=username, password=password, user_type="doctor"
                )
                Doctor.save()
                
                # Create DoctorData object and link to the doctor
                doctor = Doctor.objects.create(username=doctor_name)
                doctor_data = DoctorData.objects.create(user=user, doctor=doctor)
                
                # Debugging statement to check authentication
                authenticated_user = authenticate(
                    request, username=username, password=password
                )
                print("Authenticated user:", authenticated_user)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    return redirect("signin")
                else:
                    messages.error(
                        request,
                        "Failed to authenticate. Please check your username and password.",
                    )
                    return redirect("Records:doctor")
        else:
            messages.error(request, "Failed to register Hospital or login")
            messages.success(request, "Your hospital registration has been submitted")
            return redirect("health:Success")
    else:
        form = Hospital_user_RegistrationForm()

    return render(request, "remo.html", {"form": form})
# Create your views here.
@login_required(login_url='/SignIn/')
def search_patient(request):
    if request.method == 'POST':
        form = PatientSearchForm(request.POST)
        if form.is_valid():
            Username = form.cleaned_data['Username']
            # Perform the search based on the provided criteria
            try:
                patient = CustomUser.objects.get(Username=Username)
                # Render a template to display patient details
                return render(request, 'record.html', {'patient': patient})
            except Patient.DoesNotExist:
                messages.warning(request, 'No patient with the provided identity number found.')
        else:
            messages.error(request, 'Invalid search criteria. Please check the form.')
    else:
        form = PatientSearchForm()
    
    return render(request, 'record.html', {'form': form}) 
        

