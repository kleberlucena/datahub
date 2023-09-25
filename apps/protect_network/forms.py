from django import forms
from django.forms import formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class EstablishmentForm(forms.Form):
    name = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do estabelecimento'}))
    description = forms.CharField(label='Descrição', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 40, 'placeholder': 'Informações sobre o estabelecimento e serviço prestado'}), max_length=500)
    type = forms.CharField(label='Categoria', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '------'}))
    address = forms.CharField(label='Endereço', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira um endereço'}))
    parent_company = forms.CharField(label='CNPJ da matriz', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '99.999.999/9999-99'}))
    cnpj = forms.CharField(label='CNPJ', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '99.999.999/9999-99'}))

    # Campo para indicar se é a matriz (caixa de seleção)
    IS_HEADQUARTERS_CHOICES = [
        (True, 'Sim'),
        (False, 'Não'),
    ]
    is_headquarters = forms.ChoiceField(
        label='É Matriz?',
        choices=IS_HEADQUARTERS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,
        initial=True,
    )

    def __init__(self, *args, **kwargs):
        super(EstablishmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('name'),
            Field('description'),
            Field('cnpj'),
            Field('type'),
            Field('address'),
            Field('is_headquarters'),
            Field('parent_company'),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )


class EmployeeForm(forms.Form):
    owner_name = forms.CharField(label='Nome do Proprietário', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Proprietário'}))
    
    name = forms.CharField(label='Nome do Funcionário', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    position = forms.CharField(label='Cargo', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    rg = forms.CharField(label='RG', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cpf = forms.CharField(label='CPF', max_length=14, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Telefone', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label='Foto', required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

EmployeeFormSet = formset_factory(EmployeeForm, extra=1, can_delete=True)