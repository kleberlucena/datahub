from django import forms
from apps.rpa_manager.models import PontosDeInteresse

class PointsOfInterestForm(forms.ModelForm):
    class Meta:
        model = PontosDeInteresse
        fields = ['operacao', 'descricao', 'latitude', 'longitude']