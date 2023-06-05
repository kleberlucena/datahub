from django.contrib import admin

from .models import (
    VTR,
    PoliceTeam,
    InvolvedPerson,
    CharacteristicType,
    PersonalCharacteristic,
    InvolvedNickname,
    InvolvedAddresses,
    InvolvedDocuments,
    InvolvedImages,
    PoliceReport,
    InvolvedObject,
    ReportAddresses,
    ReportImages,
    ReportRequesters,
    ReportVictims,
    ReportSuspects,
    ReportWitnesses,
    ReportSupportTeams,
)

admin.site.register(VTR)
admin.site.register(PoliceTeam)
admin.site.register(InvolvedPerson)
admin.site.register(PersonalCharacteristic)
admin.site.register(CharacteristicType)
admin.site.register(InvolvedNickname)
admin.site.register(InvolvedAddresses)
admin.site.register(InvolvedDocuments)
admin.site.register(InvolvedImages)
admin.site.register(PoliceReport)
admin.site.register(InvolvedObject)
admin.site.register(ReportAddresses)
admin.site.register(ReportImages)
admin.site.register(ReportRequesters)
admin.site.register(ReportVictims)
admin.site.register(ReportSuspects)
admin.site.register(ReportWitnesses)
admin.site.register(ReportSupportTeams)
