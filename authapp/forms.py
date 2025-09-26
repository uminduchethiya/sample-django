from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import User


# Register form

class RegisterForm(UserCreationForm):
    first_name =forms.CharField(max_length=30)
    last_name= forms.CharField(max_length=30)
    email=forms.EmailField()
    phone_number=forms.CharField(max_length=20,required=False)
    
    class Meta:
        model=User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'password1', 'password2']

#Login Form
class LoginForm(AuthenticationForm):
    username=forms.CharField(max_length=50)
    password=forms.CharField(widget=forms.PasswordInput)