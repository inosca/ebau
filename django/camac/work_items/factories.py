from factory import Faker, LazyFunction, fuzzy
from factory.django import DjangoModelFactory

from camac.utils import choice_keys
from camac.work_items.models import WorkItemListFilterPreset, WorkItemTemplate


class WorkItemTemplateFactory(DjangoModelFactory):
    name = Faker("word")
    description = Faker("sentence")
    lead_time = Faker("pyint", min_value=1, max_value=30)
    responsibility_rule = fuzzy.FuzzyChoice(
        choice_keys(WorkItemTemplate.ResponsibilityRuleChoices)
    )

    class Meta:
        model = WorkItemTemplate


class WorkItemListFilterPresetFactory(DjangoModelFactory):
    name = Faker("word")
    query_params = LazyFunction(dict)
    prefilter_work_item_templates = True
    prefilter_tasks = False

    class Meta:
        model = WorkItemListFilterPreset
