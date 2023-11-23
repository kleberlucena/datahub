from django import forms
from apps.address.models import Address
from apps.document.models import DocumentType, Document, DocumentImage
from apps.image.models import Image
from .models import Person, Nickname, Tattoo, Physical, Face

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

class DocumentTypeForm(forms.ModelForm):
    class Meta:
        model = DocumentType
        fields = '__all__'

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

class DocumentImageForm(forms.ModelForm):
    class Meta:
        model = DocumentImage
        fields = '__all__'

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'

class NicknameForm(forms.ModelForm):
    class Meta:
        model = Nickname
        fields = '__all__'

class TattooForm(forms.ModelForm):
    class Meta:
        model = Tattoo
        fields = '__all__'

class PhysicalForm(forms.ModelForm):
    class Meta:
        model = Physical
        fields = '__all__'

class FaceForm(forms.ModelForm):
    class Meta:
        model = Face
        fields = '__all__'
