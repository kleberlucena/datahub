from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class EstablishmentForm(forms.Form):
    name = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do estabelecimento'}))
    description = forms.CharField(label='Descrição', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'cols': 40, 'placeholder': 'Informações sobre o estabelecimento e serviço prestado'}), max_length=500)
    type = forms.CharField(label='Categoria', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '------'}))
    address = forms.CharField(label='Endereço', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insira um endereço'}))
    parent_company = forms.CharField(label='CNPJ da matriz', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '99.999.999/9999-99'}))
    cnpj = forms.CharField(label='CNPJ', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '99.999.999/9999-99'}))
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
            Submit('submit', 'Submit', css_class='btn btn-primary'),
            Field('street', css_class='form-control'),
            Field('number', css_class='form-control'),
            Field('complement', css_class='form-control'),
            Field('reference', css_class='form-control'),
            Field('neighborhood', css_class='form-control'),
            Field('city', css_class='form-control'),
            Field('state', css_class='form-control'),
            Field('region', css_class='form-control'),
            Field('country', css_class='form-control'),
            Field('zipcode', css_class='form-control'),
        )


class EmployeeForm(forms.Form):
    GENDER_CHOICES = (
        ('', '------'),
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    )
    name = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    position = forms.CharField(label='Cargo ou função', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    rg = forms.CharField(label='RG', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    cpf = forms.CharField(label='CPF', max_length=14, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Telefone', max_length=20,required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', required=False,max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label='Foto', required=False, widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    start_date = forms.DateField(label='Data de Ingresso', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    end_date = forms.DateField(label='Data de Desligamento', required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    gender = forms.ChoiceField(label='Sexo', choices=GENDER_CHOICES, initial='', widget=forms.Select(attrs={'class': 'form-control'}))


class SecurityForm(forms.Form):
    YES_NO_CHOICES = [
        ('Sim', 'Sim'),
        ('Não', 'Não'),
    ]
    PRIVATE_SECURITY_CHOICES = [
        ('Não', 'Não'),
        ('Segurança privada', 'Segurança privada'),
        ('Vigia de rua', 'Vigia de rua'),
    ]
    SECURITY_CAMERAS_CHOICES = [
        ('Não', 'Não'),
        ('Sim, apenas para monitoramento', 'Sim, apenas para monitoramento'),
        ('Sim, monitoramento e gravação', 'Sim, monitoramento e gravação'),
    ]
    ALARM_SYSTEM_CHOICES = [
        ('Não', 'Não'),
        ('Sim, apenas alarme local', 'Sim, apenas alarme local'),
        ('Sim, alarme local e central de monitoramento', 'Sim, alarme local e central de monitoramento'),
    ]

    alarm_system = forms.ChoiceField(label='Sistemas de Alarme', choices=ALARM_SYSTEM_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    security_cameras = forms.ChoiceField(label='Câmeras de Segurança', choices=SECURITY_CAMERAS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    outdoor_lighting = forms.ChoiceField(label='Iluminação externa adequada?', choices=YES_NO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    gates = forms.ChoiceField(label='Portões de acesso', choices=YES_NO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    electric_fence = forms.ChoiceField(label='Cerca elétrica', choices=YES_NO_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    private_security = forms.ChoiceField(label='Segurança Privada', choices=PRIVATE_SECURITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
