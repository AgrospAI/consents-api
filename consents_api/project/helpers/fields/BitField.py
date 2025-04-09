from rest_framework.fields import Field


class BitField(Field):
    def __init__(self, **kwargs):
        super.__init__(**kwargs)
