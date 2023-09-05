import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from django_minio_backend import MinioBackend

from base.models import Base, SoftDelete
from apps.portal.models import Entity


class AcceptTermsOfUseSASP(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    accept = models.BooleanField()
    created_by = models.ForeignKey(
        User,
        related_name='accept_terms_sasp_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    entity = models.ForeignKey(
        Entity, 
        related_name='accept_terms_sasp_entity', 
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    def soft_delete_cascade_policy_action(self, **kwargs):
        # Insert here custom pre delete logic
        user = kwargs['deleted_by']
        if user is not None:
            self.deleted_by = user
        super().soft_delete_cascade_policy_action()
        # Insert here custom post delete logic

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        verbose_name = "Termos de Uso do SASP"
        verbose_name_plural = "Termos de Uso do SASP"
