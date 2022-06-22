from dataclasses import fields
from rest_framework import serializers

from apps.person.models import *


class PersonNicknameSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PersonNickname
        fields = ('uuid', 'nickname')
        

class PersonDocumentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PersonDocument
        fields = ('uuid',)


class PersonSerializer(serializers.ModelSerializer):
    nicknames = PersonNicknameSerializer(many=True, source='person_nicknames')
    documents = PersonDocumentSerializer(many=True, source='person_documents')
    
    class Meta:
        model = Person
        fields = ('uuid', 'nicknames', 'documents')
        
        
        
        
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