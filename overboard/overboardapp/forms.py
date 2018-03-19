
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms

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
