from caluma.caluma_workflow.models import Case

from camac.instance.mixins import InstanceQuerysetMixin


class ECHInstanceQuerysetMixin(InstanceQuerysetMixin):
    def get_base_queryset(self):
        qs = super().get_base_queryset()

        excluded_instance_ids = map(
            int,
            Case.objects.filter(workflow_id__in=["migrated"]).values_list(
                "meta__camac-instance-id", flat=True
            ),
        )

        return qs.exclude(pk__in=excluded_instance_ids)
