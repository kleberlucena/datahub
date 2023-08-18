from django import forms
from apps.rpa_manager.models import TesteUsuario

class TesteUsuarioForm(forms.ModelForm):
    class Meta:
        model = TesteUsuario
        fields = ['usuario', 'sub_usuario']
