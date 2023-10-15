from django.contrib import admin
from .models import *
from apps.protect_network import models

@admin.register(SpotType)
class TypificationAdmin(admin.ModelAdmin):
    list_display = ('name','spot_type_father')

@admin.register(Tag)
class TypificationAdmin(admin.ModelAdmin):
    list_display = ('name',)

    
@admin.register(ContactInfo)
class TypificationAdmin(admin.ModelAdmin):
    list_display = ('name','phone','role','email')

@admin.register(OpeningHours)
class TypificationAdmin(admin.ModelAdmin):
    list_display = (
        'spot',
        'opened_mon','open_time_mon','close_time_mon',
        'opened_tue','open_time_tue','close_time_tue',
        'opened_wed','open_time_wed','close_time_wed',
        'opened_thu','open_time_thu','close_time_thu',
        'opened_fri','open_time_fri','close_time_fri',
        'opened_sat','open_time_sat','close_time_sat',
        'opened_sun','open_time_sun','close_time_sun',
    )
   #list_display = ('business_day','open_time', 'close_time')

admin.site.register(models.Spot)

admin.site.register(models.SpotAddresses)

# @admin.register(Spot)
# class TypificationAdmin(admin.ModelAdmin):
#     list_display = ('name','details','spot_type', 'latitude', 'longitude','created_at','updated_at','created_by','updated_by','display_tags','next_update', 'is_temporary', 'date_initial', 'date_final','active')

#     def display_tags(self, obj):
#         return ", ".join([tag.name for tag in obj.tags.all()])

#     display_tags.short_description = "Tags"

    