import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line


class Command(BaseCommand):

    help = f"Roda o projeto na porta {settings.PROJECT_PORT}"

    def handle(self, *args, **options):
        self.stdout.write(f"Rodando o projeto na porta {settings.PROJECT_PORT}")
        print(subprocess.Popen(f"python manage.py runserver {settings.PROJECT_PORT}", shell=True, stdout=subprocess.PIPE).stdout.read())
        self.stdout.write(self.style.SUCCESS("Done."))


if __name__ == "__main__":
    execute_from_command_line(["manage.py", "runproject"])