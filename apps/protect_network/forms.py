from django import forms
from . import models

from apps.portal import models as portal_models
from apps.georeference.models import SpotType as geo_spottype
from apps.georeference.models import Spot as geo_spot


class UpdateGeoSpotForm(forms.ModelForm):
    IS_HEADQUARTERS_CHOICES = [
        (True, 'Sim'),
        (False, 'Não'),
    ]
    name = forms.CharField(max_length=100, label='Ponto', required=True)
    details = forms.CharField(max_length=300, label='Informações adicionais', required=False)
    spot_type = forms.ModelChoiceField(queryset=geo_spottype.objects.all(), label='Tipo de Ponto', widget=forms.Select(attrs={'class': 'form-control'}), required=True)
    latitude = forms.FloatField(label="Latitude", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clique no mapa ou digite as coordenadas'}))
    longitude = forms.FloatField(label="Longitude", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clique no mapa ou digite as coordenadas'}))
    street = forms.CharField(label='Logradouro', max_length=255, required=False)
    number = forms.CharField(label='Número', max_length=9, required=False)
    complement = forms.CharField(label='Complemento', max_length=255, required=False)
    reference = forms.CharField(label='Pontos de Referência', max_length=255, required=False)
    neighborhood = forms.CharField(label='Bairro', max_length=155, required=False)
    city = forms.CharField(label='Cidade', max_length=155, required=False)
    state = forms.CharField(label='Estado', max_length=2, required=False)
    region = forms.CharField(label='Região', max_length=2, required=False)
    country = forms.CharField(label='País', max_length=155, required=False)
    zipcode = forms.CharField(label='CEP', required=False)
    is_headquarters = forms.ChoiceField(
        label='É Matriz?',
        choices=IS_HEADQUARTERS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )
    QPP = forms.ModelChoiceField(
        queryset=models.Qpp.objects.all(),
        label='QPP',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label='Selecione um QPP'
    )
    spot_network = forms.ModelChoiceField(
        queryset=models.Network.objects.all(),
        label='Rede',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label='Selecione uma rede'
    )
    cnpj = forms.CharField(label='CNPJ', max_length=20, required=False)
    parent_company = forms.CharField(label='CNPJ da matriz', max_length=20, required=False)

                         
    class Meta:
        model = models.ProtectNetworkSpot
        fields = ['tags', 'update_score', 'next_update', 'is_headquarters', 'cnpj', 'parent_company', 'spot_network', 'qpp']
        widgets = {
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'update_score': forms.NumberInput(attrs={'class': 'form-control'}),
            'next_update': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_headquarters': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_company': forms.TextInput(attrs={'class': 'form-control'}),
            'spot_network': forms.Select(attrs={'class': 'form-control'}),
            'qpp': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    

class GeoSpotForm(forms.ModelForm):
    IS_HEADQUARTERS_CHOICES = [
        (True, 'Sim'),
        (False, 'Não'),
    ]
    latitude = forms.FloatField(label="Latitude", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clique no mapa ou digite as coordenadas'}))
    longitude = forms.FloatField(label="Longitude", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clique no mapa ou digite as coordenadas'}))
    street = forms.CharField(label='Logradouro', max_length=255, required=False)
    number = forms.CharField(label='Número', max_length=9, required=False)
    complement = forms.CharField(label='Complemento', max_length=255, required=False)
    reference = forms.CharField(label='Pontos de Referência', max_length=255, required=False)
    neighborhood = forms.CharField(label='Bairro', max_length=155, required=False)
    city = forms.CharField(label='Cidade', max_length=155, required=False)
    state = forms.CharField(label='Estado', max_length=2, required=False)
    region = forms.CharField(label='Região', max_length=2, required=False)
    country = forms.CharField(label='País', max_length=155, required=False)
    zipcode = forms.CharField(label='CEP', required=False)
    is_headquarters = forms.ChoiceField(
        label='É Matriz?',
        choices=IS_HEADQUARTERS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )
    QPP = forms.ModelChoiceField(
        queryset=models.Qpp.objects.all(),
        label='QPP',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label='Selecione um QPP'
    )
    spot_network = forms.ModelChoiceField(
        queryset=models.Network.objects.all(),
        label='Rede',
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        empty_label='Selecione uma rede'
    )
    cnpj = forms.CharField(label='CNPJ', max_length=20, required=False)
    parent_company = forms.CharField(label='CNPJ da matriz', max_length=20, required=False)


    

    class Meta:
        model = geo_spot
        fields = ('name', 'details', 'spot_type', 'latitude', 'longitude','location')
        labels = {
            'name': 'Nome',
            'details': 'Informações adicionais',
            'spot_type': 'Tipo',

        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do ponto'}),
            'details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se houver, digite informações adicionais'}),
            'spot_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    

class SpotTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['spot_type_father'].queryset = geo_spottype.objects.exclude(id=self.instance.id)

    class Meta:
        model = geo_spottype
        fields = ['name', 'spot_type_father', 'update_time']
        labels = {
            'name': 'Categoria',
            'spot_type_father': 'Categoria Pai',
            'update_time' : 'Tempo de atualização',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da categoria'}),
            'spot_type_father': forms.Select(attrs={'class': 'form-control'}),
            'update_time': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o tempo de atualização em dias'}),
        }


# class SpotForm(forms.ModelForm):
    # IS_HEADQUARTERS_CHOICES = [
    #     (True, 'Sim'),
    #     (False, 'Não'),
    # ]
    # latitude = forms.FloatField(label="Latitude", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clique no mapa ou digite as coordenadas'}))
    # longitude = forms.FloatField(label="Longitude", required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clique no mapa ou digite as coordenadas'}))
    # street = forms.CharField(label='Logradouro', max_length=255, required=False)
    # number = forms.CharField(label='Número', max_length=9, required=False)
    # complement = forms.CharField(label='Complemento', max_length=255, required=False)
    # reference = forms.CharField(label='Pontos de Referência', max_length=255, required=False)
    # neighborhood = forms.CharField(label='Bairro', max_length=155, required=False)
    # city = forms.CharField(label='Cidade', max_length=155, required=False)
    # state = forms.CharField(label='Estado', max_length=2, required=False)
    # region = forms.CharField(label='Região', max_length=2, required=False)
    # country = forms.CharField(label='País', max_length=155, required=False)
    # zipcode = forms.CharField(label='CEP', required=False)
    # is_headquarters = forms.ChoiceField(
    #     label='É Matriz?',
    #     choices=IS_HEADQUARTERS_CHOICES,
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     required=True,
    # )
    # QPP = forms.ModelChoiceField(
    #     queryset=models.Qpp.objects.all(),
    #     label='QPP',
    #     widget=forms.Select(attrs={'class': 'form-control'}),
    #     required=False,
    #     empty_label='Selecione um QPP'
    # )

    # class Meta:
    #     model = models.Spot
    #     fields = ('name', 'details', 'spot_type', 'latitude', 'longitude', 'tags','location','spot_network', 'cnpj', 'parent_company','QPP')
    #     labels = {
    #         'name': 'Nome',
    #         'details': 'Informações adicionais',
    #         'spot_type': 'Tipo',
    #         'spot_network': 'Rede',
    #         'cnpj': 'CNPJ',
    #         'parent_company': 'CNPJ da matriz',
    #     }
    #     widgets = {
    #         'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do ponto'}),
    #         'details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se houver, digite informações adicionais'}),
    #         'spot_type': forms.Select(attrs={'class': 'form-control'}),
    #         'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-check', 'style': 'display: block'}),
    #         'QPP': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a qual QPP pertence'}),
    #     }

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     if commit:
    #         instance.save()
    #     return instance
    


class SpotTagsForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=models.Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2bs4'}),
        required=False,
    )
    

    class Meta:
        model = models.ProtectNetworkSpot
        fields = ('tags',)

class TagForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = ['name','details']
        labels = {
            'name': 'Nome da Tag',
            'details': 'Descrição',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da tag'}),
            'details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descrição sobre a tag'}),
        }


class ContactInfoForm(forms.ModelForm):
    class Meta:
        model = models.ContactInfo
        fields = ['name', 'phone', 'role', 'email', 'rg', 'cpf']
        labels = {
            'name': 'Contato',
            'phone': 'Telefone de contato',
            'role': 'Título ou função',
            'email': 'E-mail',
            'rg': 'RG',
            'cpf': 'CPF',
        }

    def __init__(self, *args, **kwargs):
        super(ContactInfoForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Digite o nome do contato'
        self.fields['phone'].widget.attrs['placeholder'] = '(99) 99999-9999'
        self.fields['role'].widget.attrs['placeholder'] = 'Digite a função'
        self.fields['email'].widget.attrs['placeholder'] = 'exemplo@email.com.br'
        self.fields['rg'].widget.attrs['placeholder'] = '99.999.999-9'
        self.fields['cpf'].widget.attrs['placeholder'] = '999.999.999-99'


class OpeningHoursForm(forms.ModelForm):
    class Meta:
        model = models.OpeningHours
        fields = [
            'opened_mon','open_time_mon','close_time_mon',
            'opened_tue','open_time_tue','close_time_tue',
            'opened_wed','open_time_wed','close_time_wed',
            'opened_thu','open_time_thu','close_time_thu',
            'opened_fri','open_time_fri','close_time_fri',
            'opened_sat','open_time_sat','close_time_sat',
            'opened_sun','open_time_sun','close_time_sun',
        ]
        labels = {
            'opened_mon' :"", 'open_time_mon': "",'close_time_mon': "",
            'opened_tue' :"", 'open_time_tue': "",'close_time_tue': "",
            'opened_wed' :"", 'open_time_wed': "",'close_time_wed': "",
            'opened_thu' :"", 'open_time_thu': "",'close_time_thu': "",
            'opened_fri' :"", 'open_time_fri': "",'close_time_fri': "",
            'opened_sat' :"", 'open_time_sat': "",'close_time_sat': "",
            'opened_sun' :"", 'open_time_sun': "",'close_time_sun': "",
        }

    def __init__(self, *args, **kwargs):
        super(OpeningHoursForm, self).__init__(*args, **kwargs)
        self.fields['open_time_mon'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['close_time_mon'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['open_time_tue'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['close_time_tue'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['open_time_wed'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['close_time_wed'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['open_time_thu'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['close_time_thu'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['open_time_fri'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['close_time_fri'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['open_time_sat'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['close_time_sat'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['open_time_sun'].widget.attrs['placeholder'] = 'HH:MM'
        self.fields['close_time_sun'].widget.attrs['placeholder'] = 'HH:MM'


class SpotImageForm(forms.ModelForm):
    class Meta:
        model = models.Image
        fields = ['name','imageSpot']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Digite um nome ou descrição para a imagem'}),
        }


class NetworkForm(forms.ModelForm):
    class Meta:
        model = models.Network
        fields = ['name','details']
        labels = {
            'name': 'Nome da rede',
            'details': 'Informações adicionais',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da rede'}),
            'details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se houver, insira informações adicionais'}),
        }


class ResponsibleForm(forms.ModelForm):
    responsible = forms.ModelChoiceField(
        queryset=portal_models.Military.objects.all(),
        label='Responsável',
        widget=forms.Select(attrs={'class': 'custom-select'}),
    )

    def __init__(self, *args, **kwargs):
        network = kwargs.pop('network', None)
        super().__init__(*args, **kwargs)
        self.fields['responsible'].label_from_instance = self.label_from_promotion_instance
        if network is not None:
            self.fields['network'] = forms.ModelChoiceField(
                queryset=models.Network.objects.all(),
                initial=network, 
                widget=forms.HiddenInput())

    def label_from_promotion_instance(self, obj):
        return f"{obj.rank}  {obj.nickname}"

    class Meta:
        model = models.NetworkResponsible
        fields = ['network', 'responsible', 'active']
        labels = {
            'network': 'Rede',
            'active': 'Ativo',
        }
        widgets = {
            'network': forms.Select(attrs={'class': 'custom-select'}),
            'active': forms.Select(choices=((True, 'Sim'), (False, 'Não')), attrs={'class': 'custom-select'}),
        }


class QppForm(forms.ModelForm):
    class Meta:
        model = models.Qpp
        fields = ['name', 'details']
        labels = {
            'name': 'QPP',
            'details' : 'Informações adicionais',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do QPP'}),
            'details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se houver, insira informações adicionais'}),
        }


class SecuritySurveyForm(forms.ModelForm):
    IS_BOOLEAN_CHOICES = [
        ('', '------'),
        (True, 'Sim'),
        (False, 'Não'),
    ]

    security_cameras = forms.ChoiceField(
        label='Câmeras de Segurança',
        choices=IS_BOOLEAN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    security_cameras_rec = forms.ChoiceField(
        label='Gravação de Câmeras em DVR',
        choices=IS_BOOLEAN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    private_security = forms.ChoiceField(
        label='Segurança Privada',
        choices=IS_BOOLEAN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    external_lights = forms.ChoiceField(
        label='Iluminação Externa',
        choices=IS_BOOLEAN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    alarm_system = forms.ChoiceField(
        label='Sistema de Alarme',
        choices=IS_BOOLEAN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    fire_extinguisher = forms.ChoiceField(
        label='Extintor de Incêndio',
        choices=IS_BOOLEAN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    emergency_out = forms.ChoiceField(
        label='Saída de Emergência',
        choices=IS_BOOLEAN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    fire_alarm_system = forms.ChoiceField(
        label='Sistema de Detecção de Incêndio',
        choices=IS_BOOLEAN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    security_barriers = forms.ChoiceField(
        label='Barreiras de Segurança',
        choices=IS_BOOLEAN_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    other_security_measures = forms.CharField(
        label='Outras Medidas de Segurança',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Se houver, informe medidas de segurança adicionais'}),
        required=False
    )

    class Meta:
        model = models.SecuritySurvey
        fields = ['security_cameras','security_cameras_rec','private_security','external_lights','alarm_system','fire_extinguisher','emergency_out','fire_alarm_system','security_barriers']
