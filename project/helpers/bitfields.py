import json


def get_mask(value: int | str | dict, base_class) -> int:
    if isinstance(value, dict):
        value = str(value)

    if isinstance(value, str):
        if len(value) == 1:
            value = int(value)
        elif len(value) == 2:
            value = 0
        else:
            valid_flags = base_class._meta.get_field("request").flags

            val = json.loads(value.replace("'", '"').replace("True", "true"))
            indices = {k: valid_flags.index(k) for k in valid_flags}

            res = 0
            for flag in valid_flags:
                if flag in val and val[flag]:
                    res |= 1 << indices[flag]

            value = res

    return value
