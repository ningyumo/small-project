from django import forms
from .models import File


class FileUploadForm(forms.Form):
    title = forms.CharField(
        max_length=50,
        label="文件名",
        widget=forms.TextInput(attrs={"class": "form-control"}))
    file = forms.FileField(
        widget=forms.FileInput(attrs={"class": "form-control"}))


class FileUploadModelForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'file']
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "file": forms.FileInput(attrs={"class": "form-control"})
        }