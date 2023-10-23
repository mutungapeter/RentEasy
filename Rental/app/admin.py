from django.contrib import admin
from .models import *

# Register your models here.

class HouseAdmin(admin.ModelAdmin):
    list_display = ('landlord', 'house_number', 'house_type', 'rent', 'deposit', 'status', 'image')

admin.site.register(House, HouseAdmin)

class TenantAdmin(admin.ModelAdmin):
    list_display = ('landlord','id','id_number', 'first_name', 'last_name', 'phone_number', 'occupation_date', 'house')
    
admin.site.register(Tenant, TenantAdmin)

class LandLordAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_number', 'full_name', 'phone_number')
    
admin.site.register(LandLord, LandLordAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'phone_number','payment_method', 'amount_paid', 'status', 'date_paid', 'rent_arrears')
   
admin.site.register(Payment, PaymentAdmin)


class PaymentPremiumsAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'amount', 'due_date', 'status')

admin.site.register(PaymentPremiums, PaymentPremiumsAdmin)

