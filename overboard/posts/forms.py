from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Question, Tag
import re
import datetime


class AnswerForm(forms.Form):
    answer = forms.CharField(label='answer')


class VoteForm(forms.Form):
    vote = forms.IntegerField(label='vote')
    target = forms.IntegerField(label='target')


class AnswerVoteForm(forms.Form):
    vote = forms.IntegerField(label='vote')
    target = forms.IntegerField(label='target')
    answer = forms.CharField(label='answer', max_length=100)


# class RegistrationForm(UserCreationForm):
#     username = forms.CharField(max_length=30, required=True, help_text='Required.',
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
#     first_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
#                                  widget=forms.TextInput(attrs={'class': 'form-control'}))
#     last_name = forms.CharField(max_length=30, required=False, help_text='Optional.',
#                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',
#                              widget=forms.TextInput(attrs={'class': 'form-control'}))
#     password1 = forms.CharField(max_length=30, required=True, help_text='Required.', label="Password",
#                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(max_length=30, required=True, help_text='Required. Must be the same as .',
#                                 label="Confirm password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class NewQuestionForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    tags = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2}), required=False,
                           help_text='Tag should be one string of characters started with # sign. Separate tags with whitespace.')

    def save(self):
        question = Question.objects.create(asked_by=User.objects.get(pk=self.data['user_id']),
                                           title=self.data['title'],
                                           content=self.data['content'],
                                           pub_date=datetime.datetime.now())
        question.save()

        regex = re.compile(r'^#*')
        tags_list = [tag for tag in self.data['tags'].split() if regex.match(tag)]
        tags_names = [re.sub('#', '', tag) for tag in tags_list]

        for tag_name in tags_names:
            if Tag.objects.filter(tag_name=tag_name).exists():
                Tag.objects.get(tag_name=tag_name).questions.add(question)
            else:
                tag = Tag.objects.create(tag_name=tag_name)
                tag.questions.add(question)
                tag.save()

        return


