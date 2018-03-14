
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms

class AnswerForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea)

    def clean_answer(self):
        data = self.cleaned_data['answer']
        #answer validation
        return data

