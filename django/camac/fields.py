from rest_framework.fields import BooleanField


class CamacBooleanField(BooleanField):
    """Field to expose boolean but store integer value.

    CAMAC historically stores boolean values as small integer values (1 or 0) in
    the DB. However, we don't want the API to expose an integer but a boolean
    value.
    """

    def to_internal_value(self, data):
        return int(super().to_internal_value(data))
