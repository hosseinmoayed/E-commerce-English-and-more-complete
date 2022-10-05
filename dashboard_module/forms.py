
from django import forms
from django.contrib.auth.models import User
from django.core import validators

from dashboard_module.models import UserInfo, Cart


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['firstname','lastname','address' , 'zip','Country' , 'State']
        widgets = {
            'address': forms.TextInput(attrs={
                'placeholder': "address",
                'class' : 'form-control',
                'id':'address'
            }),
            'zip': forms.TextInput(attrs={
                'placeholder': "zip",
                'class': 'form-control',
                'id':'zip'
            }),
            'firstname': forms.TextInput(attrs={
                'placeholder': "First name",
                'class': 'form-control',
                'id':'firstname'
            }),
            'lastname': forms.TextInput(attrs={
                'placeholder': "Last name",
                'class': 'form-control',
                'id':'lastname'
            }),
            'Country': forms.TextInput(attrs={
                'placeholder': "country",
                'class': 'form-control',
                'id': 'country'
            }),
            'State': forms.TextInput(attrs={
                'placeholder': "state",
                'class': 'form-control',
                'id': 'state'
            }),
        }


class Checkoutins(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username']
        widgets = {
            'email': forms.TextInput(attrs={
                'placeholder': "email",
                'class': 'form-control disabled',
                'id': 'email'
            }),
            'username': forms.TextInput(attrs={
                'placeholder': "username",
                'class': 'form-control disabled',
                'id': 'username'
            }),
        }


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['firstname','lastname','address' , 'zip','Country' , 'State']
        widgets = {
            'address': forms.TextInput(attrs={
                'placeholder': "address",
                'class': 'form-control',
                'id': 'address'
            }),
            'zip': forms.TextInput(attrs={
                'placeholder': "zip",
                'class': 'form-control',
                'id': 'zip'
            }),
            'firstname': forms.TextInput(attrs={
                'placeholder': "First name",
                'class': 'form-control',
                'id': 'firstname'
            }),
            'lastname': forms.TextInput(attrs={
                'placeholder': "Last name",
                'class': 'form-control',
                'id': 'lastname'
            }),
            'Country': forms.TextInput(attrs={
                'placeholder': "country",
                'class': 'form-control',
                'id': 'country'
            }),
            'State': forms.TextInput(attrs={
                'placeholder': "state",
                'class': 'form-control',
                'id': 'state'
            }),
        }
        error_messages = {
            'firstname':{
                'required': 'Please complete the field'
            },
            'lastname':{
                'required': 'Please complete the field'
            },
            'address':{
                'required': 'Please complete the field'
            },
            'zip':{
                'required': 'Please complete the field'
            },
            'Country':{
                'required': 'Please complete the field'
            },
            'State':{
                'required': 'Please complete the field'
            }
        }

    def __init__(self,*args , **kwargs):
        super(CheckoutForm, self).__init__(*args , **kwargs)
        self.fields["firstname"].required = True
        self.fields["lastname"].required = True
        self.fields["address"].required = True
        self.fields["zip"].required = True
        self.fields["Country"].required = True
        self.fields["State"].required = True



class ImageForm (forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['avatar']

        widgets = {
            'avatar':forms.FileInput(attrs={
                'class':'inpt-img-asli hidden',
                'style':'position: relative;bottom: 25px;'
            })
        }
