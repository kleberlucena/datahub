from dataclasses import fields
from numpy import source
from rest_framework import serializers

from apps.person.models import *
from apps.address.api.serializers import AddressSerializer, AddressListSerializer


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


class PersonListSerializer(serializers.ModelSerializer):
    nicknames_list = PersonNicknameSerializer(many=True, source='person_nicknames')
    documents_list = PersonDocumentSerializer(many=True, source='person_documents')
    address_list = PersonAddressSerializer(many=True, source='person_address')
    
    class Meta:
        model = Person
        fields = ('uuid', 'nicknames_list', 'documents_list', 'address_list')
        
        
        
        
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