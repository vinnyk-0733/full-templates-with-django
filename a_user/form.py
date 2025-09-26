from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import *

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']
        widget = {
            'image':forms.FileInput(),
            'displayname':forms.TextInput(attrs={'placeholders':'Add display name'}),
            'info':forms.Textarea(attrs={'rows':3,'placeholder':'Add Information'})
        }

class EmailForm(ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email'] 