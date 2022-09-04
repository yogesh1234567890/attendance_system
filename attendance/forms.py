from asyncore import read
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Row,Column
from django.forms import ModelForm
from django import forms
from .models import *

class classForm(ModelForm):
    class Meta:
        model=Classes
        fields='__all__'

class SubjectForm(ModelForm):
    class Meta:
        model=Subject
        fields='__all__'
        
class StudentForm(ModelForm):
    class Meta:
        model=Students
        fields='__all__'

class InlineclassForm(ModelForm):
    class Meta:
        model=Classes
        fields=['class_name']
        