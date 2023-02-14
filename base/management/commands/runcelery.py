import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import execute_from_command_line

class Command(BaseCommand):
    help = f"Inicia o celery"
    def handle(self, *args, **options):
        self.stdout.write(f"Iniciando o commando celery")
        print(subprocess.Popen(f"python -m celery -A project worker -B -l INFO", shell=True, stdout=subprocess.PIPE).stdout.read())
        self.stdout.write(self.style.SUCCESS("Done."))
    
if __name__ == "__main__":
    execute_from_command_line(["manage.py", "runcelery"])