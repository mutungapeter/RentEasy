from datetime import date
from decimal import Decimal
from django.db import models
from accounts.models import Account

class LandLord(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
 
    def __str__(self):
        return self.user.first_name
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
class House(models.Model):
    HOUSE_TYPE_CHOICES = [
        ('single', 'Single'),
        ('bedsitter', 'Bedsitter'),
        ('one_bedroom', 'One Bedroom'),
        ('two_bedrooms', 'Two Bedrooms'),
    ]
    STATUS_CHOICES = [
        (True, 'Occupied'),
        (False, 'Vacant'),
    ]
    landlord = models.ForeignKey(LandLord, on_delete=models.CASCADE, null=True, blank=True)
    house_number = models.CharField(max_length=10)
    house_type = models.CharField(max_length=20, choices=HOUSE_TYPE_CHOICES)  
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(choices=STATUS_CHOICES, default=False) 
    

    def __str__(self):
        return self.house_number
    
    def calculate_amount_due(self):
        # Calculate the amount due based on the property's rent
        return Decimal(self.rent)  # Monthly rent

    
class Tenant(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE, null=True)
    landlord = models.ForeignKey(LandLord, on_delete=models.CASCADE)
    id_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    occupation_date = models.DateField()
    house = models.ForeignKey(House, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, editable=False)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date_paid = models.DateField()
    rent_arrears = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, editable=False)

    def __str__(self):
        return f"Rent payment for {self.tenant.first_name} {self.tenant.last_name}"
        

    @property
    def tenant_phone_number(self):
        return self.tenant.phone_number

    @property
    def tenant_id_number(self):
        return self.tenant.id_number

    @property
    def tenant_first_name(self):
        return self.tenant.first_name

    @property
    def tenant_last_name(self):
        return self.tenant.last_name

    def save(self, *args, **kwargs):
        if self.house:
            # Set amount_due based on the property's rent
            self.amount_due = self.house.rent

            # Calculate rent_arrears based on the amount_due and amount_paid
            self.rent_arrears = self.amount_due - self.amount_paid

        super().save(*args, **kwargs)