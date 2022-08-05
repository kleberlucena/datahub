from django import forms

from .models import Image


class ImageForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Image
        fields = ["file",]

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
