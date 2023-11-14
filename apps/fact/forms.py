from django import forms
from .models import FactType, Fact, FactImage, FactAddresses, FactVictims, FactSuspects, FactWitnesses

class FactTypeForm(forms.ModelForm):
    class Meta:
        model = FactType
        fields = '__all__'

class FactForm(forms.ModelForm):
    class Meta:
        model = Fact
        fields = '__all__'

class FactImageForm(forms.ModelForm):
    class Meta:
        model = FactImage
        fields = '__all__'
