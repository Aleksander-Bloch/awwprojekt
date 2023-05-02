from django import forms
from .models import Directory


class DirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        exclude = ['parent']

    parent = forms.IntegerField(widget=forms.HiddenInput())
