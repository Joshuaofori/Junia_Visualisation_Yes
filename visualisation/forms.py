from django import forms

class UploadedFileForm(forms.Form):
    data_file = forms.FileField()