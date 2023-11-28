# forms.py
from django import forms

class StudentUploadForm(forms.Form):
    file = forms.FileField()

