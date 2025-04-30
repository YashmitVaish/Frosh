from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Team,Question
from django.db import transaction
from django.core.exceptions import ValidationError

class Registerteam(UserCreationForm):
    name = forms.CharField(max_length=100)
    members = forms.CharField(widget=forms.Textarea(attrs={'rows':3}))

    class Meta:
        model = User
        fields = ["username", "members","password1", "password2","name"]
        help_texts = {
            'members' : 'enter name seperated by commas'
        }

    def clean_name(self):
        name = self.cleaned_data['name']
        if Team.objects.filter(name=name).exists():
            raise ValidationError("This team name is already taken. Please choose another.")
        return name
    
    @transaction.atomic
    def save_data(self, commit = True):
        user  = super().save(commit=True)
        Team.objects.create(
            user = user,
            name=self.cleaned_data['name'],
            members=self.cleaned_data['members']
        )
        return user

class Answer(forms.Form):
    answer = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Enter your answer'}))

class addques(forms.Form):
    question_number = forms.IntegerField(min_value=1)
    points = forms.IntegerField(min_value=1)
    question_text = forms.CharField(widget=forms.Textarea)
    answer = forms.CharField(widget=forms.Textarea)

    def clean_question_number(self):
        question_number = self.cleaned_data['question_number']
        if Question.objects.filter(question_number=question_number).exists():
            raise forms.ValidationError("A question with this number already exists.")
        return question_number

    