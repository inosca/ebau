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
