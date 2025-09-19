from rest_framework.serializers import (
    CharField,
    HyperlinkedIdentityField,
    HyperlinkedModelSerializer,
    ModelSerializer,
    SerializerMethodField,
    IntegerField,
)

from assets.models import Asset


class ListAsset(HyperlinkedModelSerializer):
    url = HyperlinkedIdentityField(view_name="assets-detail", lookup_field="did")
    owner = CharField(source="owner.address")
    type = CharField(source="get_type_display")
    chain_id = IntegerField()

    class Meta:
        model = Asset
        fields = (
            "url",
            "did",
            "owner",
            "type",
            "chain_id",
        )


class DetailAsset(ModelSerializer):
    owner = CharField(source="owner.address")
    type = CharField(source="get_type_display")
    chain_id = IntegerField()
    pending_consents = SerializerMethodField()

    class Meta:
        model = Asset
        fields = (
            "did",
            "owner",
            "type",
            "pending_consents",
            "chain_id",
        )

    def get_pending_consents(self, obj):
        return Asset.helper.get_pending_consents(obj)
