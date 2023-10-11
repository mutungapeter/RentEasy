from django.contrib import admin
from .models import *

# Register your models here.

class HouseAdmin(admin.ModelAdmin):
    list_display = ('landlord', 'house_number', 'house_type', 'rent', 'deposit', 'status',)

admin.site.register(House, HouseAdmin)

class TenantAdmin(admin.ModelAdmin):
    list_display = ('landlord','id_number', 'first_name', 'last_name', 'phone_number', 'occupation_date', 'house')
    
admin.site.register(Tenant, TenantAdmin)

class LandLordAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_number', 'first_name', 'last_name', 'phone_number')
    
admin.site.register(LandLord, LandLordAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'house', 'amount_due', 'amount_paid', 'date_paid', 'rent_arrears',)
   
admin.site.register(Payment, PaymentAdmin)
