from django import forms

class NewContact(forms.Form):
    email = forms.CharField(max_length=100, label='Email')
    first_name = forms.CharField(max_length=100, label='First Name')
    last_name = forms.CharField(max_length=100, label='Last Name')
    phone = forms.CharField(max_length=20, label='Phone') 
