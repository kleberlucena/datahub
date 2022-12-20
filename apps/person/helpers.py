from . import tasks
from . import models

def process_external_consult(person, username, cpf=False):
    # TODO: validar atributos do usu[ario
    if cpf:
        retorno = tasks.cortex_consult(username=username, cpf=cpf)
        print(retorno)
        if retorno is not None:
            models.Registry.objects.update_or_create(system_label="CORTEX", system_uuid=retorno.uuid, person=person)
            print('Deu certo!')
        else:
            print('Deu aguia!')
