from django.contrib.auth.models import User
from django.db import models
from django import forms

# Patient Model
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile',null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "No Name"

# Department Model

class Department(models.Model):
    department_choices = [
        ('Emergency', 'Emergency'),
        ('Pediatrics', 'Pediatrics'),
        ('Oncology', 'Oncology'),
        ('Radiology', 'Radiology'),
    ]
    departments = models.CharField(max_length=30, choices=department_choices, blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.departments

# Doctor Model
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    departments = models.ForeignKey(Department, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    experience = models.PositiveIntegerField()  # Years of experience
    status = models.BooleanField(default=True, null=True, blank=True)  # Active or Inactive

    def __str__(self):
        return self.name if self.name else "No Name"

# Appointment Model
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    symptoms = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed')],
        default='Pending'
    )
    payment_status = models.CharField(max_length=50, default='Pending')

    # New field to store Stripe Payment Intent ID
    payment_intent_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} on {self.appointment_date}"


class MedicalHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_histories')
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"History for {self.patient.name} on {self.date}"

class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medicine_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField()  # e.g., "Take after meals"
    date_prescribed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.name} by {self.doctor.name}"

# Billing Model
class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Cancelled', 'Cancelled')], default='Pending')
    date_billed = models.DateField(auto_now_add=True)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)  # To store Stripe payment intent ID

    def __str__(self):
        return f"Bill for {self.patient.name} - {self.total_amount}"
