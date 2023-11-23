from django.core.management import call_command
from datetime import datetime as date
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from apps.portal.models import *


class Command(BaseCommand):

    def create_groups(self):
        print("Chamou Command Portal")

    def handle(self, *args, **kwargs):
       self.create_groups()
       
       