from . import tasks
from . import models


def process_external_consult(person, username, cpf=False):
    # TODO: validar atributos do usu[ario
    if cpf:
        try:
            retorno = tasks.cortex_consult(username=username, cpf=cpf)
            models.Registry.objects.update_or_create(system_label="CORTEX", system_uuid=retorno.uuid, person=person)
        except:
            print("N'ao encontrado registro no cortex")
    else:
        print("N'ao informado cpf")


def validate_document(number):
    try:
        instance = models.Document.objects.filter(number=number)
        return instance
    except:
        return None