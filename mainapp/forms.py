from django import forms
from models import Users,Type_of_Product
from django.contrib.auth.models import User
import re
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
         
class RegistrationForm(forms.Form):
 
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30,placeholder='Username')), label=_("Username"), error_messages={ 'invalid': _("This value must contain only letters, numbers and underscores.") })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30,placeholder='Email address')), label=_("Email address"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False,placeholder='Choose a password')),min_length=6, label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False,placeholder='Confirm password')), label=_("Password (again)"))
    manager = forms.BooleanField(widget=forms.CheckboxInput(attrs=dict(required=False)),required=False,label=_("Manager"))
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_("The username already exists. Please try another one."))
 
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields did not match."))
        return self.cleaned_data
        
class AddProductForm(forms.Form):
	choices=Type_of_Product.objects.all().values_list()
	numeric = RegexValidator(r'\d+', 'Only numeric characters are allowed.')
	name=forms.CharField(widget=forms.TextInput(attrs=dict(required=True,placeholder='Product Name')))
	price=forms.RegexField(regex=r'^\d+(.\d{1,2})?$', widget=forms.TextInput(attrs=dict(required=True,placeholder='Price')), error_messages = {'invalid': _("Not a valid web address1.")})
	category=forms.ChoiceField(choices=choices, widget=forms.Select(attrs=dict(required=True,placeholder='Type of Product')))
	quantity=forms.CharField(widget=forms.TextInput(attrs=dict(required=True,placeholder='Quantity')),validators=[numeric])
    