from django import forms
from django.core.exceptions import ValidationError
from django.db import connection
import re


def get_city_choices():
    with connection.cursor() as cursor:
        cursor.execute("SELECT City_ID, City_Name FROM city")
        rows = cursor.fetchall()
    return [(row[0], row[1]) for row in rows]

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    phoneNumber = forms.CharField(max_length=11, min_length=11)
    city = forms.ChoiceField(choices=get_city_choices(), required=True)

    def clean_phoneNumber(self):
        phone_number = self.cleaned_data.get('phoneNumber')
        if not re.match(r'^0\d{10}$', phone_number):
            raise ValidationError('Phone number must be 11 digits long and start with a "0".')
        return phone_number
    
