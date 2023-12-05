import os
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Executa todos os scripts de seed dos apps.'

    def handle(self, *args, **kwargs):
        apps_directory = 'apps'  # Diretório onde estão localizados os apps
        apps_with_seeds = [d for d in os.listdir(apps_directory)
                           if os.path.isdir(os.path.join(apps_directory, d))]

        for app_name in apps_with_seeds:
            self.stdout.write(self.style.SUCCESS(f'Executando seed para: {app_name}'))
            try:
                call_command(f'{app_name}_seed')  # Supondo que o nome do comando seja 'appname_seed'
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao executar seed para {app_name}: {e}'))

