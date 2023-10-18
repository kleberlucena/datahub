from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from . import models


class SpotTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['spot_type_father'].queryset = models.SpotType.objects.exclude(id=self.instance.id)

    class Meta:
        model = models.SpotType
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



class SpotForm(forms.ModelForm):
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


    class Meta:
        model = models.Spot
        fields = ('name', 'details', 'spot_type', 'latitude', 'longitude', 'tags','location','spot_network', 'cnpj', 'parent_company','QPP')
        labels = {
            'name': 'Ponto',
            'details': 'Informações adicionais',
            'spot_type': 'Tipo',
            'spot_network': 'Rede',
            'cnpj': 'CNPJ',
            'parent_company': 'CNPJ da matriz',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do ponto'}),
            'details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Se houver, digite informações adicionais'}),
            'spot_type': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-check', 'style': 'display: block'}),
            'QPP': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a qual QPP pertence'}),
        }

    # def __init__(self, *args, **kwargs):
    #     super(SpotForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #     self.helper.layout = Layout(
    #         Field('address'),
    #         Submit('submit', 'Submit', css_class='btn btn-primary'),
    #         Field('street', css_class='form-control'),
    #         Field('number', css_class='form-control'),
    #         Field('complement', css_class='form-control'),
    #         Field('reference', css_class='form-control'),
    #         Field('neighborhood', css_class='form-control'),
    #         Field('city', css_class='form-control'),
    #         Field('state', css_class='form-control'),
    #         Field('region', css_class='form-control'),
    #         Field('country', css_class='form-control'),
    #         Field('zipcode', css_class='form-control'),
    #     )


    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
    


class SpotTagsForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=models.Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2bs4'}),
        required=False,
    )
    
    class Meta:
        model = models.Spot
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
        fields = ['name', 'phone', 'role', 'email']
        labels = {
            'name': 'Contato',
            'phone': 'Telefone de contato',
            'role': 'Título ou função',
            'email': 'E-mail',
        }

    def __init__(self, *args, **kwargs):
        super(ContactInfoForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Digite o nome do contato'
        self.fields['phone'].widget.attrs['placeholder'] = '(99) 99999-9999'
        self.fields['role'].widget.attrs['placeholder'] = 'Digite a função'
        self.fields['email'].widget.attrs['placeholder'] = 'exemplo@email.com.br'



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
