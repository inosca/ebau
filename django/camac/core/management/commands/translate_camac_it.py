import csv

from alexandria.core.models import Category
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import models as caluma_workflow_models
from django.core.management.base import BaseCommand

from camac.core.models import InstanceResource, InstanceResourceT, Resource, ResourceT
from camac.notification.models import NotificationTemplate, NotificationTemplateT
from camac.permissions.models import AccessLevel
from camac.user.models import Role, RoleT, ServiceGroup, ServiceGroupT

models = [
    {
        "type": "camac",
        "model": Resource,
        "translation_model": ResourceT,
        "translation_model_name": "ResourceT",
        "filename": "Resource",
        "columns": ["name"],
    },
    {
        "type": "camac",
        "model": InstanceResource,
        "translation_model": InstanceResourceT,
        "translation_model_name": "InstanceResourceT",
        "filename": "InstanceResource",
        "columns": ["name"],
    },
    {
        "type": "camac",
        "model": NotificationTemplate,
        "translation_model": NotificationTemplateT,
        "translation_model_name": "NotificationTemplateT",
        "filename": "NotificationTemplate",
        "columns": ["purpose", "subject", "body"],
    },
    {
        "type": "camac",
        "model": Role,
        "translation_model": RoleT,
        "translation_model_name": "RoleT",
        "filename": "Role",
        "columns": ["name", "group_prefix"],
    },
    {
        "type": "camac",
        "model": ServiceGroup,
        "translation_model": ServiceGroupT,
        "translation_model_name": "ServiceGroupT",
        "filename": "ServiceGroup",
        "columns": ["name"],
    },
    {
        "type": "caluma",
        "model": caluma_form_models.Question,
        "filename": "Question",
        "columns": ["label", "info_text", "placeholder", "static_content", "hint_text"],
    },
    {
        "type": "caluma",
        "model": caluma_form_models.Option,
        "filename": "Option",
        "columns": ["label"],
    },
    {
        "type": "caluma",
        "model": caluma_form_models.Form,
        "filename": "Form",
        "columns": ["name", "description"],
    },
    {
        "type": "caluma",
        "model": caluma_workflow_models.Task,
        "filename": "Task",
        "columns": ["name", "description"],
    },
    {
        "type": "caluma",
        "model": caluma_workflow_models.Workflow,
        "filename": "Workflow",
        "columns": ["name"],
    },
    {
        "type": "caluma",
        "model": Category,
        "filename": "Category",
        "columns": ["name", "description"],
    },
    {
        "type": "caluma",
        "model": AccessLevel,
        "filename": "AccessLevel",
        "columns": ["name"],
    },
]


def _load_csv(config):
    data = {}
    for column in config["columns"]:
        file = f"camac/core/translation_files/{config['filename']}_{column}_it.csv"

        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            line_count = 0
            for item in csv_reader:
                if line_count == 0:
                    pass
                else:
                    pk = item[0]
                    translation = item[2]

                    if pk in data:
                        data[pk][column] = translation

                    else:
                        data[pk] = {column: translation} if translation else {}
                line_count += 1
    return data


def _upload_data(config, data):
    for pk, row in data.items():
        if config["type"] == "camac":
            if config["translation_model_name"] == "NotificationTemplateT":
                _, created = config["translation_model"].objects.update_or_create(
                    template_id=pk,
                    language="it",
                    defaults=row,
                    template_slug_id=config["model"].objects.get(pk=pk).slug,
                )
            else:
                _, created = config["translation_model"].objects.update_or_create(
                    template_id=pk,
                    language="it",
                    defaults=row,
                )
            translation_model_name = config["translation_model_name"]
            if created:
                print(f"{translation_model_name}({pk}) was created: {row}")
        elif config["type"] == "caluma":
            model = config["model"].objects.get(slug=pk)
            for column in config["columns"]:
                getattr(model, column).set("it", row[column])
                model.save()


class Command(BaseCommand):
    def handle(self, *args, **option):
        for config in models:
            data = _load_csv(config)

            _upload_data(config, data)
