from rest_framework.serializers import (
    CharField,
    HyperlinkedIdentityField,
    HyperlinkedModelSerializer,
    ModelSerializer,
    SerializerMethodField,
)

from assets.models import Asset


class ListAsset(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="assets-detail", lookup_field="did")
    owner = CharField(source="owner.address")
    type = CharField(source="get_type_display")

    class Meta:
        model = Asset
        fields = (
            "url",
            "did",
            "owner",
            "type",
        )


class DetailAsset(ModelSerializer):
    owner = CharField(source="owner.address")
    type = CharField(source="get_type_display")
    pending_consents = SerializerMethodField()

    class Meta:
        model = Asset
        fields = (
            "did",
            "owner",
            "type",
            "pending_consents",
        )

    def get_pending_consents(self, obj):
        return Asset.objects.get_pending_consents(obj)
