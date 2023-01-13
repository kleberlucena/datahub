from django.contrib import admin

from . import models


@admin.register(models.PersonBNMP)
class PersonBNMPAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'idpessoa', 'numeroCPF', 'nome', 'nomeMae', 'dataNascimento')
    search_fields = ('uuid',)