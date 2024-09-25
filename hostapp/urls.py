from django.urls import path
from . import views
from .views import admin_login_view, admin_dashboard_view

urlpatterns = [
    path('', views.homePage, name='index'),
    path('adminclick/', views.adminclick_view, name='adminclick'),
    path('doctorclick/', views.doctorclick_view, name='doctorclick'),
    path('patientclick/', views.patientclick_view, name='patientclick'),
    path('admin_signup/', views.admin_signup_view, name='admin_signup'),
    path('admin_login/', admin_login_view, name='admin_login'),
    path('admin_dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('add_doctor/',views.add_doctor,name='add_doctor'),
    path('listdoctor/',views.doctor_list,name='listdoctor'),
    path('update_doctor/<int:pk>/', views.update_doctor_view, name='update_doctor'),
    path('delete_doctor/<int:pk>/', views.delete_doctor_view, name='delete_doctor'),
    path('add_patient/',views.add_patient, name='add_patient'),
    path('patients/<int:patient_id>/detail/', views.patient_detail, name='patient_detail'),
    path('listpatient/',views.patient_list, name='listpatient'),
    path('delete_patient/<int:pk>/', views.delete_patient_view, name='delete_patient'),
    path('update_patient/<int:patient_id>/', views.update_patient, name='update_patient'),
    path('admin-add-appointment/', views.add_appointment, name='add_appointment'),
    path('adminappointment/',views.admin_appointment_view,name='adminappointment'),
    path('admin-view-appointment/', views.appointment_list, name='admin_view_appointment'),
    path('appointments/approve/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('doctor/signup/', views.doctor_signup, name='doctor_signup'),
    path('doctor/login/', views.doctor_login, name='doctor_login'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('patients/<int:patient_id>/medical-history/', views.patient_medical_history, name='patient_medical_history'),
    path('patientlist/',views.list_patient_histroy,name='patientlist'),
    path('prescribe/<int:patient_id>/<int:doctor_id>/', views.prescribe_medicine, name='prescribe_medicine'),
    path('patient_signup/', views.patient_signup, name='patient_signup'),
    path('patient_login/', views.patient_login, name='patient_login'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('patientprofile/', views.patient_profile, name='patient_profile'),
    path('health_resources/', views.health_resources, name='health_resources'),
    path('appointments/', views.patient_appointments, name='patient_appointments'),


]