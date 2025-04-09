from bitfield import BitField
from bitfield.forms import BitFieldCheckboxSelectMultiple
from django.contrib import admin

from consents import models


class BitfieldAdmin(admin.ModelAdmin):
    formfield_overrides = {BitField: {"widget": BitFieldCheckboxSelectMultiple}}


admin.site.register(models.Consent, BitfieldAdmin)
admin.site.register(models.ConsentResponse, BitfieldAdmin)
