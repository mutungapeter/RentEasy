from django.urls import path
from . import views
from .views import MyPaymentsListView
urlpatterns = [
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path('activate/<uidb64>/<token>/',  views.activate, name="activate"),

    path('select_account_type/', views.SelectAccountTypeView.as_view(), name='select_account_type'),
    path('redirect_based_on_role/', views.RedirectBasedOnRoleView.as_view(), name='redirect_based_on_role'),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout, name="logout"),

    path('my_payments/', MyPaymentsListView.as_view(), name='my_paymnent_list'),
]