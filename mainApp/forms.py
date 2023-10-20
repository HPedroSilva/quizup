from django import forms
from django.db.models.base import Model
from mainApp.models import Match, Category
from django.contrib.auth.models import User

class ImportQuestionsForm(forms.Form):
    file = forms.FileField()

class CustomMMCFUser(forms.ModelMultipleChoiceField):
    def label_from_instance(self, user):
        name = user.first_name if user.first_name else user
        return f"{name}"
class CreateMatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ["categories", "level", "users"]

    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple, label="Categorias")
    users = CustomMMCFUser(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple, label="Jogadores")