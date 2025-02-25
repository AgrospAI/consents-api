from django.contrib import admin

from . import models

admin.site.register(models.Asset)
admin.site.register(models.Consent)
admin.site.register(models.ConsentHistory)
