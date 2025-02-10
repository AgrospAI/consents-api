from django.db import models

from auth.models import Web3User

class ConsentPetition(models.Model):

    class Meta:
        # Limit to one petition for user for each asset
        constraints = [
            models.UniqueConstraint(fields=['asset_did', 'user'], name='unique_asset_did_user')
        ]

    asset_did = models.CharField(max_length=255)
    user = models.ForeignKey(Web3User, on_delete=models.CASCADE)

    comments = models.TextField(blank=True, null=True)    
