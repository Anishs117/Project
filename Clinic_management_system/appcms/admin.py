from django.contrib import admin
from .models import Doctor,Staff,Patient,DoctorAvailability,Appointment,\
    AppointmentBill,Medicine,Test,MedicineHistory,\
    MedicineBill,LabBill,LabReport,PrescriptionDetail,MedicineQuantity, LoginDetails
from rest_framework.authtoken.models import Token
# Register your models here.

admin.site.register(Doctor)
admin.site.register(Staff)
admin.site.register(Patient)
admin.site.register(DoctorAvailability)
admin.site.register(Appointment)
admin.site.register(AppointmentBill)
admin.site.register(Test)
admin.site.register(Medicine)
admin.site.register(MedicineHistory)
admin.site.register(MedicineBill)
admin.site.register(LabBill)
admin.site.register(LabReport)
admin.site.register(Token)
admin.site.register(PrescriptionDetail)
admin.site.register(MedicineQuantity)
admin.site.register(LoginDetails)
