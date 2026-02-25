from typing import List

from caluma.caluma_form.models import Form as CalumaForm
from django.conf import settings

from camac.core.models import InstanceService
from camac.core.utils import generate_sort_key
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.messages import (
    Message,
)
from camac.dossier_import.writers import (
    DossierWriter,
)
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.models import Form, Instance, InstanceState
from camac.permissions import events as permissions_events
from camac.tags.models import Keyword


class KtAargauDossierWriter(DossierWriter):  # pragma: no cover
    def create_instance(self, dossier: Dossier) -> Instance:
        instance_state = InstanceState.objects.get(
            name=settings.DOSSIER_IMPORT["INSTANCE_STATE_MAPPING"].get(
                dossier._meta.target_state
            )
        )

        creation_data = dict(
            instance_state=instance_state,
            previous_instance_state=instance_state,
            user=self._user,
            group=self._group,
            form=Form.objects.get(pk=settings.DOSSIER_IMPORT["FORM_ID"]),
        )

        instance = CreateInstanceLogic.create(
            creation_data,
            caluma_user=self._caluma_user,
            camac_user=self._user,
            group=self._group,
            caluma_form=CalumaForm.objects.get(
                pk=settings.DOSSIER_IMPORT["CALUMA_FORM"]
            ),
            start_caluma=True,
        )

        InstanceService.objects.create(
            instance=instance,
            service_id=self._group.service_id,
            active=1,
            activation_date=None,
        )

        dossier_number = CreateInstanceLogic.generate_identifier(
            instance, dossier.submit_date.year
        )

        instance.case.meta.update(
            {
                "dossier-number": dossier_number,
                "dossier-number-sort": generate_sort_key(dossier_number),
            }
        )
        instance.case.save()
        permissions_events.Trigger.instance_submitted(None, instance)
        return instance

    def get_existing_dossier_ids(self, dossier_ids):
        return list(
            Keyword.objects.filter(
                name__in=dossier_ids,
                service=self._group.service,
                instances__isnull=False,
            ).values_list("name", flat=True)
        )

    def find_existing_instance(self, dossier, user):
        keyword = Keyword.objects.filter(
            name=dossier.id, service=self._group.service
        ).first()

        return keyword.instances.first() if keyword else None

    def link_instance_and_dossier(self, instance, dossier, user):
        keyword = Keyword.objects.filter(
            name=dossier.id, service=self._group.service
        ).first()

        if keyword:  # pragma: no cover
            # This only happens after an import was undone
            keyword.instances.add(instance)
        else:
            instance.keywords.create(name=dossier.id, service=self._group.service)

    def _post_create_instance(self, instance: Instance, dossier: Dossier):
        pass

    def _post_write_fields(self, instance, dossier):
        pass

    def _set_workflow_state(self, instance: Instance, dossier) -> List[Message]:
        pass
