from django.contrib import admin
from django.utils.translation import gettext as _

from hydra_datastore.models import EntryModel, DatasetModel
# Register your models here.



class EntryInline(admin.TabularInline):
    model = EntryModel
    verbose_name = _('Entry')
    verbose_name_plural = _('Entries')
    fk_name = 'dataset'
    fields = ['coordinates', 'data']
    extra = 0

@admin.register(DatasetModel)
class DataseAdmin(admin.ModelAdmin):
    fields = ['timestamp', 'schema']
    icon = '<i class="material-icons">attachment</i>'
    list_display = ['id', 'timestamp', 'schema']

# @admin.register(datastore_models.ReservationModel)
# class ReservationAdmin(admin.ModelAdmin):
#     fields = ['hotel', 'room_type', 'board']
#     # inlines = [PricePerPersonInline]
#
# @admin.register(datastore_models.RouteModel)
# class RouteAdmin( admin.ModelAdmin):
#     fields = ['flight_provider', 'departure', 'arrival', 'cheapest_out', 'cheapest_return', 'bag_type']
#     # inlines = [PricePerPersonInline]
#
#
# @admin.register(datastore_models.JourneyModel)
# class JourneyAdmin( admin.ModelAdmin):
#     fields = ['date', 'number_of_nights', 'number_of_passengers', 'stay', 'inbound_carrier', 'outbound_carrier']
#     inlines = [PricePerPersonInline]
