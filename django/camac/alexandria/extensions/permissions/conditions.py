from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.caluma.api import CalumaApi


class Condition:
    def __init__(self, value, instance, request, document) -> None:
        self.value = value
        self.instance = instance
        self.request = request
        self.document = document

    def evaluate(self) -> bool:  # pragma: no cover
        return False


class ReadyWorkItem(Condition):
    def get_fill_additional_demand(self) -> WorkItem:
        if self.document:
            document_id = self.document.metainfo.get("caluma-document-id")
        else:
            document_id = self.request.parsed_data["metainfo"].get("caluma-document-id")

        if not document_id:
            return None

        return (
            WorkItem.objects.filter(
                task_id=self.value,
                document_id=document_id,
                case__family=self.instance.case,
            )
            .order_by("-created_at")
            .first()
        )

    def evaluate(self) -> bool:
        key = self.value.replace("-", "_")
        if hasattr(self, f"get_{key}"):
            work_item = getattr(self, f"get_{key}")()
        else:
            work_item = (
                WorkItem.objects.filter(
                    task_id=self.value,
                    case__family=self.instance.case,
                )
                .order_by("-created_at")
                .first()
            )

        if not work_item:
            return False

        return work_item.status == WorkItem.STATUS_READY


class InstanceState(Condition):
    def evaluate(self) -> bool:
        if isinstance(self.value, list):
            return self.instance.instance_state.name in self.value
        return self.instance.instance_state.name == self.value


class PaperInstance(Condition):
    def evaluate(self) -> bool:
        return CalumaApi().is_paper(self.instance) == self.value


class MigratedInstance(Condition):
    def evaluate(self) -> bool:
        return (
            settings.DOSSIER_IMPORT
            and self.instance.case.document.form_id
            == settings.DOSSIER_IMPORT["CALUMA_FORM"]
        ) == self.value


class BaBInstance(Condition):
    def evaluate(self) -> bool:
        return (
            settings.BAB and self.instance.case.meta.get("is-bab", False)
        ) == self.value


class BaBService(Condition):
    def evaluate(self) -> bool:
        return (
            settings.BAB
            and self.request.group.service.service_group.name
            == settings.BAB["SERVICE_GROUP"]
        ) == self.value
