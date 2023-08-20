from django import forms
from django.core.exceptions import ValidationError
from apps.rpa_manager.models import Missao, Aeronave
from apps.rpa_manager.utils.add_class_and_form_control import add_class_and_form_control
from apps.rpa_manager.utils.addPlaceholderToField import addPlaceholder


class MissaoFormulario(forms.ModelForm):
    
    class Meta:
        model = Missao
        fields = ['titulo', 
                  'piloto_observador', 
                  'quem_solicitou', 
                  'quem_autorizou', 
                  'local', 
                  'latitude', 
                  'longitude', 
                  'aeronave', 
                  'usuario'
                  ]
        
        widgets = {
                   'usuario': forms.HiddenInput(),
                   'titulo': forms.TextInput(attrs={'class': 'form-control'}),
                   'concluida': forms.HiddenInput(),
                   }

    def clean_aeronave(self):
        aeronave = self.cleaned_data['aeronave']
        if aeronave.em_uso:
            raise forms.ValidationError('A aeronave está em uso e não pode ser selecionada.')
        return aeronave
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        addPlaceholder(self, 'titulo', 'Informe um título para operação')
        addPlaceholder(self, 'quem_autorizou', 'Informe quem autorizou a operação')
        addPlaceholder(self, 'quem_solicitou', 'Informe um título para operação')
        
        self.fields['aeronave'].widget.attrs.update({
            'class': 'aeronave_escolha'
        })
        self.fields['latitude'].widget.attrs.update({
            'required': True
        })
        self.fields['longitude'].widget.attrs.update({
            'required': True
        })

        self.fields['aeronave'].queryset = Aeronave.objects.filter(em_uso=False)
        
        campos = ['titulo', 
                  'piloto_observador', 
                  'quem_solicitou',
                  'quem_autorizou', 
                  'local', 
                  'latitude',
                  'longitude',
                  'aeronave', 
                  'usuario']
        
        for campo in campos:
            add_class_and_form_control(self, campo, campo, 'form-control')
            
    def clean(self):
        cleaned_data = super().clean()
        piloto_remoto = cleaned_data.get('usuario')
        piloto_observador = cleaned_data.get('piloto_observador')
        latitude = cleaned_data.get('latitude')
        longitude = cleaned_data.get('longitude')
        
        if piloto_remoto == piloto_observador:
            self.add_error('usuario', "O piloto remoto não pode ser o mesmo que o piloto observador.")
            self.add_error('piloto_observador', "O piloto observador não pode ser o mesmo que o piloto remoto.")
        if latitude == 0.0:
            self.add_error('latitude', "Latitude ou Longitude inválidos (marque um ponto no mapa)")
        if longitude == 0.0:
            self.add_error('longitude', "Latitude ou Longitude inválidos (marque um ponto no mapa)")
        
        return cleaned_data