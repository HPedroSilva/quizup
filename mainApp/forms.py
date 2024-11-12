from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ImportQuestionsForm(forms.Form):
    file = forms.FileField()


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')
