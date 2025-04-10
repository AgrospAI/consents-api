from rest_framework import serializers


class BitFieldSerializer(serializers.Field):
    def to_representation(self, value):
        # Return the bitfield as a dictionary of flags
        return {flag: bool(getattr(value, flag)) for flag in value.keys()}

    def to_internal_value(self, data):
        # Expecting a dict like {"flag1": True, "flag2": False}
        if not isinstance(data, dict):
            raise serializers.ValidationError("Expected a dictionary of flags.")

        return {key: bool(val) for key, val in data.items()}
