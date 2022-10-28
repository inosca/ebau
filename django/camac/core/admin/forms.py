from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from camac.core.models import InstanceResource, InstanceResourceT, Resource, ResourceT
from camac.user.admin.fields import CamacBooleanField, CamacLanguageField


class ResourceTForm(ModelForm):
    language = CamacLanguageField()

    class Meta:
        model = ResourceT
        exclude = []


class ResourceForm(ModelForm):
    hidden = CamacBooleanField(label=_("Hidden?"))

    class Meta:
        model = Resource
        exclude = []


class InstanceResourceTForm(ModelForm):
    language = CamacLanguageField()

    class Meta:
        model = InstanceResourceT
        exclude = []


class InstanceResourceForm(ModelForm):
    hidden = CamacBooleanField(label=_("Hidden?"))

    class Meta:
        model = InstanceResource
        exclude = []
