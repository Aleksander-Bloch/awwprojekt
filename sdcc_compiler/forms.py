from django import forms
from django.forms import ClearableFileInput

from .models import Directory, File


class AddDirectoryForm(forms.ModelForm):
    class Meta:
        model = Directory
        exclude = ['parent', 'owner', 'is_accessible', 'creation_date', 'access_change', 'last_modification']

    parent = forms.IntegerField(widget=forms.HiddenInput(), required=False)


class AddFileForm(forms.ModelForm):
    class Meta:
        model = File
        exclude = ['directory', 'owner', 'is_accessible', 'creation_date', 'access_change', 'last_modification']

    directory = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    file = forms.FileField(widget=ClearableFileInput(attrs={'accept': '.c'}))
