from .models import *
from django.contrib.auth.models import User
from django import forms
from . import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.validators import UnicodeUsernameValidator
# from django.utils.translation import ugettext_lazy as _   
from datetime import datetime
# from bootstrap_datepicker_plus.widgets import DateTimePickerInp

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer 
        fields= ['phone_number','profile_pic']


    def clean(self):
        super(CustomerForm, self).clean()

        phone_number = self.cleaned_data.get('phone_number')

        if len(str(phone_number))<10:
            self._errors['phone_number'] = self.error_class(['must be a minimum of 10 characters'])                      

        return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Invalid credentials")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class UserForm(forms.ModelForm):

    class Meta:
        model = User 
        fields = ['username','password','email']

    def clean(self):
        super(UserForm, self).clean()
        username = self.cleaned_data.get('username')
        if username.isnumeric():
            self._errors['username'] = self.error_class(['username cannot be numbers'])
        if len(username) < 5:
            self._errors['username'] = self.error_class(['username must be more than 5 characters'])

        return self.cleaned_data


class BusinessForm(forms.ModelForm):

    class Meta:
        model = Business 
        fields= ['brand_name','logo','liscences','phone_number','photo']
    def clean(self):
        super(BusinessForm, self).clean()

        phone_number = self.cleaned_data.get('phone_number')
        if len(str(phone_number))<10:
                self._errors['phone_number'] = self.error_class(['must be a minimum of 10 characters'])                      

        return self.cleaned_data

class DealingsForm(forms.ModelForm):
    class Meta:
        model=Dealings
        fields=['dealings','dealing_list']

class BusinessLocationForm(forms.ModelForm):
    
    class Meta:
        model = BusinessLocation
        fields = ['sub_county','county','local_town','google_map']

class CustomerLocationForm(forms.ModelForm):
    
    class Meta:
        model = CustomerLocation
        fields = ["county",'sub_county','local_town','google_map']


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = ["name",'charges','quantity','images', 'description', 'video']
from django.forms import ModelForm, ChoiceField
class ServiceForm(forms.ModelForm):    
    class Meta:
        model = Service
        fields = ["name",'charges','images', 'description', 'video']

class DiscountServiceForm(forms.ModelForm):
    
    class Meta:
        model = DiscountService
        fields = ['service',"discount",'duration']

class DiscountProductForm(forms.ModelForm):
    
    class Meta:
        model = DiscountProduct
        fields = ['product',"discount",'duration', 'quantity']
