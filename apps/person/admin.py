from django.contrib import admin

from apps.person.models import Person, PersonDocument, PersonNickname


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'created_at', 'updated_at')
    search_fields = ('uuid',)
    

@admin.register(PersonDocument)
class PersonDocumentAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'person', 'created_at', 'updated_at')
    search_fields = ('uuid', 'person')
    

@admin.register(PersonNickname)
class PersonNicknameAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'nickname', 'person', 'created_at', 'updated_at')
    search_fields = ('uuid',)
