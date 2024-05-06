from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import VendorSerializer, CreateVendorSerializer, PurchaseOrderSerializer, CreatePurchaseOrderSerializer, VendorPerformanceSerializer
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Vendor, PurchaseOrder

@swagger_auto_schema(
    method='post',
    operation_summary='Add Vendor',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'contact_details', 'address'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Full name'),
            'contact_details': openapi.Schema(type=openapi.TYPE_STRING, description='contact_details'),
            'address': openapi.Schema(type=openapi.TYPE_STRING, description='address'),
            # 'vendor_code': openapi.Schema(type=openapi.TYPE_STRING, description='vendor_code'),

        },
    ),
    responses={
        status.HTTP_201_CREATED: 'vendor created successfully',
        status.HTTP_400_BAD_REQUEST: 'Bad request (e.g., missing required fields)',
    }
)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def add_vendor(request):
    if request.method == 'POST':
        serializer = CreateVendorSerializer(data=request.data)
        if serializer.is_valid():
            last_vendor = Vendor.objects.order_by('-id').first()
            if last_vendor:
                last_vendor_code = last_vendor.vendor_code
                try:
                    last_number = int(last_vendor_code.split('-')[1])
                except (ValueError, IndexError):
                    last_number = 0
                new_number = last_number + 1
                vendor_code = f"VC-{str(new_number).zfill(3)}"
            else:
                vendor_code = "VC-001"
            serializer.validated_data['vendor_code'] = vendor_code
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_vendors(request):
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_vendor_by_id(request, vendor_id):
    if request.method == 'GET':
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    vendor.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(
    method='put',
    operation_summary='Update Vendor',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['name', 'contact_details', 'address'],
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Full name'),
            'contact_details': openapi.Schema(type=openapi.TYPE_STRING, description='contact_details'),
            'address': openapi.Schema(type=openapi.TYPE_STRING, description='address'),
        },
    ),
    responses={
        status.HTTP_200_OK: 'vendor updated successfully',
        status.HTTP_400_BAD_REQUEST: 'Bad request (e.g., missing required fields)',
        status.HTTP_404_NOT_FOUND: 'Vendor not found',
    }
)
@api_view(['PUT'])
def update_vendor(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CreateVendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def get_purchase_order(request):
    if request.method == 'GET':
        purchaseorder = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchaseorder, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_purchase_order_by(request, vendor_id):
    if request.method == 'GET':
        try:
            purchaseorders = PurchaseOrder.objects.filter(vendor=vendor_id)
            serializer = PurchaseOrderSerializer(purchaseorders, many=True)
            return Response(serializer.data)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase orders not found"}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(
    method='post',
    operation_summary='Create Purchase Order',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=[ 'vendor', 'order_date', 'items', 'quantity', 'status', 'issue_date'],
        properties={
            'vendor': openapi.Schema(type=openapi.TYPE_INTEGER, description='Vendor ID'),
            'order_date': openapi.Schema(type=openapi.FORMAT_DATETIME, description='Order date in ISO 8601 format'),
            'delivery_date': openapi.Schema(type=openapi.FORMAT_DATETIME, description='Delivery date in ISO 8601 format (optional)'),
            'items': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT), description='List of items'),
            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total quantity of items'),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the purchase order'),
            'quality_rating': openapi.Schema(type=openapi.TYPE_NUMBER, description='Quality rating (optional)'),
            'issue_date': openapi.Schema(type=openapi.FORMAT_DATETIME, description='Issue date in ISO 8601 format'),
            'acknowledgment_date': openapi.Schema(type=openapi.FORMAT_DATETIME, description='Acknowledgment date in ISO 8601 format (optional)'),
        },
    ),
    responses={
        status.HTTP_201_CREATED: 'Purchase order created successfully',
        status.HTTP_400_BAD_REQUEST: 'Bad request (e.g., missing required fields)',
    }
)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def add_purchase_order(request):
    if request.method == 'POST':
        serializer = CreatePurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            last_vendor = PurchaseOrder.objects.order_by('-id').first()
            if last_vendor:
                last_vendor_code = last_vendor.po_number
                try:
                    last_number = int(last_vendor_code.split('-')[1])
                except (ValueError, IndexError):
                    last_number = 0
                new_number = last_number + 1
                po_number = f"PO-{str(new_number).zfill(3)}"
            else:
                po_number = "PO-001"
            serializer.validated_data['po_number'] = po_number
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='put',
    operation_summary='Update Purchase Order',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['po_number', 'vendor', 'order_date', 'items', 'quantity', 'status', 'issue_date'],
        properties={
            'po_number': openapi.Schema(type=openapi.TYPE_STRING, description='Purchase order number'),
            'vendor': openapi.Schema(type=openapi.TYPE_INTEGER, description='Vendor ID'),
            'order_date': openapi.Schema(type=openapi.FORMAT_DATETIME, description='Order date in ISO 8601 format'),
            'delivery_date': openapi.Schema(type=openapi.FORMAT_DATETIME, description='Delivery date in ISO 8601 format (optional)'),
            'items': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT), description='List of items'),
            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Total quantity of items'),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Status of the purchase order'),
            'quality_rating': openapi.Schema(type=openapi.TYPE_NUMBER, description='Quality rating (optional)'),
            'issue_date': openapi.Schema(type=openapi.FORMAT_DATETIME, description='Issue date in ISO 8601 format'),
            'acknowledgment_date': openapi.Schema(type=openapi.FORMAT_DATETIME, description='Acknowledgment date in ISO 8601 format (optional)'),
        },
    ),
    responses={
        status.HTTP_200_OK: 'Purchase order updated successfully',
        status.HTTP_400_BAD_REQUEST: 'Bad request (e.g., missing required fields)',
        status.HTTP_404_NOT_FOUND: 'Purchase order not found',
    }
)
@api_view(['PUT'])
def update_purchase_order(request, po_number):
    try:
        purchaseorders = PurchaseOrder.objects.get(id=po_number)
    except Vendor.DoesNotExist:
        return Response({"error": "purchaseorders not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CreatePurchaseOrderSerializer(purchaseorders, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_purchase_order(request, po_number):
    try:
        purchase_order = PurchaseOrder.objects.get(id=po_number)
    except PurchaseOrder.DoesNotExist:
        return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

    purchase_order.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def get_vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(id=vendor_id)
        serializer = VendorPerformanceSerializer(vendor)
        return Response(serializer.data)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

