from django import forms

from apps.portal.models import Military
from apps.rpa.models import PoliceGroup
from apps.rpa.utils.addAttributes import addAttributes

class PoliceGroupForm(forms.ModelForm):
 
    class Meta:
        model = PoliceGroup
        fields = ['driver', 
                  'remote_pilot', 
                  'observer_pilot', 
                  'phone', 
                  'location',]
        
        widgets = {
            'remote_pilot': forms.HiddenInput(),    
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        self.fields['driver'].widget.attrs.update({
            'placeholder': 'Insira um motorista'
        })
        self.fields['observer_pilot'].widget.attrs.update({
            'placeholder': 'Insira um piloto observador'
        })
        self.fields['phone'].widget.attrs.update({
            'placeholder': "Somente números, exemplo: '83988776655'"
        })
        self.fields['location'].widget.attrs.update({
            'placeholder': 'Insira o local de atuação'
        })

        campos = ['driver', 
                  'remote_pilot', 
                  'observer_pilot', 
                  'phone', 
                  'location',]
        
        for campo in campos:
            addAttributes(self, campo, campo, 'form-control')    
    
    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            self.add_error("phone", "Favor inserir dígitos numéricos. Por exemplo, 83988776655.")
        return phone

    def clean_observer_pilot(self):
        observer_pilot = self.cleaned_data.get('observer_pilot')
        if observer_pilot and not Military.objects.filter(id=observer_pilot.id).exists():
            raise forms.ValidationError("Piloto observador não existe.")
        return observer_pilot

    def clean_driver(self):
        driver = self.cleaned_data.get('driver')
        if driver and not Military.objects.filter(id=driver.id).exists():
            raise forms.ValidationError("Motorista não existe.")
        return driver

    def clean_remote_pilot(self):
        remote_pilot = self.cleaned_data.get('remote_pilot')
        if remote_pilot and not Military.objects.filter(id=remote_pilot.id).exists():
            raise forms.ValidationError("Piloto remoto não existe.")
        return remote_pilot
    
    def clean(self):
        cleaned_data = super().clean()
        remote_pilot = cleaned_data.get('remote_pilot')
        observer_pilot = cleaned_data.get('observer_pilot')
        driver = cleaned_data.get('driver')

        # Verifica se os papéis não se sobrepõem
        if remote_pilot == observer_pilot or remote_pilot == driver:
            self.add_error('remote_pilot', "O piloto remoto não pode ser o mesmo que o piloto observador ou motorista.")
        if observer_pilot == remote_pilot or observer_pilot == driver:
            self.add_error('observer_pilot', "O piloto observador não pode ser o mesmo que o piloto remoto ou motorista.")
        if driver == remote_pilot or driver == observer_pilot:
            self.add_error('driver', "O motorista não pode ser o mesmo que o piloto remoto ou piloto observador.")

        # Verifica se os pilotos não estão em outras guarnições
        self.validate_pilot_assignments(remote_pilot, observer_pilot, driver)

        return cleaned_data

    def validate_pilot_assignments(self, remote_pilot, observer_pilot, driver):
        if remote_pilot and PoliceGroup.objects.filter(observer_pilot=remote_pilot).exclude(id=self.instance.id).exists():
            self.add_error('remote_pilot', "O piloto remoto já está sendo utilizado como piloto observador em outra guarnição.")
        if observer_pilot and PoliceGroup.objects.filter(remote_pilot=observer_pilot).exclude(id=self.instance.id).exists():
            self.add_error('observer_pilot', "O piloto observador já está sendo utilizado como piloto remoto em outra guarnição.")
        if driver and PoliceGroup.objects.filter(remote_pilot=driver).exclude(id=self.instance.id).exists():
            self.add_error('driver', "O motorista já está sendo utilizado como piloto remoto em outra guarnição.")


# from django import forms
# from django.contrib.auth.models import User
# from apps.portal.models import Military
# from apps.rpa.models import PoliceGroup
# from apps.rpa.utils.addAttributes import addAttributes


# class PoliceGroupForm(forms.ModelForm):
 
#     class Meta:
#         model = PoliceGroup
#         fields = ['driver', 
#                   'remote_pilot', 
#                   'observer_pilot', 
#                   'phone', 
#                   'location',
#                   ]
        
#         widgets = {
#             'remote_pilot': forms.HiddenInput(),    
#         }
        
#     def __init__(self, *args, **kwargs):
#         print(64*'#')
#         print('no PoliceGroupForm.__init__')
#         print(64*'#')
#         super().__init__(*args, **kwargs)
      
#         self.fields['driver'].widget.attrs.update({
#             'placeholder': 'Insira um motorista'
#         })
#         self.fields['driver'].queryset = Military.objects.none()
        
#         self.fields['observer_pilot'].widget.attrs.update({
#             'placeholder': 'Insira um piloto observador'
#         })

#         self.fields['observer_pilot'].queryset = Military.objects.none()

#         self.fields['phone'].widget.attrs.update({
#             'placeholder': "Somente números, exemplo: '83988776655'"
#         })
#         self.fields['location'].widget.attrs.update({
#             'placeholder': 'Insira o local de atuação'
#         })

#         campos = ['driver', 
#                   'remote_pilot', 
#                   'observer_pilot', 
#                   'phone', 
#                   'location',
#                   ]
        
#         for campo in campos:
#             addAttributes(self, campo, campo, 'form-control')    
    
#     def clean_phone(self):
#         phone = self.cleaned_data['phone']
#         if not phone.isdigit():
#             self.add_error("phone", "Favor inserir dígitos numéricos. Por exemplo, 83988776655.")
#         return phone

    
#     def clean(self):
#         print(64*'#')
#         print('no PoliceGroupForm.clean')
#         print(64*'#')
#         cleaned_data = super().clean()
#         remote_pilot = cleaned_data.get('remote_pilot')
#         observer_pilot = cleaned_data.get('observer_pilot')
#         driver = cleaned_data.get('driver')

#         if remote_pilot == observer_pilot:
#             self.add_error('remote_pilot', "O piloto remoto não pode ser o mesmo que o piloto observador ou motorista.")
        
#         if observer_pilot == remote_pilot:
#             self.add_error('observer_pilot', "O piloto observador não pode ser o mesmo que o piloto remoto.")

#         if PoliceGroup.objects.filter(observer_pilot=remote_pilot).exclude(id=self.instance.id).exists():
#             self.add_error('remote_pilot', "O piloto remoto já está sendo utilizado como piloto observador em outra guarnição.")

#         if PoliceGroup.objects.filter(driver=remote_pilot).exclude(id=self.instance.id).exists():
#             self.add_error('remote_pilot', "O piloto remoto já está sendo utilizado como motorista em outra guarnição.")

#         if PoliceGroup.objects.filter(remote_pilot=observer_pilot).exclude(id=self.instance.id).exists():
#             self.add_error('observer_pilot', "O piloto observador já está sendo utilizado como piloto remoto em outra guarnição.")

#         if PoliceGroup.objects.filter(driver=observer_pilot).exclude(id=self.instance.id).exists():
#             self.add_error('observer_pilot', "O piloto observador já está sendo utilizado como motorista em outra guarnição.")

#         if PoliceGroup.objects.filter(remote_pilot=driver).exclude(id=self.instance.id).exists():
#             self.add_error('driver', "O motorista já está sendo utilizado como piloto remoto em outra guarnição.")

#         if PoliceGroup.objects.filter(observer_pilot=driver).exclude(id=self.instance.id).exists():
#             self.add_error('driver', "O motorista já está sendo utilizado como piloto observador em outra guarnição.")

#         if PoliceGroup.objects.filter(driver=driver).exclude(id=self.instance.id).exists():
#             self.add_error('driver', "O motorista já está sendo utilizado como motorista em outra guarnição.")

#         return cleaned_data