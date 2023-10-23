from datetime import date
from django.utils import timezone
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
    landlord = models.ForeignKey(
        LandLord, on_delete=models.CASCADE, null=True, blank=True)
    house_number = models.CharField(max_length=10)
    house_type = models.CharField(max_length=20, choices=HOUSE_TYPE_CHOICES)
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    deposit = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(choices=STATUS_CHOICES, default=False)
    image = models.ImageField(upload_to="house/images", null=True)

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
    house = models.ForeignKey(
        House, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="tenants/images", null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class PaymentPremiums(models.Model):
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('pending', 'Pending'),
        ('defaulted', 'Defaulted'),
    ]

    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    due_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Payment Premium {self.tenant.first_name} {self.tenant.last_name} - {self.due_date}"

    def calculate_adjusted_premium(self):
        monthly_rent = Decimal(self.amount)

        if self.tenant.payments.filter(status="processed").exists():
            total_paid = self.tenant.payments.filter(status="processed").aggregate(
                models.Sum('amount_paid'))['amount_paid__sum']
            if total_paid is not None:
                balance = monthly_rent - total_paid
                if balance > 0:
                    monthly_rent -= balance
        return monthly_rent


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = (
        ("cash", "Cash"),
        ("mpesa", "Mpesa"),
    )
    PAYMENT_STATUS_CHOICES = [
        ('processed', 'Processed'),
        ('failed', 'Failed'),
    ]
    tenant = models.ForeignKey(
        Tenant, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.CharField(
        max_length=100, choices=PAYMENT_METHOD_CHOICES, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    amount_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0)
    status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    date_paid = models.DateField()
    payment_premium = models.ForeignKey(
        PaymentPremiums, on_delete=models.SET_NULL, null=True, blank=True)

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

    @property
    def rent_arrears(self):
        if self.amount_paid and self.payment_premium:
            # Calculate rent_arrears based on the difference between amount_paid and amount
            premium_amount = self.payment_premium.amount
            amount_paid = self.amount_paid
            return premium_amount - amount_paid

        return None  # Handle the case where payment or payment_premium is not present
