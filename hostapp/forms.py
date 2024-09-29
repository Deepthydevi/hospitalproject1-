from django import forms
from django.contrib.auth.views import LoginView

from .models import Patient, Doctor, Appointment, Department, Prescription

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'  # Ensure this includes all necessary fields
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'departments', 'address', 'mobile', 'email', 'specialization', 'experience', 'status']

        # Optional: Add custom widgets if you want to style the dropdown or other fields
        widgets = {
            'departments': forms.Select(attrs={'class': 'form-control'}),  # To style the dropdown
        }

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'medicine_name', 'dosage', 'instructions']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'medicine_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control'}),
        }

class PatientEditForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['name', 'email', 'mobile', 'gender', 'address', 'medical_history']

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Your Name')
    email = forms.EmailField(required=True, label='Your Email')
    message = forms.CharField(widget=forms.Textarea, required=True, label='Your Message')
