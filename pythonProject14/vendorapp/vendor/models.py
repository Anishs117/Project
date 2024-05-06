from django.db import models
from django.db.models import Count, Avg, F, ExpressionWrapper, DecimalField
from django.utils import timezone


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name



    def update_performance_metrics(self):
        # On-Time Delivery Rate
        completed_pos = self.purchaseorder_set.filter(status='completed')
        total_completed_pos = completed_pos.count()
        on_time_delivery_count = completed_pos.filter(delivery_date__lte=F('issue_date')).count()
        self.on_time_delivery_rate = (
                                                 on_time_delivery_count / total_completed_pos) * 100 if total_completed_pos != 0 else 0.0

        # Quality Rating Average
        self.quality_rating_avg = \
        completed_pos.filter(quality_rating__isnull=False).aggregate(avg_rating=Avg('quality_rating'))[
            'avg_rating'] or 0.0

        # Average Response Time
        response_time = ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DecimalField())
        avg_response_time = self.purchaseorder_set.filter(acknowledgment_date__isnull=False).annotate(
            response_time=response_time).aggregate(avg_response=Avg('response_time'))['avg_response']
        self.average_response_time = avg_response_time.total_seconds() / 3600 if avg_response_time else 0.0

        # Fulfilment Rate
        total_pos = self.purchaseorder_set.count()
        successful_pos = self.purchaseorder_set.filter(status='completed').count()
        self.fulfillment_rate = (successful_pos / total_pos) * 100 if total_pos != 0 else 0.0

        self.save()


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.delivery_date:
            self.delivery_date = timezone.now()
        super().save(*args, **kwargs)
        self.vendor.update_performance_metrics()


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"


from django.db import models

# Create your models here.
