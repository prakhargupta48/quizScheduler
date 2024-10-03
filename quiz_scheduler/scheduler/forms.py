from django import forms
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['class_timetable', 'faculty_file']
