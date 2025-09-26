from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  # show login page first
    path('home/', views.home, name='home'),    # optional: home page
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
]