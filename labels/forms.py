from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Label

class LabelForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), max_length=50)

    class Meta:
        model = Label
        fields = ['name']
