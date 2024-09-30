from django import forms


class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, label='Username')
    email = forms.EmailField()
    password = forms.CharField(max_length=50, label='Password', widget=forms.PasswordInput)