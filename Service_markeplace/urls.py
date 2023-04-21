"""Service_markeplace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.urls import reverse
from django.conf.urls.static import static
from django.conf import settings
from Service.views import *
from django.urls import path, include
# from mpesa.urls import mpesa_urls  stk_push_success



urlpatterns = [
    re_path('admin/', admin.site.urls),
    path('logout_view/', logout_view, name='logout_view'),
    path('change_password/<int:id>', change_password, name='change_password'),

    # mpesa
    path('oauth_success/', oauth_success, name='oauth_success'),
    path('stk_push_success/', stk_push_success, name='stk_push_success'),
    # path('mpesa/', include(mpesa_urls)),
    # index
    path('', index),    
    # auth and accounts
    re_path('signin/', signin, name='signin'),
    path('customersignup/', customer_signup, name='customersignup'),
    path('business.signup/', business_signup, name='business.signup'),

    # business
    path('business_home/', business_home, name='business_home'),
    path('dealings/', dealings, name='dealings'),
    path('business_location/', business_location, name='business_location'),
    path('customer_location/', customer_location, name='customer_location'),
    
    

    # customer
    path('customer_home/', customer_home, name='customer_home'),
    path('products/', products, name='products'),
    path('product_detail/<int:pk>', product_detail, name='product_detail'),
    path('services/', services, name='services'),
    path('service_discount/', service_discount, name='service_discount'),
    path('product_discount/', product_discount, name='product_discount'),
    path('service_detail/<int:pk>', service_detail, name='service_detail'),
    path('schedule_service/<int:pk>', schedule_service, name='schedule_service'),
    path('enquiry_home/', inquire_home, name='inquire_home'),
    path('service_enquire/<int:pk>', service_enquire, name='service_enquire'),
    path('enquiry_response/<int:pk>/', enquiry_response, name='enquiry_response'),
    path('service_rating/<int:pk>/', service_rating, name='service_rating'),
    path('product_rating/<int:pk>/', product_rating, name='product_rating'),
    path('checkout/<int:pk>', checkout, name='checkout'),
    path('invoices/', invoices, name='invoices'),
    path('download_invoice/', download_invoice, name='download_invoice'),
    path('customer_profile/', customer_profile, name='customer_profile'),

    # business admin
    path('add_product/', add_product, name='add_product'),
    path('add_service/', add_service, name='add_service'),
    path('product_discount/', product_discount, name='product_discount'),
    path('service_discount/', service_discount, name='service_discount'),
    path('bulk_emails/', bulk_emails, name='bulk_emails'),
    path('posters/', posters, name='posters'),
    path('profile/', profile, name='profile'),
    path('today_query/', today_query, name='today_query'),
    path('today_service/', today_service, name='today_service'),
    path('from_to_query/', from_to_query, name='from_to_query'),
    path('checked_out/<int:pk>/', sale_status, name='checked_out'),
    path('from_to_query/', from_to_query, name='from_to_query'),
    path('from_to_schedule/', from_to_schedule, name='from_to_schedule'),
    path('sales_data/', sales_data, name='sales_data'),

    # reports
    path('reports/', reports, name='reports'),
    path('generate_report/', generate_report, name='generate_report'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)