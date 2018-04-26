from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question, Tag
import re
import datetime


class AnswerForm(forms.Form):
    answer = forms.CharField(label='answer')


class RegistrationForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, help_text='Required.',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=30, required=True, help_text='Required.', label="Password",
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=30, required=True, help_text='Required. Must be the same as .',
                                label="Confirm password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
