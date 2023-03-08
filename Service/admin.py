from ast import Sub
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User



class AccessTokenAdmin(admin.ModelAdmin):
    customers = AccessToken.objects.all().count()
    list_display=['token','created_at']

admin.site.register(AccessToken,AccessTokenAdmin)

class CustomerAdmin(admin.ModelAdmin):
    customers = Customer.objects.all().count()
    list_display=['user','phone_number']
    
admin.site.register(Customer,CustomerAdmin)

class ServiceAdmin(admin.ModelAdmin):
    customers = Service.objects.all().count()
    list_display=['business','name','images','charges','description','video']
    
admin.site.register(Service,ServiceAdmin)

class BusinessAdmin(admin.ModelAdmin):
    customers = Business.objects.all().count()
    list_display=['user','brand_name','photo','liscences', 'logo']
    
admin.site.register(Business,BusinessAdmin)

class EventAdmin(admin.ModelAdmin):
    events = Event.objects.all().count()
    list_display = ['title','host', 'organizers','category','start_time','end_time','neccesary_info','description']

admin.site.register(Event,EventAdmin)

class PatronageAdmin(admin.ModelAdmin):
    subscriptions = Patronage.objects.all().count()
    list_display = ['customer','business','state']

admin.site.register(Patronage,PatronageAdmin)

class NewsAdmin(admin.ModelAdmin):
    information = News.objects.all().count()
    list_display = ['title','category','outlet','message']

class NewsLikeAdmin(admin.ModelAdmin):
    information = NewsLike.objects.all().count()
    list_display = ['news','reads','likes']

admin.site.register(NewsLike,NewsLikeAdmin)

class FeedbackAdmin(admin.ModelAdmin):
    feeds = Feedback.objects.all().count()
    list_display = ['bussiness','feed']

admin.site.register(Feedback,FeedbackAdmin)

class RateServiceAdmin(admin.ModelAdmin):
    ratings = RateService.objects.all().count()
    list_display = ['service','rate','comment']

admin.site.register(RateService,RateServiceAdmin)

class RateBusinessAdmin(admin.ModelAdmin):
    ratings = RateBusiness.objects.all().count()
    list_display = ['business','rate','comment']

admin.site.register(RateBusiness,RateBusinessAdmin)


class ReferServiceAdmin(admin.ModelAdmin):
    ratings = ReferService.objects.all().count()
    list_display = ['referee','refered','service','message']

admin.site.register(ReferService,ReferServiceAdmin)

class TestimonyAdmin(admin.ModelAdmin):
    ratings = Testimony.objects.all().count()
    list_display = ['customer','business','testimony']

admin.site.register(Testimony,TestimonyAdmin)

class DealingsAdmin(admin.ModelAdmin):
    ratings = Dealings.objects.all().count()
    list_display = ['business','dealing_list','dealings']

admin.site.register(Dealings,DealingsAdmin)

class ProductAdmin(admin.ModelAdmin):
    ratings = Product.objects.all().count()
    list_display = ['business','name','charges', 'quantity', 'images', 'video', 'description']

admin.site.register(Product,ProductAdmin)

class SalesAdmin(admin.ModelAdmin):
    sales = Sales.objects.all().count()
    list_display = ['product','quantity','total_price', 'time', 'status']

admin.site.register(Sales,SalesAdmin)

class DeliveryAdmin(admin.ModelAdmin):
    delivery = Delivery.objects.all().count()
    list_display = ['business','customer','price', 'd_man']

admin.site.register(Delivery,DeliveryAdmin)

class ScheduleServiceAdmin(admin.ModelAdmin):
    schedules = ScheduleService.objects.all().count()
    list_display = ['service','time']

admin.site.register(ScheduleService,ScheduleServiceAdmin)

class EnquireAdmin(admin.ModelAdmin):
    enquiries = Enquire.objects.all().count()
    list_display = ['business','enquiry']

admin.site.register(Enquire,EnquireAdmin)

class DiscountProductAdmin(admin.ModelAdmin):
    discounts = DiscountProduct.objects.all().count()
    list_display = ['product','discount', 'quantity', 'duration']

admin.site.register(DiscountProduct,DiscountProductAdmin)

class DiscountServiceAdmin(admin.ModelAdmin):
    discounts = DiscountService.objects.all().count()
    list_display = ['service','discount', 'duration']

admin.site.register(DiscountService,DiscountServiceAdmin)

class BusinessLocationAdmin(admin.ModelAdmin):
    location = BusinessLocation.objects.all().count()
    list_display = ['business','county', 'sub_county','local_town','google_map']

admin.site.register(BusinessLocation,BusinessLocationAdmin)

class CustomerLocationAdmin(admin.ModelAdmin):
    location = CustomerLocation.objects.all().count()
    list_display = ['customer','county', 'sub_county','local_town','google_map']

admin.site.register(CustomerLocation,CustomerLocationAdmin)

class ResponseAdmin(admin.ModelAdmin):
    location = Response.objects.all().count()
    list_display = ['customer','service', 'response','time']

admin.site.register(Response,ResponseAdmin)