from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView
from .models import House, Tenant, Payment, PaymentPremiums
from .paymentsHandler import Mark_oldest_premium, mark_oldest_premium_using_payment
from accounts.models import Account
from .mpesaHandler import initiate_payment
from django.http import HttpResponse, JsonResponse
import requests
import json
import uuid

class TestView(View):
    def get(self, request, tenant_id, payment_id):
        oldest_premium = Mark_oldest_premium(tenant_id)
        result = mark_oldest_premium_using_payment(payment_id)
        print(oldest_premium)
        return HttpResponse(f"Oldest Premium: {oldest_premium}\nResult: {result}")
class MpesaPaymentView(View):
    # def get(self, request, *args, **kwargs):
    #     return render(request, 'payments/payments.html')

    def post(self, request, *args, **kwargs):
        # Generate a unique transaction ID
        transaction_id = uuid.uuid4().hex  # Use a suitable method to generate a transaction ID

        amount = request.POST.get('amount_paid')
        phone_number = request.POST.get('phone_number')

        # Call a function to initiate the payment
        success, response = initiate_payment(transaction_id, amount, phone_number)

        if success:
            # Payment initiated successfully, save payment details to the database
            payment = Payment.objects.create(
                transaction_id=transaction_id,
                amount=amount,
                phone_number=phone_number
            )
            payment.save()
            payment_handler_result = mark_oldest_premium_using_payment(payment.id)

            return JsonResponse({'message': 'Payment initiated successfully!', 'payment_handler_result': payment_handler_result})
        else:
            return JsonResponse({'error': 'Failed to initiate payment'})
      
class MpesaCallbackView(View):
    def post(self, request, *args, **kwargs):
        # Retrieve the callback data from the request
        callback_data = json.loads(request.body.decode('utf-8'))
        print("callbackData ->:",callback_data)

        # Process the callback data
        success = callback_data.get('ResultCode') == '0'
        print(success)

        if success:
            # Payment was successful, update the payment status in your database
            transaction_id = callback_data.get('TransactionID')
            try:
                # Assuming 'transaction_id' is a unique identifier for your payment
                payment = Payment.objects.get(transaction_id=transaction_id)
                payment.status = 'paid'  # Update the status to indicate a successful payment
                payment.save()
                return HttpResponse(status=200, content="Payment status updated successfully")
            except Payment.DoesNotExist:
                return HttpResponse(status=400, content="Payment not found for the given transaction ID")
        else:
            # Payment was not successful
            # log out

            # Respond with an error message
            return HttpResponse(status=400, content="Callback processing failed")



class PaymentView(View):
       def get(self, request, *args, **kwargs):
        return render(request, 'payments/payments.html')  
       
def home(request):
    return render(request, 'accounts/login.html')

class HousListView(ListView):
    model = House
    template_name = 'houses/property_list.html'
    context_object_name = 'properties'

    def get_queryset(self):
        return House.objects.filter(landlord__user=self.request.user)

class HouseDetailView(DetailView):
    model = House
    template_name = 'houses/property_detail.html'
    context_object_name = 'property'

class TenantListView(ListView):
    model = Tenant
    template_name = 'tenants/tenants_list.html'
    context_object_name = 'tenants'

    def get_queryset(self):
        return Tenant.objects.filter(landlord__user=self.request.user)
 
class TenantDetailView(DetailView):
    model = Tenant
    template_name = 'tenants/tenant_detail.html'
    context_object_name = 'tenant'
    
class RentPaymentListView(ListView):
    model = Payment
    template_name = 'payments/payments_list.html'
    context_object_name = 'payments'

    def get_queryset(self):
        return Payment.objects.filter(tenant__landlord__user=self.request.user)
class PaymentPremiumListView(ListView):
    model = PaymentPremiums
    template_name = 'payments/payment_premiums.html'
    context_object_name = 'payment_premiums'

    def get_queryset(self):
        return PaymentPremiums.objects.filter(tenant__landlord__user=self.request.user)
class PaymentDetailView(DetailView):
    model = Payment
    template_name = 'payments/payment_detail.html'
    context_object_name = 'payment'

class RentArrearsListView(ListView):
    model = Payment
    template_name = 'payments/rent_arrears.html'
    context_object_name = 'rent_arrears'

    def get_queryset(self):
        return Payment.objects.filter(tenant__user=self.request.user)