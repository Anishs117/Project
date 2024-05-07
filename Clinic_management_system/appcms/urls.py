from django.urls import path
from .views import Patient_list, Patient_details_view, Doctor_Availability_view, \
    Doctor_Availability_details_view, Appointment_view, Appointment_details_view, \
    Appointment_bill_view, Appointment_bill_details_view, Medicine_list, Medicine_details_view, \
    Test_list, Test_details_view, LoginAPIView, LogoutAPIView, doctor_list, doctor_detail, \
    medicine_history_list, medicine_history_detail,\
    staff_list, staff_details_view, Lab_bill_details, \
    Lab_report_list, Lab_report_details, Medicine_Bills, prescription_detail_detail, \
    prescription_detail_list, medicine_quantity_list, medicine_quantity_detail, Lab_bill, medicine_bill_detail
from . import views


urlpatterns = [
    path('api/patient_details', Patient_list),
    path('api/patient_details/<int:passed_id>', Patient_details_view),
    path('api/doctor_availability', Doctor_Availability_view),
    path('api/doctor_availability/<int:passed_id>',Doctor_Availability_details_view),
    path('api/appointment', Appointment_view),
    path('api/appointment/<int:passed_id>',Appointment_details_view),
    path('api/appointment_bill', Appointment_bill_view),
    path('api/appointment_bill/<int:passed_id>', Appointment_bill_details_view),

    path('api/medicine', Medicine_list),
    path('api/medicine/<int:passed_id>',Medicine_details_view),
    path('api/test', Test_list),
    path('api/test/<int:passed_id>', Test_details_view),

    path('api/user/login', LoginAPIView.as_view(), name = 'user-login'),
    path('api/logout', LogoutAPIView.as_view()),
    path('api/logindetails', views.LoginDetailsListCreateView.as_view(), name='logindetails-list'),
    path('api/doctors', doctor_list, name='doctor-list'),
    path('api/doctors/<int:doctor_id>', doctor_detail, name='doctor-detail'),
    path('api/staff', staff_list),
    path('api/staff/<int:staff_id>', staff_details_view),



    path('api/medicine-history', medicine_history_list, name='medicine-history-list'),
    path('api/medicine-history/<int:passed_id>', medicine_history_detail, name='medicine-history-detail'),


    path('api/lab-bill/', Lab_bill, name='lab-bill-list'),
    path('api/lab-bill/<int:staff_id>', Lab_bill_details),

    path('api/lab-report', Lab_report_list, name='lab_report_list'),
    path('api/lab-report/<int:passed_id>', Lab_report_details, name='lab_report_detail'),

    path('api/medicine_bills', Medicine_Bills),
    path('api/medicine_bills/<int:passed_id>', medicine_bill_detail),

    path('api/prescription_detail',prescription_detail_list),
    path('api/prescription_detail/<int:passed_id>', prescription_detail_detail),

    path('api/medicine_quantity',medicine_quantity_list),
    path('api/medicine_quantity/<int:passed_id>', medicine_quantity_detail),

]