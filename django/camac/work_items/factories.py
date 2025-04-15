from factory import Faker
from factory.django import DjangoModelFactory

from camac.work_items.models import WorkItemTemplate


class WorkItemTemplateFactory(DjangoModelFactory):
    name = Faker("word")
    description = Faker("sentence")
    lead_time = Faker("pyint", min_value=1, max_value=30)
    addressed_to_current_service = Faker("pybool")
    assigned_to_current_user = Faker("pybool")

    class Meta:
        model = WorkItemTemplate
