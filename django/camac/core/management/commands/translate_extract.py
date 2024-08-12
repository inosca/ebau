import csv

from alexandria.core.models import Category
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import models as caluma_workflow_models
from django.core.management.base import BaseCommand

from camac.core.models import InstanceResource, MultilingualModel, Resource
from camac.notification.models import NotificationTemplate
from camac.permissions.models import AccessLevel
from camac.user.models import Role, ServiceGroup

MODELS = [
    {
        "model": Resource,
        "columns": ["name"],
    },
    {
        "model": InstanceResource,
        "columns": ["name"],
    },
    {
        "model": NotificationTemplate,
        "columns": ["purpose", "subject", "body"],
    },
    {"model": Role, "columns": ["name", "group_prefix"]},
    {"model": ServiceGroup, "columns": ["name"]},
    {
        "model": caluma_form_models.Question,
        "columns": ["label", "info_text", "placeholder", "static_content", "hint_text"],
    },
    {
        "model": caluma_form_models.Option,
        "columns": ["label"],
    },
    {
        "model": caluma_form_models.Form,
        "columns": ["name", "description"],
    },
    {
        "model": caluma_workflow_models.Task,
        "columns": ["name"],
    },
    {
        "model": caluma_workflow_models.Workflow,
        "columns": ["name"],
    },
    {"model": Category, "columns": ["name", "description"]},
    {"model": AccessLevel, "columns": ["name"]},
]


def _write_translations(model, columns):
    for column in columns:
        with open(
            f"translations/{model.__name__}_{column}.csv", "w+", newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow(["id", f"{column}"])
            for inst in model.objects.all():
                if isinstance(model, MultilingualModel):
                    row = [inst.get_trans_attr(column, "de", fallback=False)]
                else:
                    row = [getattr(getattr(inst, column), "de", None)]

                if "" not in row and None not in row:
                    writer.writerow([inst.pk] + row)


class Command(BaseCommand):
    def handle(self, *args, **option):
        for config in MODELS:
            _write_translations(**config)
