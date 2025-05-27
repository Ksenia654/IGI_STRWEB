from typing import Any
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from realtorBack.models import *
from django.utils import timezone
from realtorBack.db.category import *

STYLE_ATTRIBUTE = 'width: 200px; text-align: center; border: 2px solid black; border-radius: 10px; height: 40px;'

class DateInput(forms.DateInput):
    input_type='date'

class RegisterForm(UserCreationForm):
    username=forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'lf--input',
                'placeholder': 'Username',
                'style': STYLE_ATTRIBUTE
            }
        ),
        min_length=4,
        max_length=50,
        required=True
    )

    first_name=forms.CharField(
        label='First Name',
        widget=forms.TextInput(
            attrs={
                'class': 'lf--input',
                'placeholder': 'First Name',
                'style': STYLE_ATTRIBUTE
            }
        ),
        min_length=2,
        max_length=50,
        required=True
    ) 

    last_name=forms.CharField(
        label='Last Name',
        widget=forms.TextInput(
            attrs={
                'class': 'lf--input',
                'placeholder': 'Last Name',
                'style': STYLE_ATTRIBUTE
            }
        ),
        min_length=2,
        max_length=50,
        required=True
    ) 

    email=forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={
                'class': 'lf--input',
                'placeholder': 'Email',
                'style': STYLE_ATTRIBUTE
            }
        ),
        min_length=2,
        max_length=50,
        required=True
    ) 
    phone_number = forms.CharField(
        label='Phone number', 
        widget=forms.TextInput(
            attrs={
                'class': 'lf--input',
                'placeholder': 'Phone number',
                'style': STYLE_ATTRIBUTE
            }
        ),
        min_length=2, 
        max_length=100
    )
    birth_date = forms.DateField(
        label='Type your birth date', 
        widget=DateInput,
        required=True
    )
    photo = forms.ImageField(
        label='Image', 
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 
                  'first_name',
                  'last_name',
                  'email', 
                  'password1', 
                  'password2',
                  'birth_date',
                  'phone_number', 
                  'photo')
        
class LoginForm(forms.Form):
    username=forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'lf--input',
                'placeholder': 'Username',
                'style': STYLE_ATTRIBUTE
            }
        ),
        min_length=4,
        max_length=50,
        required=True
    )
    
    password=forms.CharField(
        label='Password',
        widget=forms.TextInput(
            attrs={
                'class': 'lf--input',
                'placeholder': 'Password',
                'type': 'password',
                'style': STYLE_ATTRIBUTE
            }
        ),
        min_length=4,
        max_length=50,
        required=True
    )

class ReviewForm(forms.Form):
    grade=forms.IntegerField(
        label='Grade',
        widget=forms.TextInput(
            attrs={
                'class': 'lf--input',
                'style': STYLE_ATTRIBUTE
            }
        ),
        min_value=0,
        max_value=10,
        required=True
    )
    comment=forms.CharField(
        label='Comment',
        widget=forms.TextInput(
            attrs={
                'class': 'lf--input',
                'placeholder': 'Type your comment here',
                'style': STYLE_ATTRIBUTE
            }
        ),
        max_length=500,
        required=True
    )

class EstateForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    description = forms.CharField(max_length=300)
    category = forms.ModelChoiceField(GetCategories())
    cost = forms.DecimalField(
        max_digits=6, 
        validators=[MinValueValidator(
            limit_value=0,
            message="Invalid cost."
        )]
    )
    area=forms.DecimalField(
        max_digits=6, 
        validators=[MinValueValidator(
            limit_value=0,
            message="Invalid area."
        )]
    )

    class Meta:
        model = Estate
        fields = ['name','description','category','cost','area']