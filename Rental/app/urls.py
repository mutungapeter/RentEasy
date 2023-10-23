from django.urls import path
from .views import HouseDetailView, HousListView, TenantListView, TenantDetailView, RentPaymentListView, MpesaPaymentView, MpesaCallbackView, PaymentDetailView, PaymentPremiumListView, TestView,PaymentView ,RentArrearsListView
from.import views

urlpatterns = [
    path('', views.home, name='home'),
    
    #Properties URLS
    path('properties/', HousListView.as_view(), name='property_list'),
    path('property/<int:pk>/', HouseDetailView.as_view(), name='property_detail'),
 
    #Tenants URLS
    path('tenants/', TenantListView.as_view(), name='tenant_list'),
    path('tenant/<int:pk>/', TenantDetailView.as_view(), name='tenant_detail'),
 
    #Payment URLS
    path('payments/', RentPaymentListView.as_view(), name='payment_list'),
    path('premiums/', PaymentPremiumListView.as_view(), name='payment_premiums_list'),
    path('payment/<int:pk>/', PaymentDetailView.as_view(), name='payment_detail'),
    path('payment_form/', PaymentView.as_view(), name='payment_form'), 
    path("test/<int:tenant_id>/<int:payment_id>/", TestView.as_view(), name="test"),

    path('arrears/', RentArrearsListView.as_view(), name='arrears_list'),


    path('process_payment/', MpesaPaymentView.as_view(), name='process_payment'),
    path('', PaymentView.as_view(), name='payment_form'), 
    path('mpesa_callback/', MpesaCallbackView.as_view(), name='mpesa_callback'),
]
