from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from .forms import (
    Doctor_registrationForm,
    Patient_registrationForm,
    HospitalUploadForm,
    ChangePasswordForm,
)
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from user.models import CustomUser, Patient, Doctor
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from .models import (
    PatientUpload,
    Doctor_registration,
    HospitalUpload,
    Patient_registration,
)
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model


def dashboard_view(request):
    # Retrieve data from models
    uploads = PatientUpload, HospitalUpload.objects.all()
    doctors = Doctor_registration, Patient_registration.objects.all()

    # Create a dictionary with the data
    context = {
        "uploads": uploads,
        "doctors": doctors,
    }

    # Pass the context dictionary when rendering the template
    return render(request, "uploadhos.html", "uploadpatient.html", context)


def get_posts_view(request):
    # Retrieve posts from the database or any other data source
    posts = Patient_registration.objects.all()  # Assuming you have a "Post" model

    # Create a list of post data
    post_data = []
    for post in posts:
        post_data.append(
            {
                "title": post.title,
                "content": post.content,
                # Add other fields as needed
            }
        )

    # Create a JSON response with the posts
    response = {
        "posts": post_data,
    }

    return JsonResponse(response)


def search_view(request):
<<<<<<< HEAD
    query = request.GET.get("q", "")
    results = []

    if query:
        patient_results = Patient.objects.filter(Username__icontains=query)
        doctor_results = Doctor.objects.filter(Username__icontains=query)
        hospital_results = HospitalUpload.objects.filter(name__icontains=query)  # <-- changed here

        for patient in patient_results:
            results.append(f"Patient: {patient.Username}")
        for doctor in doctor_results:
            results.append(f"Doctor: {doctor.Username}")
        for hospital in hospital_results:
            results.append(f"Hospital: {hospital.name}")  # <-- changed here
=======
    query = request.GET.get("q")  # Get the search query from the request
    results = []  # Perform the search operation and obtain search results
>>>>>>> 144a6299dd623bb6476b549c3b2c0f28d01a8a1d

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "search_results.html", context)


class CustomLoginView(LoginView):
    pass


class HomePage(TemplateView):
    template_name = "home.html"


class Aboutpage(TemplateView):
    template_name = "about.html"


class Servicespage(TemplateView):
    template_name = "service.html"


class Registrationpage(TemplateView):
    template_name = "hosreg.html"


class Submitpage(TemplateView):
    template_name = "success.html"


class PatientPage(TemplateView):
    template_name = "patientreg.html"


class Loginpage(TemplateView):
    template_name = "hospitallog.html"


class UserLogpage(TemplateView):
    template_name = "hospitallog.html"


class LogoutView(LogoutView):
    next_page = "logout"


class PasswordChangePage(TemplateView):
    template_name = "passchange.html"


class HospitalPage(TemplateView):
    template_name = "uploadhos.html"


class UploadPage(LoginRequiredMixin, TemplateView):
    template_name = "uploadpatient.html"


class HospitalListView(LoginRequiredMixin, ListView):
    model = HospitalUpload
    template_name = "patient_list.html"
    context_object_name = "patients"


class FileUploadView(LoginRequiredMixin, TemplateView):
    template_name = "upload_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        uploaded_files = HospitalUpload.objects.filter(user_id=user.id)
        context["uploaded_files"] = uploaded_files

        # Check if the user is a patient and get their hospitals
        if user.user_type == "patient":
            patient = Patient.objects.get(user=user)
            my_hospitals = patient.my_hospitals.all()
            context["my_hospitals"] = my_hospitals
            context["num_hospitals"] = my_hospitals.count()
        return context

    def post(self, request, *args, **kwargs):
        form = HospitalUploadForm(request.POST, request.FILES)
        if form.is_valid():
            hospital_upload = form.save(commit=False)
            hospital_upload.user = self.request.user
            hospital_upload.save()

            # Check if the user is a patient and add the hospital to their "my hospitals" list
            if self.request.user.user_type == "patient":
                patient = Patient.objects.get(user=self.request.user)
                hospital = hospital_upload.hospital
                patient.my_hospitals.add(hospital)

            return self.render_to_response({"success": True})
        else:
            return self.render_to_response({"form": form})


def Doctor_registration(request):
    if request.method == "POST":
        form = Doctor_registrationForm(request.POST)
        if form.is_valid():
            # Extract form data
            username = form.cleaned_data["Username"]
            password = form.cleaned_data["Password"]
            doctor_name = form.cleaned_data["name"]
            reg_number = form.cleaned_data["reg_number"]
            
            # Check if the username already exists
            if get_user_model().objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different one.")
                return redirect("health:registration")
            else:
                # Create a new User instance
                user = get_user_model().objects.create_user(
                    username=username,
                    user_type='doctor',
                    password=password,
                    reg_number=reg_number,
                    name= doctor_name,
                )
                
                # Create a new Doctor instance associated with the created User instance
                doctor = Doctor.objects.create(
                    user=user,
                    Username=username,
                    Password=password,
                
                    # Add other doctor-specific fields here
                )
                
                # Log in the user
                authenticated_user = authenticate(request, username=username, password=password)
                if authenticated_user is not None:
                    login(request, authenticated_user)
                    return redirect("health:Hospital")
                else:
                    messages.error(request, "Failed to authenticate. Please check your username and password.")
                    return redirect("health:hospital_registration")
        else:
            # Handle invalid form submission
            messages.error(request, "Failed to register Hospital or login")
            messages.success(request, "Your hospital registration has been submitted")
            return redirect("success")
    else:
        form = Doctor_registrationForm()

    return render(request, "hosreg.html", {"form": form})

def Patient_registration(request):
    if request.method == "POST":
        form = Patient_registrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["Username"]
            password = form.cleaned_data["Password"]
            hospital = form.cleaned_data["Hospital"]
            identity = form.cleaned_data["Identity_No"]

            # Check if the username already exists
            if CustomUser.objects.filter(username=username).exists():
                messages.error(
                    request, "Username already exists. Please choose a different one."
                )
                return redirect("health:patient")

            # Create a CustomUser for the patient
            user = CustomUser.objects.create_user(
                username=username, password=password, user_id=identity, user_type="patient"
            )
            user.save()

            # Create Patient object and link to the user and hospital
            patient= Patient(Username = form.cleaned_data["Username"],
            password = form.cleaned_data["Password"],
            Hospital = form.cleaned_data["Hospital"],
            user_id =form.cleaned_data["Identity_No"],
            )
            patient.save()
            print("Form data:", form.cleaned_data)
            print("User:", user)
            print("Patient:", patient)
            patient = Patient.objects.create(
                user=user,
                Username=username,
                Password=password,
                Hospital=hospital,
                user_id=identity,
            )
            patient.my_hospitals.add(hospital)
            # Debugging statement to check authentication
            authenticated_user = authenticate(
                request, username=username, password=password
            )
            print("Authenticated user:", authenticated_user)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect("uploadpatient.html")
            else:
                messages.error(
                    request,
                    "Failed to authenticate. Please check your username and password.",
                )
                return redirect("patient_registration")
        else:
            messages.error(request, "Failed to register or login")
            print(form.errors)  # Print form errors for debugging
            messages.success(request, "Your registration has been submitted")
            return redirect("health:Success")
    else:
        form = Patient_registrationForm()
        return render(request, "patientreg.html", {"form": form})


def success(request):
    return render(request, "success.html")


@login_required
def profile(request):
    return render(request, "uploadhos.html")


def Login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("Username")
            password = form.cleaned_data.get("Password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(my_view)
        # If authentication fails or the form is invalid, render the login form with errors
        return render(request, "log.html", {"form": form})
    else:
        form = AuthenticationForm()
        return render(request, "log.html", {"form": form})


class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.user_type == "doctor":
            return "hospital_dashboard"  
        elif user.user_type == "patient":
            return "patient_dashboard"  
        else:
            return "home"


@login_required
def hospital_dashboard(request):
    # Add hospital-specific logic and context data here
    return render(request, "uploadhos.html")

@login_required
def patient_dashboard(request):
    user = request.user
    if user.user_type == "patient":
        user_type = 'patient'
        patients = CustomUser.objects.filter(user_type=user_type)
        patient = Patient.objects.filter()
        # Add patient-specific logic and context data here
        patient = CustomUser.objects.filter(user_type=user_type)  
    if patient.exists():
        patient = patients[0] 
        my_hospitals = patient.hospitals.all()
        num_hospitals = my_hospitals.count()
        # If there are patients with the specified user_type, you can do something with them.
        # For example, you can loop through the patients.
        patient_data = []  # Initialize a list to store patient data
        for patient in patients:
            # Access patient data using patient.username, patient.hospital_name, etc.
            patient_info = {
                'Username': patient.username,
                'hospital': patient.hospital_name,
                # Add more fields as needed
            }
            patient_data.append(patient_info)

        context = {
            "num_hospitals": num_hospitals,
            "my_hospitals": my_hospitals,
        }

        return render(request, "uploadpatient.html", context)
    else:
        return render(request, "uploadpatient.html")


@login_required
def my_view(request):
    user = request.user
    if user.user_type == "doctor":
        return redirect("hospital_dashboard")
    elif user.user_type == "patient":
        return redirect("patient_dashboard")
    else:
        return redirect("home")


@login_required
def change_password_view(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data["old_password"]
            new_password = form.cleaned_data["new_password"]

            # Verify the old password
            user = request.user
            if user.check_password(old_password):
                # Old password is correct, update the password
                user.set_password(new_password)
                user.save()

                # After changing the password, update the session auth hash
                # to keep the user logged in.
                update_session_auth_hash(request, user)
                return redirect('paswd_change') # Redirect another view
            else:
                # Old password is incorrect, show an error message
                form.add_error("old_password", "Incorrect old password.")
    else:
        form = ChangePasswordForm()
    return render(request, "passchange.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("home")


# Create your views here.
