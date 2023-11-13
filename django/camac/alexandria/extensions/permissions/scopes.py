from camac.alexandria.extensions.common import get_service_parent_and_children


class Scope:
    def __init__(self, user, document) -> None:
        self.user = user
        self.document = document

    def evaluate(self) -> bool:
        return True


class All(Scope):
    pass


class Service(Scope):
    def evaluate(self) -> bool:
        return self.document.created_by_group == str(self.user.group)


class ServiceAndSubservice(Scope):
    def evaluate(self) -> bool:
        return self.document.created_by_group in get_service_parent_and_children(
            self.user.group
        )
