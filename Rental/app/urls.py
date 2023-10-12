from django.urls import path
from .views import HouseDetailView, HousListView, TenantListView, TenantDetailView, RentPaymentListView, PaymentDetailView
from.import views

urlpatterns = [
    path('', views.home, name='home'),
    path('properties/', HousListView.as_view(), name='property_list'),
    path('property/<int:pk>/', HouseDetailView.as_view(), name='property_detail'),
    path('tenants/', TenantListView.as_view(), name='tenant_list'),
    path('payments/', RentPaymentListView.as_view(), name='payment_list'),
    path('payment/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
    path('tenant/<int:pk>/', TenantDetailView.as_view(), name='tenant_detail'),
]
