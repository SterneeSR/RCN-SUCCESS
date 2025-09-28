# core/forms.py
from django import forms

class BulkUploadForm(forms.Form):
    file = forms.FileField(label='Select a CSV or Excel file')