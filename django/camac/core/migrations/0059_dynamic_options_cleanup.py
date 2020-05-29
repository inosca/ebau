import operator
from functools import reduce

from django.db import migrations
from django.db.models import Q

from camac.user.models import Service


def migrate_dynamic_options(apps, schema_editor):
    numbers = [str(num) for num in range(1, 10)]

    DynamicOption = apps.get_model("caluma_form", "DynamicOption")

    query = reduce(operator.or_, (Q(label__de__contains=number) for number in numbers))

    dynamic_options = DynamicOption.objects.filter(query)

    for option in dynamic_options:
        if option.slug == "-1":
            continue
        service = Service.objects.filter(service_id=int(option.slug)).first()
        if service:
            option.label["de"] = service.get_name()
            option.save()


class Migration(migrations.Migration):

    dependencies = [("core", "0058_auto_20200427_1302")]

    operations = [
        migrations.RunPython(
            migrate_dynamic_options, reverse_code=migrations.RunPython.noop
        )
    ]
