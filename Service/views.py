import os
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from decouple import config

from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib import admin

from .models import *
from .forms import *

from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from .mpesa.core import MpesaClient
from .mpesa import utils

import smtplib
import ssl
from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from email.mime.image import MIMEImage

cl = MpesaClient()
stk_push_callback_url = 'https://api.darajambili.com/express-payment'
b2c_callback_url = 'https://api.darajambili.com/b2c/result'


def oauth_success(request):
	r = cl.access_token()
	return JsonResponse(r, safe=False)

def stk_push_success(request):
	phone_number = config('LNM_PHONE_NUMBER')
	amount = 1
	account_reference = 'ABC001'
	transaction_desc = 'STK Push Description'
	callback_url = stk_push_callback_url
	r = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
	return JsonResponse(r.response_description, safe=False)

def email( subject, body, emails=[]):
    port = settings.EMAIL_PORT
    smtp_server = settings.EMAIL_HOST
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    receiver_email = emails
    # subject = 'Website registration'
    # body = 'Activate your account.'
    message = 'Subject: {}\n\n{}'.format(subject, body)
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    return 0

# def email( subject, body, attach, emails=[] ):
#     port = settings.EMAIL_PORT
#     smtp_server = settings.EMAIL_HOST
#     sender_email = settings.EMAIL_HOST_USER
#     password = settings.EMAIL_HOST_PASSWORD
#     receiver_email = emails
#     # subject = 'Website registration'
#     # body = 'Activate your account.'
#     message = 'Subject: {}\n\n{}'.format(subject, body)
#     context = ssl.create_default_context()
#     with smtplib.SMTP(smtp_server, port) as server:
#         server.ehlo()  # Can be omitted
#         server.starttls(context=context)
#         server.ehlo()  # Can be omitted
#         server.login(sender_email, password)
#         mail =  EmailMessage(subject=subject, body=message,to=[emails])
#         mail.attach(attach.name, attach.read(), attach.content_type)
#         mail.send()
                                        
#         server.sendmail(sender_email, receiver_email, message)
#     return 0

def index(request):     
    return render(request, "index/index.html", {})

def send_emails(email):
    port = settings.EMAIL_PORT
    smtp_server = settings.EMAIL_HOST
    sender_email = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    receiver_email = [email]
    subject = 'Website registration'
    body = 'Activate your account.'
    message = 'Subject: {}\n\n{}'.format(subject, body)
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    # return render(request, "business_home/NiceAdmin/send email.html", {})

#-----------for checking user iscustomer
def is_customer(user):
    return user.groups.filter(name='customer').exists()

def is_business(user):
    return user.groups.filter(name='customer').exists()

def logout_view(request):
    logout(request)
    return redirect(index)

@csrf_exempt
def change_password(request):
    user = request.user
    # user=User.objects.get(id=id)
    form = ChangePasswordForm(request.POST)
    if form.is_valid():
        print("form is valid")
        password = form.cleaned_data['password1']
        user.set_password(password)
        authenticate(username=user.username, password=password)
        user.save()
        return redirect('admin/')
        
        # return HttpResponse(reverse(profile), args=[id])
    return redirect(profile, id)    

@csrf_exempt
def signin(request):
    userForm=UserForm()
    if request.method == "POST":
        username = request.POST['username']
        password =  request.POST['password']
        user = authenticate(
    		    request, 
    		    username=username, 
    		    password=password
        )
        if user:
            login(request, user)
            if is_customer(request.user):
                messages.success(request, messages.INFO, 'you are logged in.')
                return redirect('customer_home')
            else:
                messages.success(request, messages.INFO, 'you are loged in.')
                return redirect('business_home')       

    return render(request,"auth/signin.html", {'userForm':userForm})

def customer_signup(request):
    userForm=UserForm()
    customerForm=CustomerForm()
    mydict={'userForm':userForm,'customerForm':CustomerForm}
    if request.method=='POST':
        userForm=UserForm(request.POST)
        customerForm=CustomerForm(request.POST,request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            login(request, user)
            my_customer_group = Group.objects.get_or_create(name='customer')
            my_customer_group[0].user_set.add(user)

            return redirect(customer_location)
        else:
            HttpResponse("error")
    return render(request, "auth/customersignup.html", {'userForm':userForm,'customerForm':customerForm})

@csrf_exempt
def business_signup(request):
    userForm=UserForm()
    businessForm=BusinessForm()
    mydict={'userForm':userForm,'businessForm':businessForm}
    if request.method=='POST':
        userForm=UserForm(request.POST)
        businessForm=BusinessForm(request.POST,request.FILES)
        if userForm.is_valid() and businessForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            business=businessForm.save(commit=False)
            business.user=user
            business.save()
            login(request, user)            
            my_business_group = Group.objects.get_or_create(name='businesses')
            my_business_group[0].user_set.add(user)
            return redirect(dealings)
        else:
            HttpResponse("error")
    return render(request, "auth/business.signup.html", {'userForm':userForm,'businessForm':businessForm})

@csrf_exempt
def dealings(request):
    user = request.user
    # id = request.session.get('id')
    business = Business.objects.get(user=user)
    print(business)
    dealingsForm = DealingsForm()
    if request.method=='POST':
        dealingsForm=DealingsForm(request.POST,request.FILES)
        if dealingsForm.is_valid():
            dealings=dealingsForm.save(commit=False)
            dealings.business=business
            dealings.save()
            return redirect(business_location)        
    return render(request, "auth/dealings.html", {'dealingsForm':dealingsForm})

@csrf_exempt
def business_location(request):
    user = request.user
    business = Business.objects.get(user=user)
    print(business)
    blocationForm = BusinessLocationForm()
    if request.method=='POST':
        blocationForm=BusinessLocationForm(request.POST,request.FILES)
        if blocationForm.is_valid():
            location=blocationForm.save(commit=False)
            location.business=business
            location.save()
            return redirect(signin)
    
    return render(request, "auth/business.location.html", {'blocationForm':blocationForm})

@csrf_exempt
def customer_location(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    # blocationForm = BusinessLocationForm.objects.get(pk=id)
    print(customer)
    clocationForm = CustomerLocationForm()
    if request.method=='POST':
        clocationForm=CustomerLocationForm(request.POST,request.FILES)
        if clocationForm.is_valid():
            location=clocationForm.save(commit=False)
            location.customer=customer
            location.save()
            return redirect(signin)
    
    return render(request, "auth/customer.location.html", {'clocationForm':clocationForm})

def business_home(request):
    user = request.user
    last = user.last_login
    now = datetime.datetime.now()
    business = Business.objects.get(user=user)
    business.id
    p = business.products.all()   
    # enquiries = Enquire.objects.filter(business=business)
    enquiries = Response.objects.all()
    sales = Sales.objects.all()
    products = business.products.all()

    mydict = {
        'business':business,
        'enquiries':enquiries,
        'sales':sales,
        'products':products,
        'last':last,
        'now': now
        
    }
    # return render(request, "business_home/NiceAdmin/index.html", mydict, context_instance=RequestContext(request))
    return render(request, "business_home/NiceAdmin/index.html", mydict)

@csrf_exempt
def add_product(request):
    user = request.user
    business = Business.objects.get(user=user)
    # business.product
    pForm = ProductForm()
    if request.method=='POST':
        pForm = ProductForm(request.POST, request.FILES)
        if pForm.is_valid():
            product=pForm.save(commit=False)
            product.business=business
            product.save()
            return render(request, "business_home/NiceAdmin/product.html", {'pForm':pForm})
            # return redirect(add_product)

    return render(request, "business_home/NiceAdmin/product.html", {'pForm':pForm})

@csrf_exempt
def add_service(request):
    user = request.user
    business = Business.objects.get(user=user)
    # business.product
    sForm = ServiceForm()
    if request.method=='POST':
        sForm = ServiceForm(request.POST, request.FILES)
        if sForm.is_valid():
            service=sForm.save(commit=False)
            service.business=business
            service.save()
            messages.success(request, 'Service added successfully')
            return render(request, "business_home/NiceAdmin/serviceform.html", {'sForm':sForm})
            # return redirect(add_product)

    return render(request, "business_home/NiceAdmin/serviceform.html", {'sForm':sForm})

@csrf_exempt
def product_discount(request):
    user = request.user
    business = Business.objects.get(user=user)
    # business.product
    body = ""
    subject = ""
    emails = []
    pForm = DiscountProductForm()
    if request.method=='POST':
        pForm = DiscountProductForm(request.POST, request.FILES)
        if pForm.is_valid():
            discount=pForm.save(commit=False)
            discount.business=business
            discount.save()
            # email()
            return render(request, "business_home/NiceAdmin/product_discount.html", {'pForm':pForm})
            # return redirect(add_product)

    return render(request, "business_home/NiceAdmin/product_discount.html", {'pForm':pForm})

@csrf_exempt
def service_discount(request):
    user = request.user
    business = Business.objects.get(user=user)
    # business.product
    body = ""
    subject = ""
    emails = []

    sForm = DiscountServiceForm()
    if request.method=='POST':
        sForm = DiscountServiceForm(request.POST, request.FILES)
        if sForm.is_valid():
            discount=sForm.save(commit=False)
            discount.business=business
            discount.save()
            # email()
            return render(request, "business_home/NiceAdmin/service_discount.html", {'sForm':sForm})
            # return redirect(add_product)

    return render(request, "business_home/NiceAdmin/service_discount.html", {'sForm':sForm})

def reports(request):
    user = request.user
    business = Business.objects.get(user=user)
    products = business.products.all()
    sales = Sales.objects.all()    
    services = Service.objects.all()
    delivery = Delivery.objects.all()
    mydict = {
        'user':user,
         'products':products,
          'business':business,
          'sales':sales,
          'services':services,
          'delivery':delivery
        }
    return render(request, "business_home/NiceAdmin/tables-general.html", mydict)

def generate_report(request):
    user = request.user
    return render(request, "business_home/NiceAdmin/tables-data.html", {'user':user})


@csrf_exempt
def bulk_emails(request):
    user = request.user

    # body = "Delivery of the following products to  "
    subject = "Product delivery"
    emails = ["michaelkiprono98@gmail.com"]

    if (request.POST):
        data = request.POST.dict()
        subject = data.get("subject")
        body = data.get("text")
        image = request.FILES.get("image")
        print(image.name,"mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm")

        path = default_storage.save('tmp/'+image.name, ContentFile(image.read()))
        tmp_file = os.path.join(settings.MEDIA_ROOT, path)        
        # email(subject=subject, body=body, emails=emails)
        subject, from_email, to = 'hello', 'mkiprono94@gmail.com', 'michaelkiprono98@gmail.com'
        text_content = 'This is an important message.'
        html_content = '<p>This is an <strong>important</strong> message.</p> <img src="{{ tmp_file }}" />'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        
        msg.attach_file(tmp_file)
        msg.attach_alternative(html_content,  "text/html")
        msg.send()


    return render(request, "business_home/NiceAdmin/bulk_emails.html", {'user':user})

def posters(request):
    user = request.user
    return render(request, "business_home/NiceAdmin/posters.html", {'user':user})

def profile(request):
    user = request.user
    business = Business.objects.get(user=user)
    dealings = Dealings.objects.get(business=business)
    location = BusinessLocation.objects.all() # solve this error
    # loc = location.business_set.all()
    # business.location_set.all()
    print(location, ".............................................")
    userForm=UserForm(instance=user)
    businessForm=BusinessForm(instance=business)
    form = ChangePasswordForm()
    if request.method=='post':
        return redirect(change_password, id)

    mydict = {
        'user':user,
        'form':form,
        'business':business,
        'dealings':dealings,
        'userForm':userForm,
        'businessForm':businessForm
        # 'location':location
        }
    return render(request, "business_home/NiceAdmin/users-profile.html", mydict)

def customer_home(request):
    user = request.user
    # user = User.objects.get(id=id)
    customer = Customer.objects.get(user=user)
    products = Product.objects.all()
    services =  Service.objects.all()
    # location = CustomerLocation.objects.get(customer=customer)
    mydict = {
        'user':user,
        'customer':customer, 
        'products':products,
        'services':services
        # 'location':location
        }
   
    return render(request, "customer_home/eshopper-1.0.0/index.html", mydict)

def products(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    products = Product.objects.all()
    return render(request, "customer_home/eshopper-1.0.0/shop.html", {'products':products})

@csrf_exempt
def product_detail(request,pk):
    user = request.user
    product = Product.objects.get(pk=pk)
    return render(request, "customer_home/eshopper-1.0.0/detail.html", {'product':product})

def services(request):
    user = request.user
    customer = Customer.objects.get(user=user)
    services = Service.objects.all()
    return render(request, "customer_home/eshopper-1.0.0/services.html", {'services':services})

def service_detail(request, pk):
    user = request.user
    # business = user.business_set.all()
    # business = Business.objects.get(user=user)
    service = Service.objects.get(pk=pk)
    services = Service.objects.all()
    queue = ScheduleService.objects.filter(service=service)
   
    return render(request, "customer_home/eshopper-1.0.0/service_detail.html", {'service':service, 'services':services, 'queue':queue})
import datetime

@csrf_exempt
def service_enquire(request, pk):
    service = Service.objects.get(pk=pk)
    if (request.POST):
        data = request.POST.dict()
        enquiry = data.get("enquiry")
        enquiry = Response.objects.create(customer=request.user.customer, service=service, response=enquiry, time=datetime.datetime.now())
        # enquiry = Enquire.objects.create(business=service.business,enquiry=enquiry, time=datetime.datetime.now())
    return redirect(service_detail, service.pk)

@csrf_exempt
def enquiry_response(request, pk):
    e = Response.objects.get(pk=pk)
    # service = Service.objects.get(pk=s_pk)
    # customer = Customer.objects.get(pk=c_pk)
    if (request.POST):
        data = request.POST.dict()
        enquiry = data.get("response")
        response = Response.objects.create(customer=e.customer, service=e.service, response=enquiry, time=datetime.datetime.now())
        redirect(business_home)
        # enquiry = EnquiryResponse.objects.create(customer=user.customer,enquiry=enquiry, time=datetime.datetime.now())
    return redirect(business_home)
def invoices(request):
    sales = Sales.objects.all()
    return render(request, "customer_home/eshopper-1.0.0/checkout.html", {'sales':sales})

def checkout(request, pk):
    product = Product.objects.get(pk=pk)
    total=1

    account_reference = 'ABC001'
    callback_url = stk_push_callback_url
    transaction_desc = 'STK Push Description'    

    body = "Delivery of the following products to  "
    subject = "Product delivery"
    emails = ["michaelkiprono98@gmail.com"]

    if (request.POST):
        data = request.POST.dict()
        phone_number = data.get("phone_number")
        quantity =  data.get("quantity")
        delivery_man = data.get("delivery_man")
        total = int(quantity)*int(product.charges)

        if (int(product.quantity)>int(quantity)) or (int(product.quantity==quantity)):
            r = cl.stk_push(phone_number, total, account_reference, transaction_desc, callback_url)
            email(subject=subject, body=body, emails=emails)
            product.quantity = int(product.quantity)-int(quantity)
            product.save()
            return redirect(invoices)
            # return JsonResponse(r.response_description, safe=False)
    return render(request, "customer_home/eshopper-1.0.0/detail.html", {'product':product})

def schedule_service(request, pk):
    user = request.user
    service = Service.objects.get(pk=pk)
    schedule = ScheduleService.objects.create(service=service, time=datetime.datetime.now())
    return redirect(service_detail, service.pk)

def customer_profile(request):
    return render(request, "customer_home/eshopper-1.0.0/profile.html", {})

from xhtml2pdf import pisa
import io
from django.template.loader import get_template

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return pdf



def download_invoice(request):
    user = request.user
    sales = Sales.objects.get(id=1)
    # product = Product.objects.get()
    
    pdf = render_to_pdf("customer_home/eshopper-1.0.0/downlod_invoice.html", {'sales':sales, 'user':user})
    # print("mmmmmmmmmmmmmmmmmmmmmmmmmmm",type(pdf))
    return render_to_pdf("customer_home/eshopper-1.0.0/downlod_invoice.html", {'sales':sales, 'user':user})
