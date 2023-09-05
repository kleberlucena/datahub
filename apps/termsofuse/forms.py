from django.forms import ModelForm

from apps.termsofuse.models import AcceptTermsOfUseSASP


class AcceptTermsOfUseSASPForm(ModelForm):
    class Meta:
        model = AcceptTermsOfUseSASP
        fields = ['accept',"accept","accept",]
        
    def clean(self):
            cleaned_data = super().clean()
            accept = cleaned_data.get("accept", "accept",)

            if accept == False:
                self.add_error('accept', "O acesso ao SASP está condicionado ao aceite dos termos de uso.")