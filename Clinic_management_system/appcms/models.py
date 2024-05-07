from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.dispatch import receiver

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Staff(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    ROLE_CHOICES = [
        ('Doctor', 'Doctor'),
        ('Lab Technician', 'Lab Technician'),
        ('Pharmacist', 'Pharmacist'),
        ('Receptionist', 'Receptionist'),
        # Add other roles as needed
    ]

    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15)  # Assuming phone number format
    date_of_joining = models.DateField()
    username = models.CharField(max_length=100, blank= True)
    password = models.CharField(max_length=100, blank= True)
    is_active = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if the staff member is being created for the first time
        if not self.pk:
            # Create a corresponding User instance and save it
            user = User.objects.create_user(username=self.username, password=self.password)
            # Assign the user to the staff member
            self.user = user
        else:
            # Staff instance is being updated, retrieve the associated User instance
            user = self.user
            if user:
                # Update username and password if they are provided
                if self.username:
                    user.username = self.username
                if self.password:
                    user.set_password(self.password)
                user.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='Doctor', limit_choices_to={'role': 'Doctor'})
    specialization = models.CharField(max_length=100)
    consultation_fee = models.IntegerField()
    def __str__(self):
        return self.staff.name


class LoginDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    def log_login(self):
        self.login_time = timezone.now()
        self.save()

    def log_logout(self):
        self.logout_time = timezone.now()
        self.save()



class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]

    fullname = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dateofbirth = models.DateField()
    age = models.IntegerField()
    bloodgroup = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    mobile = models.CharField(max_length=15)
    address = models.TextField()
    email = models.CharField(max_length=25,blank=True)
    registernumber = models.CharField(max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.registernumber:
            last_patient = Patient.objects.order_by('-id').first()
            new_registernumber = f"REG{str(last_patient.id + 1).zfill(4)}" if last_patient else "REG0001"
            self.registernumber = new_registernumber
        super(Patient, self).save(*args, **kwargs)

    def __str__(self):
        return self.registernumber



class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    availability = models.BooleanField()

    def __str__(self):
        return f"{self.doctor} - {'Available' if self.availability else 'Not Available'}"

class Appointment(models.Model):
    doctor = models.ForeignKey(DoctorAvailability, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date_of_visit = models.DateField(auto_now_add=True)
    token = models.CharField(max_length=10, unique=True, editable=False)
    bill_no = models.CharField(max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.bill_no:
            last_bill = Appointment.objects.order_by('-id').first()
            new_bill_no = f"BILL{str(last_bill.id + 1).zfill(4)}" if last_bill else "BILL0001"
            self.bill_no = new_bill_no

        if not self.token:
            last_appointment = Appointment.objects.order_by('-id').first()
            new_token = f"TOKEN{str(last_appointment.id + 1).zfill(4)}" if last_appointment else "TOKEN0001"
            self.token = new_token

        super(Appointment, self).save(*args, **kwargs)

    def __str__(self):
        return f"Token: {self.token}, Bill No: {self.bill_no}"



class AppointmentBill(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointed_doc = models.ForeignKey(DoctorAvailability, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    bill_no = models.CharField(max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.bill_no:
            last_bill = AppointmentBill.objects.order_by('-id').first()
            new_bill_no = f"BILL{str(last_bill.id + 1).zfill(4)}" if last_bill else "BILL0001"
            self.bill_no = new_bill_no
        super(AppointmentBill, self).save(*args, **kwargs)

    def __str__(self):
        return self.bill_no




class Medicine(models.Model):
    medicine_name = models.CharField(max_length=255)
    description = models.TextField()
    stock_quantity = models.IntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.medicine_name


class Test(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class MedicineHistory(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorAvailability, on_delete=models.CASCADE)
    dateofvisit = models.DateTimeField(auto_now_add=True)
    observation_details = models.TextField()
    diagnosis_details = models.TextField()
    choose_test = models.ManyToManyField(Test, blank= True)




class PrescriptionDetail(models.Model):
    medicine_prescription = models.ForeignKey(MedicineHistory, on_delete=models.CASCADE, related_name='prescription_details')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=255)
    time_of_consumption = models.CharField(max_length=255)
    days = models.CharField(max_length=255,blank=True)



class MedicineQuantity(models.Model):
    prescribed_medicine = models.ForeignKey(PrescriptionDetail, on_delete=models.CASCADE,related_name='medicine_quantities')
    quantity = models.IntegerField(default=1)

@receiver(post_save, sender=MedicineQuantity)
def update_stock_quantity(sender, instance, **kwargs):
    # Update stock quantity when a new MedicineQuantity instance is created
    medicine = instance.prescribed_medicine.medicine
    new_stock_quantity = medicine.stock_quantity - instance.quantity
    if new_stock_quantity >= 0:
        medicine.stock_quantity = new_stock_quantity
        medicine.save()


class MedicineBill(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    medicine_prescription_id = models.ForeignKey(MedicineHistory, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    medicine_bill_id = models.CharField(max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.medicine_bill_id:
            last_bill = MedicineBill.objects.order_by('-id').first()
            new_bill_no = f"MED{str(last_bill.id + 1).zfill(4)}" if last_bill else "MED0001"
            self.medicine_bill_id = new_bill_no
        super(MedicineBill, self).save(*args, **kwargs)

    def __str__(self):
        return self.medicine_bill_id


class LabBill(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(DoctorAvailability, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    tested_tests = models.ForeignKey(MedicineHistory, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    test_bill_id = models.CharField(max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.test_bill_id:
            last_bill = LabBill.objects.order_by('-id').first()
            new_bill_no = f"TES{str(last_bill.id + 1).zfill(4)}" if last_bill else "TES0001"
            self.test_bill_id = new_bill_no
        super(LabBill, self).save(*args, **kwargs)


    def __str__(self):
        return self.test_bill_id


class LabReport(models.Model):
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE)
    staff_id = models.ForeignKey(Staff,on_delete=models.CASCADE)
    doctor_id = models.ForeignKey(DoctorAvailability,on_delete=models.CASCADE)
    tests = models.ManyToManyField(Test)
    report = models.TextField()
    lab_report_id = models.CharField(max_length=10, unique=True, editable=False)
    test_bill_id = models.CharField(max_length=10, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.test_bill_id:
            last_bill = LabReport.objects.order_by('-id').first()
            new_bill_no = f"TES{str(last_bill.id + 1).zfill(4)}" if last_bill else "TES0001"
            self.test_bill_id = new_bill_no

        if not self.lab_report_id:
            last_report = LabReport.objects.order_by('-id').first()
            new_report_id = f"LR{str(last_report.id + 1).zfill(4)}" if last_report else "LR0001"
            self.lab_report_id = new_report_id

        super(LabReport, self).save(*args, **kwargs)

    def __str__(self):
        return self.lab_report_id