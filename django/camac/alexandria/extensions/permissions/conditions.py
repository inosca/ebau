from caluma.caluma_workflow.models import WorkItem

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
    def get_additional_demand(self) -> WorkItem:
        if self.document:
            document_id = self.document.metainfo["caluma-document-id"]
        else:
            document_id = self.request.data["metainfo"]["caluma-document-id"]

        return (
            WorkItem.objects.filter(
                task_id=self.value,
                document_id=document_id,
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

        return work_item and work_item.status == WorkItem.STATUS_READY


class InstanceState(Condition):
    def evaluate(self) -> bool:
        if isinstance(self.value, list):
            return self.instance.instance_state.name in self.value
        return self.instance.instance_state.name == self.value


class PaperInstance(Condition):
    def evaluate(self) -> bool:
        return CalumaApi().is_paper(self.instance)
