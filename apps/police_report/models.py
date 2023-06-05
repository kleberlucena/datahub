import uuid
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from stdimage.models import StdImageField
from django_minio_backend import MinioBackend

from base.models import Base, SoftDelete, Registry
from apps.address.models import Address
from apps.document.models import Document
from apps.image.models import Image
from apps.portal.models import Entity, Military


class CharacteristicType(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.label}"

    class Meta:
        verbose_name = "Tipo Característica"
        verbose_name_plural = "Tipos Característica"


class VTR(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    unit = models.ForeignKey(
        Entity, related_name='vtrs_unit', on_delete=models.RESTRICT)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    signal_number = models.CharField(max_length=255, null=True, blank=True)
    prefix = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    year = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.model} - {self.signal_number} - {self.prefix}"

    class Meta:
        verbose_name = "Viatura"
        verbose_name_plural = "Viaturas"


class PoliceTeam(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    vtr = models.ForeignKey(VTR, related_name='police_teams',
                            null=True, blank=True, on_delete=models.RESTRICT)
    unit = models.ForeignKey(
        Entity, related_name='teams_unit', on_delete=models.RESTRICT)
    subunit = models.ForeignKey(
        Entity, related_name='teams_subunit', on_delete=models.RESTRICT)
    QPP = models.CharField(max_length=255, null=True, blank=True)
    commander = models.ForeignKey(
        Military, related_name='teams_comander', on_delete=models.RESTRICT)
    driver = models.ForeignKey(
        Military, related_name='teams_driver', on_delete=models.RESTRICT)
    patrolman01 = models.ForeignKey(
        Military, related_name='teams_patrolman01', on_delete=models.RESTRICT)
    patrolman02 = models.ForeignKey(
        Military, related_name='teams_patrolman02', on_delete=models.RESTRICT)

    def __str__(self):
        return f"{self.commander} - {self.unit} - {self.vtr}"

    class Meta:
        verbose_name = "Guarnição Policial"
        verbose_name_plural = "Guarnições Policiais"


class InvolvedPerson(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    mother = models.CharField(max_length=255, null=True, blank=True)
    father = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField()
    phone = models.CharField(max_length=255, null=True, blank=True)
    profession = models.CharField(max_length=255, null=True, blank=True)
    addresses = models.ManyToManyField(
        Address,
        through='InvolvedAddresses',
        through_fields=('involved_person', 'address'),
    )
    images = models.ManyToManyField(
        Image,
        through='InvolvedImages',
        through_fields=('involved_person', 'image'),
    )
    documents = models.ManyToManyField(
        Document,
        through='InvolvedDocuments',
        through_fields=('involved_person', 'document'),
    )

    updated_by = models.ForeignKey(
        User,
        related_name='involved_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='involved_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    entity = models.ForeignKey(
        Entity,
        related_name='involved_entity',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )


class PersonalCharacteristic(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    description = models.CharField(max_length=1024, null=True, blank=True)
    characteristic_type = models.ForeignKey(CharacteristicType, related_name='personal_characteristics', null=True,
                                            blank=True, on_delete=models.RESTRICT)
    person_involved = models.ForeignKey(
        InvolvedPerson, related_name='personal_characteristics', on_delete=models.RESTRICT)
    file = StdImageField(
        'imagem de característica pessoal',
        storage=MinioBackend(bucket_name=settings.MINIO_MEDIA_FILES_BUCKET),
        upload_to='personal_characteristic_images',
        variations={
            'large': {'width': 720, 'height': 720, 'crop': True},
            'medium': {'width': 480, 'height': 480, 'crop': True},
            'thumbnail': {'width': 128, 'height': 128, 'crop': True},
        }, delete_orphans=True, blank=True
    )

    entity = models.ForeignKey(
        Entity,
        related_name='personal_characteristic_entity',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='personal_characteristic_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='personal_characteristic_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.description}"

    class Meta:
        verbose_name = "Característica Pessoal"
        verbose_name_plural = "Características Pessoais"


class InvolvedNickname(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    label = models.CharField("Alcunha", max_length=255)
    involved_person = models.ForeignKey(
        InvolvedPerson, related_name='nicknames', on_delete=models.RESTRICT)
    entity = models.ForeignKey(
        Entity,
        related_name='nicknames_involved_entity',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        User,
        related_name='nickname_involved_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='nickname_involved_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.label}"

    class Meta:
        verbose_name = "Alcunha"
        verbose_name_plural = "Alcunhas"


class InvolvedAddresses(models.Model):
    involved_person = models.ForeignKey(
        InvolvedPerson, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT)
    addressType = models.CharField(max_length=64, null=True, blank=True)


class InvolvedDocuments(models.Model):
    involved_person = models.ForeignKey(
        InvolvedPerson, on_delete=models.CASCADE)
    document = models.ForeignKey(Document, on_delete=models.RESTRICT)


class InvolvedImages(models.Model):
    involved_person = models.ForeignKey(
        InvolvedPerson, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.RESTRICT)


class PoliceReport(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    report_number = models.CharField(max_length=255, null=True, blank=True)
    ciop_number = models.CharField(max_length=255, null=True, blank=True)
    report_type = models.CharField(max_length=255, null=True, blank=True)
    report_code = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField('Relato')
    police_team = models.ForeignKey(
        PoliceTeam,
        related_name='police_report_team',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    support_teams = models.ManyToManyField(
        PoliceTeam,
        through='ReportSupportTeams',
        through_fields=('police_report', 'support_team'),
    )
    operational_unit = models.ForeignKey(
        Entity,
        related_name='report_unit_entity',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    operational_subunit = models.ForeignKey(
        Entity,
        related_name='report_subunit_entity',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    qpp = models.CharField(max_length=255, null=True, blank=True)
    report_date = models.DateField()
    report_time = models.TimeField()

    addresses = models.ManyToManyField(
        Address,
        through='ReportAddresses',
        through_fields=('police_report', 'address'),
    )
    images = models.ManyToManyField(
        Image,
        through='ReportImages',
        through_fields=('police_report', 'image'),
    )
    requesters = models.ManyToManyField(
        InvolvedPerson,
        related_name='report_requesters',
        through='ReportRequesters',
        through_fields=('police_report', 'requester'),
    )
    victims = models.ManyToManyField(
        InvolvedPerson,
        related_name='report_victims',
        through='ReportVictims',
        through_fields=('police_report', 'victim'),
    )
    suspects = models.ManyToManyField(
        InvolvedPerson,
        related_name='report_suspects',
        through='ReportSuspects',
        through_fields=('police_report', 'suspect'),
    )
    witnesses = models.ManyToManyField(
        InvolvedPerson,
        related_name='report_witnesses',
        through='ReportWitnesses',
        through_fields=('police_report', 'witness'),
    )

    updated_by = models.ForeignKey(
        User,
        related_name='report_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='report_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    entity = models.ForeignKey(
        Entity,
        related_name='police_reports_entity',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.report_number} - {self.ciop_number}"

    class Meta:
        verbose_name = "Ocorrência"
        verbose_name_plural = "Ocorrências"


class InvolvedObject(Base, SoftDelete):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    unit = models.ForeignKey(
        Entity, related_name='involved_object_unit', on_delete=models.RESTRICT)
    brand = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    quantity = models.DecimalField(
        max_digits=20, decimal_places=2, validators=[MinValueValidator(0.01)])
    measure = models.CharField(max_length=100)
    police_report = models.ForeignKey(
        PoliceReport,
        related_name='report_invloved_objects',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    updated_by = models.ForeignKey(
        User,
        related_name='involved_object_updater',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        User,
        related_name='involved_object_creator',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.model} - {self.quantity} - {self.measure}"

    class Meta:
        verbose_name = "Objeto apreendido"
        verbose_name_plural = "Objetos apreendidos"


class ReportAddresses(models.Model):
    police_report = models.ForeignKey(
        PoliceReport, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.RESTRICT)
    addressType = models.CharField(max_length=64, null=True, blank=True)


class ReportImages(models.Model):
    police_report = models.ForeignKey(
        PoliceReport, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.RESTRICT)


class ReportRequesters(models.Model):
    police_report = models.ForeignKey(
        PoliceReport, on_delete=models.CASCADE)
    requester = models.ForeignKey(
        InvolvedPerson, on_delete=models.RESTRICT)


class ReportVictims(models.Model):
    police_report = models.ForeignKey(
        PoliceReport, on_delete=models.CASCADE)
    victim = models.ForeignKey(
        InvolvedPerson, on_delete=models.RESTRICT)


class ReportSuspects(models.Model):
    police_report = models.ForeignKey(
        PoliceReport, on_delete=models.CASCADE)
    suspect = models.ForeignKey(
        InvolvedPerson, on_delete=models.RESTRICT)


class ReportWitnesses(models.Model):
    police_report = models.ForeignKey(
        PoliceReport, on_delete=models.CASCADE)
    witness = models.ForeignKey(
        InvolvedPerson, on_delete=models.RESTRICT)


class ReportSupportTeams(models.Model):
    police_report = models.ForeignKey(
        PoliceReport, on_delete=models.CASCADE)
    support_team = models.ForeignKey(PoliceTeam, on_delete=models.RESTRICT)
