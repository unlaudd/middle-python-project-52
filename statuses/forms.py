from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Status

class StatusForm(forms.ModelForm):
    name = forms.CharField(label=_('Name'), max_length=100)

    class Meta:
        model = Status
        fields = ['name']
