from camac.alexandria.extensions.common import get_service_parent_and_children
from camac.applicants.models import ROLE_CHOICES


class Scope:
    def __init__(self, group, document) -> None:
        self.group = group
        self.document = document

    def evaluate(self) -> bool:
        return True


class All(Scope):
    pass


class Service(Scope):
    def evaluate(self) -> bool:
        return self.document.modified_by_group == str(self.group.service_id)


class ServiceAndSubservice(Scope):
    def evaluate(self) -> bool:
        return self.document.modified_by_group in get_service_parent_and_children(
            self.group.service_id
        )


class Applicant(Scope):
    def evaluate(self) -> bool:
        applicants = list(
            map(
                str,
                self.document.instance_document.instance.involved_applicants.exclude(
                    role=ROLE_CHOICES.READ_ONLY.value
                ).values_list("invitee_id", flat=True),
            )
        )
        return self.document.created_by_user in applicants
