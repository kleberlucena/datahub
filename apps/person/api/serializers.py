from dataclasses import fields
from numpy import source
from rest_framework import serializers

from apps.person.models import *
from apps.address.api.serializers import AddressSerializer, AddressListSerializer
from apps.image.api.serializers import ImageSerializer


class PersonNicknameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PersonNickname
        fields = ('uuid', 'nickname')
        

class PersonDocumentSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = PersonDocument
        fields = ('uuid',)
        

class PersonAddressSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    
    class Meta:
        model = PersonAddress
        fields = ('uuid', 'address')
        
        
class PersonImageSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    
    class Meta:
        model = PersonImage
        fields = ('uuid', 'image', 'description')
        
        
class PersonImageFaceSerializer(serializers.ModelSerializer):
    image = ImageSerializer()
    
    class Meta:
        model = PersonImageFace
        fields = ('uuid', 'image')


class PersonListSerializer(serializers.ModelSerializer):
    nicknames = PersonNicknameSerializer(many=True, source='person_nickname')
    documents = PersonDocumentSerializer(many=True, source='person_document')
    addresses = PersonAddressSerializer(many=True, source='person_address')
    images = PersonImageSerializer(many=True, source='person_image')
    faces = PersonImageFaceSerializer(many=True, source='person_image_face')
    
    class Meta:
        model = Person
        fields = (
            'uuid', 'nicknames', 'documents', 'addresses','images', 'faces')
        
    