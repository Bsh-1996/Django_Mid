from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from . models import Profile

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=50, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'your password...'}))
    password2 = forms.CharField(max_length=50, label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'your password...'}))


    # the methods below are for validdations for email, username, and check the password confirmation
    # the clean email is for when someone want to register avoid that person to register with same email... and exaclty for username. and clean method is for
    # confiramtion password to cheeck if password and password confirm are same.
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email = email).exists()
        if user:
            raise ValidationError('this email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username = username).exists()
        if user:
            raise ValidationError('this username already exists')
        return username
    
    def clean(self):
        cd = super().clean()
        p1 = cd.get("password1")
        p2 = cd.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError('passwords do not match')

    
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=50, label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'your password...'}))
    

class EditUserForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = ('age', 'bio')
    
    


