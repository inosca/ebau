from pyjexl.analysis import ValidatingAnalyzer


class ExtractTransformSubjectAnalyzer(ValidatingAnalyzer):
    """Extract all subject values of given transforms."""

    def __init__(self, config, transforms):
        self.transforms_with_subject = transforms
        super().__init__(config)

    def visit_Transform(self, transform):
        if transform.name in self.transforms_with_subject:
            yield transform.subject.value

        yield from self.generic_visit(transform)
