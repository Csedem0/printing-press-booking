# booking/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import PrintingPress
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'description']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class PrintingPressOwnerForm(forms.ModelForm):
    class Meta:
        model = PrintingPress
        fields = ['name', 'location', 'contact_info']
