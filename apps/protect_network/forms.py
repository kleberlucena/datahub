from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class EstablishmentForm(forms.Form):
    name = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do estabelecimento'}))
    description = forms.CharField(label='Descrição', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 40, 'placeholder': 'Resumo sobre o estabelecimento e serviço prestado'}), max_length=500)
    cnpj = forms.CharField(label='CNPJ', max_length=14, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '99.999.999/9999-99'}))
    type = forms.CharField(label='Categoria', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '------'}))
    address = forms.CharField(label='Endereço', widget=forms.Textarea(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(EstablishmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name'),
            Field('description'),
            Field('cnpj'),
            Field('type'),
            Field('address'),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )
