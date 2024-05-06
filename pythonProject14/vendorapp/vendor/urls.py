from django.urls import path
from .views import add_vendor, get_vendors, get_vendor_by_id, delete_vendor, update_vendor, get_purchase_order,\
    get_purchase_order_by, add_purchase_order, update_purchase_order ,delete_purchase_order,get_vendor_performance
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/vendor/',get_vendors ,name='vendor_list'),
    path('api/vendor/post/',add_vendor ,name='vendor_post'),
    path('api/vendor/<int:vendor_id>/', get_vendor_by_id, name='get-vendor-by-id'),
    path('api/vendor/delete/<int:vendor_id>/', delete_vendor, name='delete-vendor-by-id'),
    path('api/vendor/update/<int:vendor_id>/', update_vendor, name='update-vendor-by-id'),

    path('api/purchaseorder/',get_purchase_order ,name='purchase_order'),
    path('api/purchaseorder/<int:vendor_id>/', get_purchase_order_by, name='get-purchase-by-id'),
    path('api/purchaseorder/post/',add_purchase_order ,name='add_purchase_order'),
    path('api/purchaseorder/update/<int:po_number>/', update_purchase_order, name='update-purchase-by-id'),
    path('api/purchaseorder/delete/<str:po_number>/', delete_purchase_order, name='delete-purchase-by-id'),
    path('api/vendors/<int:vendor_id>/performance/', get_vendor_performance, name='get-vendor-performance'),

]


