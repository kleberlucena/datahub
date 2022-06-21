from django.contrib import admin

from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'created_at', 'updated_at')
    search_fields = ('uuid',)
