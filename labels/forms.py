# labels/forms.py
"""
Forms for the labels application.
"""
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Label


class LabelForm(forms.ModelForm):
    """
    Form for creating and updating task labels.
    """
    name = forms.CharField(label=_('Имя'), max_length=50)

    class Meta:
        model = Label
        fields = ['name']