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
    nickname_list = PersonNicknameSerializer(many=True, source='person_nickname')
    document_list = PersonDocumentSerializer(many=True, source='person_document')
    address_list = PersonAddressSerializer(many=True, source='person_address')
    image_list = PersonImageSerializer(many=True, source='person_image')
    face_list = PersonImageFaceSerializer(many=True, source='person_image_face')
    
    class Meta:
        model = Person
        fields = (
            'uuid', 'nickname_list', 'document_list', 'address_list','image_list', 'face_list')
        
        
        
        
'''
[
    {
        "id": "UUID",
        "person_face": [
            {
                "id": "UUID",
                "person_id": "UUID",
                "image": {
                    "path": "https://...",
                    "path_thumbnail": "https://..."
                }
            }
        ],
        "person_nickname": [
            {
                "id": "UUID",
                "person_id": "UUID",
                "nickname": "alcunha"
            }
        ],
        "person_document": [
            {
                "id": "UUID",
                "person_id": "UUID",
                "document": {
                    "id": "UUID",
                    "number": "123123"
                }
            }
        ]
    }
]
'''