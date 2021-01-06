from django.utils.translation import gettext_lazy as _

from camac.caluma.api import CalumaApi
from camac.instance.models import Instance
from camac.user.models import Service


def set_construction_control(instance: Instance) -> Service:
    involved_municipalities = instance.instance_services.filter(
        service__service_group__name="municipality"
    )
    active_municipality = involved_municipalities.filter(active=1).first()

    if active_municipality:
        # active service is a municipality, take this one
        municipality = active_municipality.service
    elif involved_municipalities.exists():
        # active service is an RSTA, take involved (but not active) municipality
        municipality = involved_municipalities.first().service
    else:
        # no involved municipality, take fallback from form
        municipality = Service.objects.get(pk=CalumaApi().get_municipality(instance))

    try:
        construction_control = Service.objects.get(
            service_group__name="construction-control",
            trans__language="de",
            trans__name=municipality.trans.get(language="de").name.replace(
                "Leitbehörde", "Baukontrolle"
            ),
        )
    except Service.DoesNotExist:  # pragma: no cover
        raise Exception(
            _(
                "Could not find construction control for instance %(id)d"
                % {"id": instance.pk}
            )
        )

    instance.instance_services.create(service=construction_control, active=1)

    return construction_control
