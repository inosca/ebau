from django.contrib.auth import get_user_model
from rest_framework_json_api import serializers


class CurrentGroupDefault(serializers.CurrentUserDefault):
    """Current group of user is first found default group."""

    def __call__(self):
        return self.user.user_groups.filter(default_group=1).first().group


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            get_user_model().REQUIRED_FIELDS + [
                get_user_model().USERNAME_FIELD
            ]
        )
