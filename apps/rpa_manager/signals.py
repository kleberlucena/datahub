from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.rpa_manager.models import Aeronave, HistoricoAlteracoesAeronave

@receiver(post_save, sender=Aeronave)
def update_titulo_aeronave(sender, instance, **kwargs):
    print("--- Signals iniciado ---")
    historicos = HistoricoAlteracoesAeronave.objects.filter(aeronave=instance)
    
    for historico in historicos:
        historico.titulo_aeronave = instance.prefixo
        historico.save()
        