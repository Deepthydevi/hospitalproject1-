from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from hostapp.forms import DoctorForm, PatientForm, AppointmentForm, PrescriptionForm, ContactForm
from hostapp.models import Doctor, Department, Patient, Appointment
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


# Create your views here.
def homePage(request):
    return render(request, 'index.html')
def adminclick_view(request):
    return render(request,'admin.html')

def doctorclick_view(request):
    return render(request,'doctor.html')

def patientclick_view(request):
    return render(request,'patient.html')

def admin_signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
        else:
            # Create the user with admin privileges
            user = User.objects.create_user(username=username, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = True  # Give the user admin privileges
            user.save()

            messages.success(request, 'Admin account created successfully.')
            return redirect('admin_login')  # Consider redirecting to a confirmation page

    return render(request, 'adminsignup.html')

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:  # Check if the user is an admin
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('admin_dashboard')  # Redirect to admin dashboard or any page
            else:
                messages.error(request, 'You do not have admin privileges.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'admin_login.html')


@login_required
def admin_dashboard_view(request):
    if not request.user.is_staff:  # Ensure only admin users can access
        return redirect('admin_login')

    return render(request, 'admin_dashboard.html')

def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor added successfully!')
            return redirect('listdoctor')  # Redirect after successful form submission
        else:
            messages.error(request, 'There was an error in your form. Please check the fields.')
    else:
        form = DoctorForm()  # Display the empty form for a GET request

    return render(request, 'admin-add_doctor.html', {'form': form})



def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin-doctor_list.html', {'doctors': doctors})

def update_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, id=pk)
    departments = Department.objects.all()  # Get all departments

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('listdoctor')  # Change this to your desired redirect URL
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'admin-update_doctor.html', {'form': form, 'doctor': doctor, 'departments': departments})

def delete_doctor_view(request, pk):
    doctor = get_object_or_404(Doctor, id=pk)
    doctor.delete()
    return redirect('listdoctor')  # Ensure 'patient-list' is a defined URL



def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()  # Save the patient instance
            return redirect('listpatient')  # Redirect to the patient list after successful addition
    else:
        form = PatientForm()  # Display an empty form for GET requests

    return render(request, 'admin-add_patient.html', {'form': form})

def patient_list(request):
    patients = Patient.objects.all()
    return render(request, 'admin-patient_list.html', {'patients': patients})

def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'admin-patient_detail.html', {'patient': patient})

def update_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)  # Fetch the patient instance

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('listpatient')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'admin-update_patient.html', {'form': form, 'patient': patient})


def delete_patient_view(request, pk):
    patient = get_object_or_404(Patient, id=pk)
    patient.delete()
    return redirect('listpatient')  # Ensure 'patient-list' is a defined URL

def admin_appointment_view(request):
    return render(request,'admin_appointment.html')

def add_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the appointment instance
            return redirect('admin_view_appointment')  # Redirect to a list of appointments or any other view
    else:
        form = AppointmentForm()  # Display an empty form for GET requests

    return render(request, 'admin_add_appointment.html', {'form': form})


def appointment_list(request):
    appointments = Appointment.objects.all()  # Fetch all appointment instances
    return render(request, 'appointment_list.html', {'appointments': appointments})

def approve_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.method == 'POST':
        appointment.status = 'Approved'  # Update the status to 'Approved'
        appointment.save()  # Save the changes
        messages.success(request, 'Appointment approved successfully!')
        return redirect('appointment_list')  # Redirect to the list of appointments

    return render(request, 'approve_appointment.html', {'appointment': appointment})


def doctor_signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        doctor_form = DoctorForm(request.POST)

        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.email = doctor_form.cleaned_data['email']  # Doctor's email from the DoctorForm
            doctor.save()
            login(request, user)
            return redirect('doctor_login')  # Redirect to doctor list after signup
        else:
            # Show error messages on the form
            messages.error(request, "Error in form submission. Please check your inputs.")
            print(user_form.errors)
            print(doctor_form.errors)
    else:
        user_form = UserCreationForm()
        doctor_form = DoctorForm()

    return render(request, 'doctor_signup.html', {
        'user_form': user_form,
        'doctor_form': doctor_form
    })


def doctor_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('doctor_dashboard')  # Redirect to doctor's dashboard after login
    else:
        form = AuthenticationForm()
    return render(request, 'doctor_login.html', {'form': form})

def doctor_dashboard(request):
    # Fetch doctor's appointments or relevant data
    appointments = Appointment.objects.filter(doctor__user=request.user)  # Assuming there's a relation to User
    return render(request, 'navbar1.html', {'appointments': appointments})

def patient_medical_history(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    medical_histories = patient.medical_histories.all()  # Access related medical history entries
    return render(request, 'patient_medical_history.html', {'patient': patient, 'medical_histories': medical_histories})

def list_patient_histroy(request):
    patients = Patient.objects.all()
    return render(request, 'patient_list.html', {'patients': patients})


def prescribe_medicine(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.doctor = doctor  # Assign the doctor who is prescribing
            prescription.save()
            return redirect('doctor_dashboard')  # Redirect after successful submission
    else:
        form = PrescriptionForm()

    return render(request, 'doctor-prescribe_medicine.html', {'form': form, 'doctor': doctor})

def patient_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('patient_dashboard')  # Redirect to patient's dashboard after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'patient_login.html', {'form': form})


def patient_signup(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        patient_form = PatientForm(request.POST)

        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save()
            patient = patient_form.save(commit=False)
            patient.user = user  # Link the patient to the user
            patient.email = patient_form.cleaned_data['email']  # Patient's email from the PatientForm
            patient.save()
            login(request, user)  # Automatically log the patient in after signup
            return redirect('patient_login')  # Redirect to patient dashboard after signup
        else:
            # Print the errors to the console for debugging
            print("User Form Errors:", user_form.errors)
            print("Patient Form Errors:", patient_form.errors)

            messages.error(request, "Error in form submission. Please check your inputs.")
    else:
        user_form = UserCreationForm()
        patient_form = PatientForm()

    return render(request, 'patient_signup.html', {
        'user_form': user_form,
        'patient_form': patient_form
    })


@login_required
def patient_dashboard(request):
    try:
        # Fetch the patient associated with the current logged-in user
        patient = Patient.objects.get(user=request.user)

        # Fetch all appointments for the patient
        appointments = Appointment.objects.filter(patient=patient)

        context = {
            'patient': patient,
            'appointments': appointments
        }
        return render(request, 'patient_dashboard.html', context)

    except Patient.DoesNotExist:
        # In case the patient profile is not found, handle the error
        messages.error(request, "Patient profile not found. Please contact support.")
        return redirect('patient_signup')  # Or some error page

@login_required
def patient_profile(request):
    # Get the patient instance linked to the logged-in user
    patient = get_object_or_404(Patient, user=request.user)

    return render(request, 'patientprofile.html', {
        'patient': patient
    })

from django.shortcuts import render

def health_resources(request):
    tips = [
        {
            "title": "Measure and Watch Your Weight",
            "content": "Keeping track of your body weight on a daily or weekly basis will help you see what you’re losing and/or what you’re gaining."
        },
        {
            "title": "Limit Unhealthy Foods and Eat Healthy Meals",
            "content": "Do not forget to eat breakfast and choose a nutritious meal with more protein and fiber and less fat, sugar, and calories. For more information on weight-control foods and dietary recommendations, please check the following website: www.hsph.harvard.edu/obesity-prevention-source/obesity-causes/diet-and-weight/"
        },
        {
            "title": "Take Multivitamin Supplements",
            "content": "To make sure you have sufficient levels of nutrients, taking a daily multivitamin supplement is a good idea. However, there’s currently NO available evidence that adding any supplements or 'miracle mineral supplements' to your diet will help protect you from the virus."
        },
        {
            "title": "Drink Water and Stay Hydrated, and Limit Sugared Beverages",
            "content": "Drink water regularly to stay healthy, but there is NO evidence that drinking water frequently can help prevent any viral infection."
        },
        {
            "title": "Exercise Regularly and Be Physically Active",
            "content": "At this time, at-home workouts may be a good idea. Be sure you know what’s going on in your area and if there are any restrictions."
        },
        {
            "title": "Reduce Sitting and Screen Time",
            "content": "Even people who exercise regularly could be at increased risk for diabetes and heart disease if they spend lots of time sitting behind computers."
        },
        {
            "title": "Get Enough Good Sleep",
            "content": "You can keep your immune system functioning properly by getting seven to eight hours of sleep each night."
        },
        {
            "title": "Go Easy on Alcohol and Stay Sober",
            "content": "Drinking alcohol does not protect you from the coronavirus infection. Alcohol should always be consumed in moderation."
        },
        {
            "title": "Find Ways to Manage Your Emotions",
            "content": "It is common for people to have feelings of fear, anxiety, sadness, and uncertainty during a pandemic. Use information about stress and coping provided by the CDC."
        },
        {
            "title": "Use an App to Keep Track of Your Movement, Sleep, and Heart Rate",
            "content": "People with serious chronic medical conditions should talk to their medical providers and listen to their advice."
        }
    ]

    return render(request, 'health_resources.html', {'tips': tips})

@login_required
def patient_appointments(request):
    # Get the logged-in user's corresponding Patient object
    try:
        patient = request.user.patient_profile  # Use the related name defined in the Patient model
    except Patient.DoesNotExist:
        return HttpResponse("Patient profile does not exist.", status=404)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient  # Set the patient to the logged-in user
            appointment.save()
            return redirect('patient_appointments')  # Redirect to the same view to see the updated appointments
    else:
        form = AppointmentForm()

    # Get all appointments for this patient
    appointments = Appointment.objects.filter(patient=patient)

    return render(request, 'patient_appointments.html', {
        'appointments': appointments,
        'form': form,
    })


# Function to create a User and a corresponding Patient object
def create_patient_user(username, password, patient_data):
    user = User.objects.create_user(username=username, password=password)
    patient = Patient.objects.create(user=user, **patient_data)  # patient_data is a dict with additional patient fields
    return user, patient  # Returning both objects if needed

@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    if created:
        Patient.objects.create(user=instance)

