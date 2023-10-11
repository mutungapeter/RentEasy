from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required   
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views import View
from .mixins import TenantMixin, LandLordMixin

#Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# import requests
from django.template.loader import get_template
from django.views import View
from io import BytesIO
from django.http import HttpResponse

from django.views.generic import ListView
from app.models import *
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string("accounts/account_verification_email.html", {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, "Thank you for registering with us. We have have sent a verification email to your email address.Please Verify it.")
            # return HttpResponse("register successful")
            return redirect("/accounts/login/?command=verification&email="+email)
    else:
        form = RegistrationForm()
    context = {
            "form": form,
        }
    return render(request, "accounts/register.html", context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activation successful")
        return redirect("login")
    else:
        messages.error(request, "invalid activation link")
        return redirect("register")

def login(request):
    if request.method == "POST":
        # print(request.POST)
        email = request.POST["email"] 
        password = request.POST["password"]

        user = auth.authenticate(email=email, password=password)
        # print("user:", user)

        if user:
            auth.login(request, user)
            messages.success(request, "Login successful")
            return redirect('redirect_based_on_role') 
        else:
            messages.error(request, "Invalid login credentials")
            # return HttpResponse('Not authenticated')

    return render(request, "accounts/login.html")

class SelectAccountTypeView(LandLordMixin, TenantMixin, View):
    def post(self, request):
        account_type = request.POST.get('account_type')
        user = request.user
        if account_type == 'landlord':
            user.is_landlord = True
            user.is_tenant = False
            user.save()
        elif account_type == 'tenant':
            user.is_tenant = True
            user.is_landlord = False 
            user.save()

        return redirect('dashboard') 

    def get(self, request):
        return render(request, 'accounts/select_account_type.html')
    
class RedirectBasedOnRoleView(LandLordMixin, TenantMixin, View):
    def get(self, request):
        user = request.user

        if user.is_active and not user.has_selected_account():
            return redirect('select_account_type')
        elif user.is_superadmin or user.is_admin or user.is_staff:
            return redirect('dashboard')
        elif user.has_selected_account():
            return redirect('dashboard')
        elif user.is_landlord or user.is_tenant:
            return redirect('select_account_type')
        else:
            messages.success(request, "Oops! Account inactive. Please activate your account")

        return redirect('redirect_based_on_role')



def dashboard(request):
    return render(request, 'index.html')

def logout(request):
    auth.logout(request)
    messages.success(request, "You are logged out.")
    return redirect("login") 

class MyPaymentsListView(ListView):
    model = Payment
    template_name = 'accounts/my_payments_list.html'
    context_object_name = 'payments'

    def get_queryset(self):
        return Payment.objects.filter(tenant__user=self.request.user)
