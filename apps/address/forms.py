from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Address
        # fields = '__all__'
        fields = ["street", "number", "complement", "neighborhood", "city", "state", "region", "country", "zipcode"]

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

