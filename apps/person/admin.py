from django.contrib import admin

from apps.person.models import *


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'created', 'updated')
    search_fields = ('uuid',)
    

@admin.register(PersonDocument)
class PersonDocumentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'person', 'created', 'updated')
    search_fields = ('uuid', 'person')
    

@admin.register(PersonNickname)
class PersonNicknameAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'nickname', 'person', 'created', 'updated')
    search_fields = ('uuid',)


@admin.register(PersonAddress)
class PersonAddressAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'address', 'created', 'updated')
    search_fields = ('uuid',)