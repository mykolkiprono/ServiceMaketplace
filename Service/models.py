from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator

class AccessToken(models.Model):
	token = models.CharField(max_length=30)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		get_latest_by = 'created_at'

	def __str__(self):
		return self.token

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    phone_number = models.CharField(max_length=10)
    profile_pic = models.ImageField(upload_to="photos/profiles",null=True,blank=True)

    def __str__(self):
      return self.user.username
    
class Business(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, related_name="businesses")    
    brand_name = models.CharField(max_length=20,default="none")
    logo = models.ImageField(upload_to="photos/logos",null=True,blank=True)    
    liscences = models.ImageField(upload_to="photos/liscences",null=True,blank=True)
    phone_number = models.CharField(max_length=10)
    photo = models.ImageField(upload_to="photos/Businesses",null=True,blank=True)

    def __str__(self):
       return self.user.username 

class CustomerLocation(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name="locations")
    google_map = models.URLField(null=True,blank=True) #change
    county = models.CharField(max_length=15)
    sub_county = models.CharField(max_length=15,null=True)
    local_town = models.CharField(max_length=15,null=True)

class BusinessLocation(models.Model):
    business = models.ForeignKey('Business', on_delete=models.CASCADE, related_name="locations")
    county = models.CharField(max_length=15,default="meru")
    sub_county = models.CharField(max_length=15,default="nchiru")
    local_town = models.CharField(max_length=15,default="nchiru")
    google_map = models.URLField(blank=True, null=True)

    def __str__(self):
       return self.business 


class Service(models.Model):
    business = models.ForeignKey("Business",on_delete=models.CASCADE, null=True, related_name="services")
    name = models.CharField(max_length=200)
    charges = models.DecimalField(max_digits=6, decimal_places=2)
    images = models.FileField(upload_to="photo/Service", blank=True, null=True)
    video = models.FileField(upload_to="videos", blank=True, null=True)
    description = models.TextField(max_length=200)
    def __str__(self):
      return self.name

class Product(models.Model):
    business = models.ForeignKey("Business",on_delete=models.CASCADE, null=True, related_name="products")
    name = models.CharField(max_length=200)
    charges = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    images = models.FileField(upload_to="photo/Service", blank=True, null=True)
    video = models.FileField(upload_to="videos", blank=True, null=True)
    description = models.TextField(max_length=200)
    def __str__(self):
      return self.name

class Sales(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name="sales")
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, null=True,blank=True)
    quantity = models.IntegerField()
    total_price = models.CharField(max_length=15)
    time = models.DateTimeField()
    choices = (
        ("pending", "pending"),
        ("checked out", "checked out")
    )
    status = models.CharField(default=None, choices=choices, max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.product.name)

class ScheduleService(models.Model):
    customer = models.ForeignKey("Customer", on_delete=models.CASCADE, null=True,blank=True)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    time = models.DateTimeField()

class Delivery(models.Model):
    business = models.ForeignKey('Business', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    sale = models.ForeignKey('Sales', on_delete=models.CASCADE)
    price = models.IntegerField()
    d_man = models.ForeignKey(User, on_delete=models.CASCADE)


class Dealings(models.Model):
    business = models.ForeignKey('Business', on_delete=models.CASCADE)
    dealing_list = models.CharField(max_length=50,default="selling") # products or services or both
    dealings = models.TextField(max_length=1000) # descibe what you do

class Event(models.Model):
    choices = ((1,"political"), (2, "entertainment"), (3, "promotion"))
    title = models.CharField(max_length=15)
    host = models.ForeignKey("Business",on_delete=models.CASCADE)
    neccesary_info = models.TextField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()    
    category = models.TextField(choices=choices, max_length=100)
    description = models.TextField(max_length=200)    
    organizers = models.CharField(max_length=50)
    hosts = models.CharField(max_length=50)

    def __str__(self):
      return self.title

class EventLocation(models.Model):
    event=models.OneToOneField('event', on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    google_map= models.URLField(blank=True, null=True)

class DiscountService(models.Model):
    service = models.ForeignKey("Service",on_delete=models.CASCADE, blank=True, null=True)
    discount = models.IntegerField()
    duration = models.IntegerField()

class DiscountProduct(models.Model):
    product = models.ForeignKey("Product",on_delete=models.CASCADE, related_name="pdiscounts")
    discount = models.IntegerField()
    quantity = models.IntegerField()
    duration = models.IntegerField()

class StateService(models.Model):
    service = models.ForeignKey("Service",on_delete=models.CASCADE)
    available = models.BooleanField()
    description = models.TextField(max_length=50, null=True,blank=True)

class Patronage(models.Model):
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)
    business = models.ForeignKey("Business",on_delete=models.CASCADE)
    state = models.BooleanField()

    def __str__(self):
       return str(self.state)

class News(models.Model): 
    outlet = models.ForeignKey("Business",on_delete=models.CASCADE)
    title = models.TextField(max_length=200)
    message = models.TextField(max_length=500)
    category = models.TextField(max_length=200)
    date = models.DateField() # change 

    def __str__(self):
       return self.title

class NewsLike(models.Model):
    news = models.ForeignKey("News",on_delete=models.CASCADE)
    reads = models.PositiveIntegerField()
    likes = models.PositiveIntegerField()
    comment = models.TextField(null=True, blank=True)

import datetime

class Enquire(models.Model):
    business = models.ForeignKey('Business', on_delete=models.CASCADE, related_name="enquiries")
    enquiry = models.CharField(max_length=200)
    time = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    # @property
    # def is_past(self, u):
    #     if (self.time>u.last_login):
    #         return True
    #     else:
    #         return False

# class Enquiry(models.Model):
#     # business = models.ForeignKey('Business', on_delete=models.CASCADE, related_name="enquiries")
#     service = models.ForeignKey("Service", on_delete=models.CASCADE)
#     customer = models.ForeignKey("Service",on_delete=models.CASCADE)
#     enquiry = models.CharField(max_length=200)
#     time = models.DateTimeField(null=True, blank=True, auto_now_add=True)

#     # @property
#     # def is_past(self, u):
#     #     if (self.time>u.last_login):
#     #         return True
#     #     else:
#     #         return False

class Response(models.Model):
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)
    service = models.ForeignKey("Service", on_delete=models.CASCADE)
    # bussiness = models.ForeignKey("Service",on_delete=models.CASCADE)
    response = models.TextField(max_length=200)
    time = models.DateTimeField()
    is_customer = models.BooleanField(default=False)

    def __str__(self):
       return self.response

class Feedback(models.Model):
    # customer = models.ForeignKey("Customer",on_delete=models.CASCADE)
    bussiness = models.ForeignKey("Service",on_delete=models.CASCADE)
    feed = models.TextField(max_length=200)
    # time = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
       return self.feed
    
# class EnquiryResponse(models.Model):
#     customer = models.ForeignKey("Customer",on_delete=models.CASCADE)
#     # service = models.ForeignKey("Service",default=None, on_delete=models.CASCADE)
#     # bussiness = models.ForeignKey("Service",on_delete=models.CASCADE)
#     response = models.TextField(max_length=200)
#     time = models.DateTimeField()

#     def __str__(self):
#        return self.response

class RateService(models.Model):
    service = models.ForeignKey("Service",on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    comment = models.TextField(max_length=200)

    def __str__(self):
       return self.comment

class RateProduct(models.Model):
    product = models.ForeignKey("Product",on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    comment = models.TextField(max_length=200)

    def __str__(self):
       return self.comment


class RateBusiness(models.Model):
    business = models.ForeignKey("Business",on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    comment = models.TextField(max_length=200)

    def __str__(self):
       return self.comment

class ReferService(models.Model):
    referee = models.CharField(max_length=30)
    refered = models.ForeignKey("Customer",on_delete=models.CASCADE)
    service = models.ForeignKey("Service",on_delete=models.CASCADE)
    message = models.TextField(max_length=50,default="none")


class Testimony(models.Model):
    customer = models.ForeignKey("Customer",on_delete=models.CASCADE)
    business = models.ForeignKey("Business",on_delete=models.CASCADE)
    testimony = models.TextField(max_length=200)

    class Meta:
        verbose_name="Testimony"

class Delivery_men(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, blank=True, null=True)
    business = models.ForeignKey('Business', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField()
