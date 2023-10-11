from django.contrib import admin
from .models import Account
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
     list_display = ('first_name', 'last_name', 'username', 'email', 'phone_number', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'is_active', 'is_superadmin', 'is_tenant', 'is_landlord')
 

admin.site.register(Account, AccountAdmin)