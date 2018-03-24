from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean_answer(self):
        data = self.cleaned_data['answer']
        #answer validation
        return data


class VoteForm(forms.Form):
    user = forms.CharField(label='user', max_length=100)
    vote = forms.IntegerField(label='vote')
    question = forms.IntegerField(label='question')


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)