import orjson
from bitfield import BitField
from consents.models import RequestFlags
from rest_framework import serializers


class BitFieldSerializer(serializers.Field):
    def to_representation(self, value):
        return {flag: bool(val) for flag, val in value.items() if bool(val)}

    def to_internal_value(self, data: int | dict):
        try:
            data = orjson.loads(data)
        except orjson.JSONDecodeError as e:
            raise serializers.ValidationError(
                f"Invalid JSON format. Error: {e} with data: {data}"
            )

        if isinstance(data, int):
            return data

        # Check if all keys are valid flags
        invalid_keys = [
            key for key in data.keys() if key not in BitField(RequestFlags.flags).flags
        ]
        if invalid_keys:
            raise serializers.ValidationError(
                f"Invalid flags: {', '.join(invalid_keys)}, expected keys: {', '.join(RequestFlags.flags)}"
            )

        return {key: bool(val) for key, val in data.items()}
