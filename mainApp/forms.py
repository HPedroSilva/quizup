from django import forms


class ImportQuestionsForm(forms.Form):
    file = forms.FileField()
