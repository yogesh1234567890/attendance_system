from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Layout, Row,Column
from django.forms import ModelForm
from .models import *

class classForm(ModelForm):
    class Meta:
        model=Classes
        fields='__all__'

class SubjectForm(ModelForm):
    class Meta:
        model=Subject
        fields='__all__'