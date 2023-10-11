from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import House, Tenant, Payment

def home(request):
    return render(request, 'index.html')

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

class RentPaymentListView(ListView):
    model = Payment
    template_name = 'payments/payments_list.html'
    context_object_name = 'payments'

    def get_queryset(self):
        return Payment.objects.filter(tenant__landlord__user=self.request.user)
    
class TenantDetailView(DetailView):
    model = Tenant
    template_name = 'tenants/tenant_detail.html'
    context_object_name = 'tenant'
