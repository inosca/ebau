from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from camac.user.admin.fields import CamacBooleanField, CamacLanguageField
from camac.user.models import (
    Group,
    GroupT,
    RoleT,
    Service,
    ServiceGroupT,
    ServiceRelation,
    ServiceT,
    User,
    UserGroup,
)


class GroupTForm(ModelForm):
    language = CamacLanguageField()

    class Meta:
        model = GroupT
        exclude = []


class GroupForm(ModelForm):
    disabled = CamacBooleanField(label=_("Disabled?"))

    class Meta:
        model = Group
        exclude = []


class UserGroupForm(ModelForm):
    default_group = CamacBooleanField()

    class Meta:
        model = UserGroup
        exclude = ["created_by"]


class ServiceForm(ModelForm):
    disabled = CamacBooleanField(label=_("Disabled?"))
    notification = CamacBooleanField(label=_("Receive notifications?"))

    class Meta:
        model = Service
        exclude = []


class UserForm(ModelForm):
    disabled = CamacBooleanField(label=_("Disabled?"))

    class Meta:
        model = User
        exclude = []


class ServiceTForm(ModelForm):
    language = CamacLanguageField()

    class Meta:
        model = ServiceT
        exclude = []


class RoleTForm(ModelForm):
    language = CamacLanguageField()

    class Meta:
        model = RoleT
        exclude = []


class ServiceGroupTForm(ModelForm):
    language = CamacLanguageField()

    class Meta:
        model = ServiceGroupT
        exclude = []


class ServiceRelationForm(ModelForm):
    class Meta:
        model = ServiceRelation
        exclude = []
