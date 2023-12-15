from django.forms import ModelForm
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']

        widgets = {     
            'username' : forms.TextInput(),
            'email' : forms.EmailInput(),
            'first_name' : forms.TextInput(),
            'last_name' : forms.TextInput(),
            'password1' : forms.PasswordInput(),
            'password2' : forms.PasswordInput(),
        }

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name','tableNumber','venue']
        

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title','desc','platform']
        

class JudgementForm(ModelForm):
    class Meta:
        model = Judgement
        exclude = ['mentor','round','timeCreated']
        

class MentorForm(ModelForm):
    class Meta:
        model = Mentor
        exclude = ['user']