from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

class CreateVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        exclude = ['vendor_code']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
class CreatePurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        exclude = ['po_number']

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source='vendor.name')

    class Meta:
        model = HistoricalPerformance
        fields = ('vendor_name', 'date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')

class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate')
