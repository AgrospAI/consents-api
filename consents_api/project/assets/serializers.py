from rest_framework.serializers import (
    CharField,
    HyperlinkedIdentityField,
    HyperlinkedModelSerializer,
    ModelSerializer,
)

from assets.models import Asset


class ListAsset(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="assets-detail")

    class Meta:
        model = Asset
        fields = ("url",)


class DetailAsset(ModelSerializer):
    owner = CharField(source="owner.address")

    class Meta:
        model = Asset
        fields = (
            "did",
            "owner",
        )
