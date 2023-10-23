from .models import PaymentPremiums,Payment,Tenant
from accounts.models import Account

def Mark_oldest_premium(tenant_id):
    # return None
    tenant = Tenant.objects.get(id=tenant_id)
    if tenant:
        unpaid_premiums = PaymentPremiums.objects.filter(tenant=tenant, status__in=["unpaid", "pending"]).order_by('due_date').first()
        if unpaid_premiums:
            oldest_premium = unpaid_premiums
            return oldest_premium
        print(unpaid_premiums)
    return None
    
def mark_oldest_premium_using_payment(payment_id):
    payment = Payment.objects.get(id=payment_id)
    if payment:
        oldest_premium = Mark_oldest_premium(payment.tenant.id)
        if oldest_premium:
            balance = payment.amount_paid - oldest_premium.amount
            if balance >= 0:
                #Payment covers the premium
                oldest_premium.status= "paid"
                oldest_premium.save()
                if balance > 0:
                    # Excess Payment 
                    return f"Premium marked as paid. Excess payment: {balance}"
                else:
                    return f"Premium marked as paid. No balance."
            else:
                #Payment is less than the premium
                return f"Payment Received . but the premium is not fully covered. Remaining balance: {abs(balance)}"
    return f"No unpaid premiums found."
   