from django.shortcuts import render
from .models import Staff, Doctor, Medicine, MedicineBill, MedicineHistory,AppointmentBill, \
    Appointment, LoginDetails, DoctorAvailability, PrescriptionDetail, MedicineQuantity
from .models import Patient, Test, LabBill, LabReport
from .serializers import PatientSerializers, AppointmentSerializers, \
    AppointmentBillSerializers, MedicineSerializers, MedicineHistorySerializer, \
    MedicineBillSerializers, PrescriptionDetailSerializer, MedicineQuantitySerializer
from .serializers import DoctorSerializers, DoctorAvalabilitySerializers, StaffSerializers, TestSerializers, \
    LoginSerializer, LabBillSerializer, LabReportSerializer, LoginDetailsSerializer
from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status,generics
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.contrib.auth import logout
from django.contrib.auth.models import User


# Create your views here.
class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Generate and return token
                token = Token.objects.get(user=user)

                # Create new LoginDetails object for this login session
                login_details = LoginDetails.objects.create(user=user)
                login_details.log_login()

                response = {'username': username, 'status': status.HTTP_200_OK, 'message': 'success',
                            'data': {'Token': token.key}}
                return Response(response, status=status.HTTP_200_OK)

            else:
                response = {'status': status.HTTP_401_UNAUTHORIZED, 'message': 'Invalid username or password'}
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        response = {'status': status.HTTP_400_BAD_REQUEST, 'message': 'Bad request', 'data': serializer.errors}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')  # Assuming the username is sent in the request data

        # Find the user based on the provided username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            response_data = {'message': 'User not found'}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        # Find the corresponding LoginDetails object for the user
        login_details = LoginDetails.objects.filter(user=user).last()

        if login_details:
            login_details.log_logout()
            response_data = {'message': 'Logout successful'}
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {'message': 'No active login session found'}
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class LoginDetailsListCreateView(generics.ListCreateAPIView):
    queryset = LoginDetails.objects.all()
    serializer_class = LoginDetailsSerializer
    # permission_classes = [IsAuthenticated]  # Add appropriate permissions


class LoginDetailsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoginDetails.objects.all()
    serializer_class = LoginDetailsSerializer
    # permission_classes = [IsAuthenticated]  # Add appropriate permissions


@csrf_exempt
def staff_list(request):
    if request.method == 'GET':
        staff_list = Staff.objects.all()
        serialize_staff_list = StaffSerializers(staff_list, many=True)
        return JsonResponse(serialize_staff_list.data, safe=False, status=200)
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        staff_add_serializer = StaffSerializers(data=request_data)
        if staff_add_serializer.is_valid():
            staff_add_serializer.save()
            return JsonResponse(staff_add_serializer.data, status=201)
        return JsonResponse(staff_add_serializer.errors, status=400)


@csrf_exempt
def staff_details_view(request, staff_id):
    try:
        staff_details = Staff.objects.get(id=staff_id)
    except Staff.DoesNotExist:
        return JsonResponse({'error': 'Staff not found'}, status=404)

    if request.method == 'GET':
        serialize_staff_details = StaffSerializers(staff_details)
        return JsonResponse(serialize_staff_details.data, safe=False, status=200)
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        staff_edit_serializer = StaffSerializers(staff_details, data=request_data)
        if staff_edit_serializer.is_valid():
            staff_edit_serializer.save()
            return JsonResponse(staff_edit_serializer.data, status=200)
        else:
            return JsonResponse(staff_edit_serializer.errors, status=400)
    elif request.method == 'DELETE':
        staff_details.delete()
        return HttpResponse(status=204)


@csrf_exempt
def doctor_list(request):
    if request.method == 'GET':
        doctors = Doctor.objects.all()
        serializer = DoctorSerializers(doctors, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DoctorSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def doctor_detail(request, doctor_id):
    try:
        doctor = Doctor.objects.get(pk=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=404)

    if request.method == 'GET':
        serializer = DoctorSerializers(doctor)
        return JsonResponse(serializer.data, status=200)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DoctorSerializers(doctor, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        doctor.delete()
        return HttpResponse(status=204)


@csrf_exempt
def Patient_list(request):
    if request.method == 'GET':
        patient_list = Patient.objects.all()
        serialize_Patient_list = PatientSerializers(patient_list, many=True)
        return JsonResponse(serialize_Patient_list.data, safe=False, status=200)
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        patient_add_serializer = PatientSerializers(data=request_data)
        if patient_add_serializer.is_valid():
            patient_add_serializer.save()
            return JsonResponse(patient_add_serializer.data, status=201)

        return JsonResponse(patient_add_serializer.errors, status=400)


@csrf_exempt
def Patient_details_view(request, passed_id):
    patient_details = Patient.objects.get(id=passed_id)
    if request.method == 'GET':
        serialize_patient_details_list = PatientSerializers(patient_details)
        return JsonResponse(serialize_patient_details_list.data, safe=False, status=200)
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        patient_edit_serializer = PatientSerializers(patient_details, data=request_data)
        if patient_edit_serializer.is_valid():
            patient_edit_serializer.save()
            return JsonResponse(patient_edit_serializer.data, status=200)
        else:
            return JsonResponse(patient_edit_serializer.errors, status=400)
    elif request.method == 'DELETE':
        patient_details.delete()
        return HttpResponse(status=204)


@csrf_exempt
def Doctor_Availability_view(request):
    if request.method == 'GET':
        doctor_availability = DoctorAvailability.objects.all()
        serialize_doctor_availability = DoctorAvalabilitySerializers(doctor_availability, many=True)
        return JsonResponse(serialize_doctor_availability.data, safe=False, status=200)
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        doctor_availability_add_serializer = DoctorAvalabilitySerializers(data=request_data)
        if doctor_availability_add_serializer.is_valid():
            doctor_availability_add_serializer.save()
            return JsonResponse(doctor_availability_add_serializer.data, status=201)

        return JsonResponse(doctor_availability_add_serializer.errors, status=400)


@csrf_exempt
def Doctor_Availability_details_view(request, passed_id):
    doctor_availability = DoctorAvailability.objects.get(id=passed_id)
    if request.method == 'GET':
        serialize_doctor_availability = DoctorAvalabilitySerializers(doctor_availability)
        return JsonResponse(serialize_doctor_availability.data, safe=False, status=200)
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        doctor_availability_edit_serializer = DoctorAvalabilitySerializers(doctor_availability, data=request_data)
        if doctor_availability_edit_serializer.is_valid():
            doctor_availability_edit_serializer.save()
            return JsonResponse(doctor_availability_edit_serializer.data, status=200)
        else:
            return JsonResponse(doctor_availability_edit_serializer.errors, status=400)
    elif request.method == 'DELETE':
        doctor_availability.delete()
        return HttpResponse(status=204)


@csrf_exempt
def Appointment_view(request):
    if request.method == 'GET':
        appointment_list = Appointment.objects.all()
        serialize_appointment_list = AppointmentSerializers(appointment_list, many=True)
        return JsonResponse(serialize_appointment_list.data, safe=False, status=200)
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        appointment_list_add_serializer = AppointmentSerializers(data=request_data)
        if appointment_list_add_serializer.is_valid():
            appointment_list_add_serializer.save()
            return JsonResponse(appointment_list_add_serializer.data, status=201)

        return JsonResponse(appointment_list_add_serializer.errors, status=400)


@csrf_exempt
def Appointment_details_view(request, passed_id):
    appointment_list_view = Appointment.objects.get(id=passed_id)
    if request.method == 'GET':
        serialize_appointment_list_view = AppointmentSerializers(appointment_list_view)
        return JsonResponse(serialize_appointment_list_view.data, safe=False, status=200)
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        appointment_list_view_edit_serializer = AppointmentSerializers(appointment_list_view, data=request_data)
        if appointment_list_view_edit_serializer.is_valid():
            appointment_list_view.save()
            return JsonResponse(appointment_list_view_edit_serializer.data, status=200)
        else:
            return JsonResponse(appointment_list_view_edit_serializer.errors, status=400)
    elif request.method == 'DELETE':
        appointment_list_view.delete()
        return HttpResponse(status=204)


@csrf_exempt
def Appointment_bill_view(request):
    if request.method == 'GET':
        appointment_bill = AppointmentBill.objects.all()
        serialize_appointment_bill = AppointmentBillSerializers(appointment_bill, many=True)
        return JsonResponse(serialize_appointment_bill.data, safe=False, status=200)
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        appointment_bill_add_serializer = AppointmentBillSerializers(data=request_data)
        if appointment_bill_add_serializer.is_valid():
            appointment_bill_add_serializer.save()
            return JsonResponse(appointment_bill_add_serializer.data, status=201)
        return JsonResponse(appointment_bill_add_serializer.errors, status=400)


@csrf_exempt
def Appointment_bill_details_view(request, passed_id):
    appointment_bill = AppointmentBill.objects.get(id=passed_id)
    if request.method == 'GET':
        serialize_appointment_bill = AppointmentBillSerializers(appointment_bill)
        return JsonResponse(serialize_appointment_bill.data, safe=False, status=200)
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        appointment_bill_edit_serializer = AppointmentBillSerializers(appointment_bill, data=request_data)
        if appointment_bill_edit_serializer.is_valid():
            appointment_bill_edit_serializer.save()
            return JsonResponse(appointment_bill_edit_serializer.data, status=200)
        else:
            return JsonResponse(appointment_bill_edit_serializer.errors, status=400)
    elif request.method == 'DELETE':
        appointment_bill.delete()
        return HttpResponse(status=204)


@csrf_exempt
def Test_list(request):
    try:
        if request.method == 'GET':
            test_list = Test.objects.all()
            serialize_test_list = TestSerializers(test_list, many=True)
            return JsonResponse(serialize_test_list.data, safe=False, status=200)
        elif request.method == 'POST':
            request_data = JSONParser().parse(request)
            test_add_serializer = TestSerializers(data=request_data)
            if test_add_serializer.is_valid():
                test_add_serializer.save()
                return JsonResponse(test_add_serializer.data, status=201)

            return JsonResponse(test_add_serializer.errors, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def Test_details_view(request, passed_id):
    try:
        test_details = Test.objects.get(id=passed_id)
        if request.method == 'GET':
            serialize_test_details_list = TestSerializers(test_details)
            return JsonResponse(serialize_test_details_list.data, safe=False, status=200)
        elif request.method == 'PUT':
            request_data = JSONParser().parse(request)
            test_edit_serializer = TestSerializers(test_details, data=request_data)
            if test_edit_serializer.is_valid():
                test_edit_serializer.save()
                return JsonResponse(test_edit_serializer.data, status=200)
            else:
                return JsonResponse(test_edit_serializer.errors, status=400)
        elif request.method == 'DELETE':
            test_details.delete()
            return HttpResponse(status=204)
    except Test.DoesNotExist:
        return JsonResponse({'error': 'Test not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def Medicine_list(request):
    try:
        if request.method == 'GET':
            medicine_list = Medicine.objects.all()
            serialize_medicine_list = MedicineSerializers(medicine_list, many=True)
            return JsonResponse(serialize_medicine_list.data, safe=False, status=200)
        elif request.method == 'POST':
            request_data = JSONParser().parse(request)
            medicine_add_serializer = MedicineSerializers(data=request_data)
            if medicine_add_serializer.is_valid():
                medicine_add_serializer.save()
                return JsonResponse(medicine_add_serializer.data, status=201)

            return JsonResponse(medicine_add_serializer.errors, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def Medicine_details_view(request, passed_id):
    try:
        medicine_details = Medicine.objects.get(id=passed_id)
        if request.method == 'GET':
            serialize_medicine_details_list = MedicineSerializers(medicine_details)
            return JsonResponse(serialize_medicine_details_list.data, safe=False, status=200)
        elif request.method == 'PUT':
            request_data = JSONParser().parse(request)
            medicine_edit_serializer = MedicineSerializers(medicine_details, data=request_data)
            if medicine_edit_serializer.is_valid():
                medicine_edit_serializer.save()
                return JsonResponse(medicine_edit_serializer.data, status=200)
            else:
                return JsonResponse(medicine_edit_serializer.errors, status=400)
        elif request.method == 'DELETE':
            medicine_details.delete()
            return HttpResponse(status=204)
    except Medicine.DoesNotExist:
        return JsonResponse({'error': 'Medicine not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def medicine_detail(request, medicine_id):
    try:
        medicine = Medicine.objects.get(id=medicine_id)
    except Medicine.DoesNotExist:
        return JsonResponse({'error': 'Medicine not found'}, status=404)

    if request.method == 'GET':
        serializer = MedicineSerializers(medicine)
        return JsonResponse(serializer.data, safe=False, status=200)

    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        serializer = MedicineSerializers(medicine, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        medicine.delete()
        return HttpResponse(status=204)


@csrf_exempt
def medicine_history_list(request):
    if request.method == 'GET':
        medicine_histories = MedicineHistory.objects.all()
        serializer = MedicineHistorySerializer(medicine_histories, many=True)
        return JsonResponse(serializer.data, safe=False, status=200)
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        serializer = MedicineHistorySerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def medicine_history_detail(request, passed_id):
    try:
        medicine_history = MedicineHistory.objects.get(id=passed_id)
    except MedicineHistory.DoesNotExist:
        return JsonResponse({'error': 'MedicineHistory not found'}, status=404)

    if request.method == 'GET':
        serializer = MedicineHistorySerializer(medicine_history)
        return JsonResponse(serializer.data, safe=False, status=200)

    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        serializer = MedicineHistorySerializer(medicine_history, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        medicine_history.delete()
        return HttpResponse(status=204)




@csrf_exempt
def Lab_bill(request):
    if request.method == 'GET':
        lab_bill = LabBill.objects.all()
        serialize_lab_bill = LabBillSerializer(lab_bill, many=True)
        return JsonResponse(serialize_lab_bill.data, safe=False, status=200)
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        lab_bill_add_serializer = LabBillSerializer(data=request_data)
        if lab_bill_add_serializer.is_valid():
            lab_bill_add_serializer.save()
            return JsonResponse(lab_bill_add_serializer.data, status=201)

        return JsonResponse(lab_bill_add_serializer.errors, status=400)


@csrf_exempt
def Lab_bill_details(request, passed_id):
    lab_bill_details = LabBill.objects.get(id=passed_id)
    if request.method == 'GET':
        serialize_Lab_bill_details = LabBillSerializer(lab_bill_details)
        return JsonResponse(serialize_Lab_bill_details.data, safe=False, status=200)
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        lab_bill_details_edit_serializer = LabBillSerializer(lab_bill_details, data=request_data)
        if lab_bill_details_edit_serializer.is_valid():
            lab_bill_details_edit_serializer.save()
            return JsonResponse(lab_bill_details_edit_serializer.data, status=200)
        else:
            return JsonResponse(lab_bill_details_edit_serializer.errors, status=400)
    elif request.method == 'DELETE':
        lab_bill_details.delete()
        return HttpResponse(status=204)
@csrf_exempt
def Lab_report_list(request):
    if request.method == 'GET':
        lab_report_list = LabReport.objects.all()
        serialize_lab_report = LabReportSerializer(lab_report_list, many=True)
        return JsonResponse(serialize_lab_report.data, safe=False, status=200)
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        lab_report_add_serializer = LabReportSerializer(data=request_data)
        if lab_report_add_serializer.is_valid():
            lab_report_add_serializer.save()
            return JsonResponse(lab_report_add_serializer.data, status=201)

        return JsonResponse(lab_report_add_serializer.errors, status=400)


@csrf_exempt
def Lab_report_details(request, passed_id):
    lab_report_details = LabReport.objects.get(id=passed_id)
    if request.method == 'GET':
        serialize_Lab_report_details = LabReportSerializer(lab_report_details)
        return JsonResponse(serialize_Lab_report_details.data, safe=False, status=200)
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        lab_report_details_edit_serializer = LabReportSerializer(lab_report_details, data=request_data)
        if lab_report_details_edit_serializer.is_valid():
            lab_report_details_edit_serializer.save()
            return JsonResponse(lab_report_details_edit_serializer.data, status=200)
        else:
            return JsonResponse(lab_report_details_edit_serializer.errors, status=400)
    elif request.method == 'DELETE':
        lab_report_details.delete()
        return HttpResponse(status=204)


@csrf_exempt
def Medicine_Bills(request):
    try:
        if request.method == 'GET':
            medicine_bills = MedicineBill.objects.all()
            # medicine_bills = MedicinePrescription.objects.all()
            # serialize_medicine_bill = MedicineBillSerializers(medicine_bills, many=True)
            serialize_medicine_bill = MedicineBillSerializers(medicine_bills, many=True)
            return JsonResponse(serialize_medicine_bill.data, safe=False, status=200)
        elif request.method == 'POST':
            request_data = JSONParser().parse(request)
            medicine_billing_serializer = MedicineBillSerializers(data=request_data)
            if medicine_billing_serializer.is_valid():
                medicine_billing_serializer.save()
                return JsonResponse(medicine_billing_serializer.data, status=201)

            return JsonResponse(medicine_billing_serializer.errors, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def medicine_bill_detail(request, passed_id):
    medicine_bill_details = MedicineBill.objects.get(id=passed_id)
    if request.method == 'GET':
        serialize_medicine_bill_details= MedicineBillSerializers(medicine_bill_details)
        return JsonResponse(serialize_medicine_bill_details.data, safe=False, status=200)
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        medicine_bill_details_edit_serializer = MedicineBillSerializers(medicine_bill_details, data=request_data)
        if medicine_bill_details_edit_serializer.is_valid():
            medicine_bill_details_edit_serializer.save()
            return JsonResponse(medicine_bill_details_edit_serializer.data, status=200)
        else:
            return JsonResponse(medicine_bill_details_edit_serializer.errors, status=400)
    elif request.method == 'DELETE':
        medicine_bill_details.delete()
        return HttpResponse(status=204)


@csrf_exempt
def prescription_detail_list(request):
    if request.method == 'GET':
        prescription_details_list = PrescriptionDetail.objects.all()
        serialize_prescription_details_list = PrescriptionDetailSerializer(prescription_details_list, many=True)
        return JsonResponse(serialize_prescription_details_list.data, safe=False, status=200)
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        prescription_detail_add_serializer = PrescriptionDetailSerializer(data=request_data)
        if prescription_detail_add_serializer.is_valid():
            prescription_detail_add_serializer.save()
            return JsonResponse(prescription_detail_add_serializer.data, status=201)

        return JsonResponse(prescription_detail_add_serializer.errors, status=400)


@csrf_exempt
def prescription_detail_detail(request, passed_id):
    Prescription_details = PrescriptionDetail.objects.get(id=passed_id)
    if request.method == 'GET':
        serialize_prescription_details= PrescriptionDetailSerializer(Prescription_details)
        return JsonResponse(serialize_prescription_details.data, safe=False, status=200)
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        prescription_details_edit_serializer = PrescriptionDetailSerializer(Prescription_details, data=request_data)
        if prescription_details_edit_serializer.is_valid():
            prescription_details_edit_serializer.save()
            return JsonResponse(prescription_details_edit_serializer.data, status=200)
        else:
            return JsonResponse(prescription_details_edit_serializer.errors, status=400)
    elif request.method == 'DELETE':
        Prescription_details.delete()
        return HttpResponse(status=204)
@csrf_exempt
def medicine_quantity_list(request):
    if request.method == 'GET':
        medicine_quantity_lists = MedicineQuantity.objects.all()
        serialize_prescription_details_list = MedicineQuantitySerializer(medicine_quantity_lists, many=True)
        return JsonResponse(serialize_prescription_details_list.data, safe=False, status=200)
    elif request.method == 'POST':
        request_data = JSONParser().parse(request)
        medicine_quantity_add_serializer = MedicineQuantitySerializer(data=request_data)
        if medicine_quantity_add_serializer.is_valid():
            medicine_quantity_add_serializer.save()
            return JsonResponse(medicine_quantity_add_serializer.data, status=201)

        return JsonResponse(medicine_quantity_add_serializer.errors, status=400)


@csrf_exempt
def medicine_quantity_detail(request, passed_id):
    medicine_quantity_details = MedicineQuantity.objects.get(id=passed_id)
    if request.method == 'GET':
        serialize_prescription_details= MedicineQuantitySerializer(medicine_quantity_details)
        return JsonResponse(serialize_prescription_details.data, safe=False, status=200)
    elif request.method == 'PUT':
        request_data = JSONParser().parse(request)
        medicine_quantity_details_edit_serializer = MedicineQuantitySerializer(medicine_quantity_details, data=request_data)
        if medicine_quantity_details_edit_serializer.is_valid():
            medicine_quantity_details_edit_serializer.save()
            return JsonResponse(medicine_quantity_details_edit_serializer.data, status=200)
        else:
            return JsonResponse(medicine_quantity_details_edit_serializer.errors, status=400)
    elif request.method == 'DELETE':
        medicine_quantity_details.delete()
        return HttpResponse(status=204)