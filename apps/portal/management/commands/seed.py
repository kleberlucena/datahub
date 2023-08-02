from django.core.management import call_command
from datetime import datetime as date
from django.core.management.base import BaseCommand
from django.utils.timezone import now
from apps.portal.models import *


class Command(BaseCommand):
    help = 'Insert seed data'

    def handle(self, *args, **options):

        #         criando entity
        entidade1 = Entity.objects.create(id_portal=1,
                                          name="Batalhão 1",
                                          code="1",
                                          father=0,
                                          child_exists=False,
                                          category=1,
                                          hierarchy=0)
        entidade2 = Entity.objects.create(id_portal=2,
                                          name="Batalhão 2",
                                          code="2",
                                          father=0,
                                          child_exists=False,
                                          category=1,
                                          hierarchy=0)

        military1 = Military.objects.create(
            name="Antônio da Silva Filho",
            admission_date="2005-07-04",
            birthdate="1990-07-04",
            father="Joaquim Barbosa",
            mather="Maria das Neves",
            place_of_birth="1983-07-14",
            nickname="Silva",
            activity_status="Ativa",
            genre="M",
            email="teste_gmail.com",
            marital_status="Solteiro",
            phone="83999990000",
            address="Rua Joaquim Nabuco",
            number="30",
            complement="Perto do posto",
            district="Torre",
            city="João Pessoa",
            state="PB",
            zipcode="58000-000",
            register="5269999",
            cpf="123.123.123-11",
            url_image="não tem")

        military2 = Military.objects.create(
            name="José Meireles Silva",
            admission_date="2005-07-04",
            birthdate="1990-07-04",
            father="Joaquim Barbosa 2",
            mather="Maria das Neves 2",
            place_of_birth="1983-07-14",
            nickname="Meireles",
            activity_status="Ativa",
            genre="M",
            email="teste2_gmail.com",
            marital_status="Solteiro",
            phone="83999990000",
            address="Rua Joaquim Nabuco",
            number="30",
            complement="Perto do posto",
            district="Torre",
            city="João Pessoa",
            state="PB",
            zipcode="58000-000",
            register="5268888",
            cpf="123.123.123-12",
            url_image="não tem")

        HistoryTransfer.objects.create(
            military=military1, entity=entidade1, date_start=date.now(), obs="cadastro pela seed")

        HistoryTransfer.objects.create(
            military=military2, entity=entidade2, date_start=date.now(), obs="cadastro pela seed")

        Promotion.objects.create(military=military1, rank="SD")
        Promotion.objects.create(military=military2, rank="SD")
        Promotion.objects.create(military=military1, rank="CB")
