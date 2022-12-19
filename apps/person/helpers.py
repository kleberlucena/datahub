from . import tasks


def process_external_consult(username, cpf=False):
    # TODO: validar atributos do usu[ario
    if cpf:
        tasks.cortex_consult(cpf=cpf, username=username)