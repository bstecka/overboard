from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question, Tag
import re


class AnswerForm(forms.Form):
    answer = forms.CharField(label='answer')


class VoteForm(forms.Form):
    user = forms.CharField(label='user', max_length=100)
    vote = forms.IntegerField(label='vote')
    target = forms.IntegerField(label='target')


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class NewQuestionForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    tags = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), help_text='Tag should be one string of characters started with # sign. Separate tags with whitespace.')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.pub_date = kwargs.pop('pub_date', None)
        super(NewQuestionForm, self).__init__(*args, **kwargs)

    def save(self):
        question = Question.objects.create(asked_by=self.user,
                                           title=self.data['title'],
                                           content=self.data['content'],
                                           pub_date=self.pub_date)
        question.save()

        regex = re.compile('^#*')
        tagsList = [tag for tag in self.data['tags'].split() if regex.match(tag)]
        tagsNames = [re.sub('#', '', tag) for tag in tagsList]

        for tagName in tagsNames:
            if Tag.objects.filter(tag_name=tagName).exists():
                Tag.objects.get(tag_name=tagName).questions.add(question)
            else:
                tag = Tag.objects.create(tag_name=tagName)
                tag.questions.add(question)
                tag.save()

        return


