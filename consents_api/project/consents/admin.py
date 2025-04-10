from bitfield import BitField, BitHandler
from bitfield.forms import BitFieldCheckboxSelectMultiple
from django.contrib import admin
from django import forms

from consents import models


class BitfieldAdmin(admin.ModelAdmin):
    formfield_overrides = {BitField: {"widget": BitFieldCheckboxSelectMultiple}}


class ConsentAdminForm(forms.ModelForm):
    class Meta:
        model = models.Consent
        fields = "__all__"

    def clean_flags(self):
        data = self.cleaned_data["request"]

        if isinstance(data, int):
            return BitHandler(
                data, flags=self._meta.model._meta.get_field("request").flags
            )
        return data


admin.site.register(models.Consent, BitfieldAdmin)
admin.site.register(models.ConsentResponse, BitfieldAdmin)
