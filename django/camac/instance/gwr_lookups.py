from caluma.caluma_form import models as form_models
from django.conf import settings

from camac.core.models import WorkflowEntry
from camac.user.models import Location


def resolve(lookup_key, case):
    config = settings.APPLICATION["GWR_DATA"].get(lookup_key)
    if config:
        resolver = config[0]
        return globals()[f"get_{resolver}"](*config[1:], case=case)

    return None  # pragma: no cover


def get_answer(lookup, *args, case):
    if not lookup:
        return None  # pragma: no cover
    queryset = case.document.answers

    try:
        if type(lookup) == list:
            value = queryset.filter(question__slug__in=lookup).first().value
        else:
            parts = lookup.split(".")
            if len(parts) > 1:
                queryset = form_models.Answer.objects.filter(
                    document=queryset.get(question__slug=parts[0]).documents.first()
                )
                value = queryset.filter(question__slug=parts[1]).first().value
            else:
                value = queryset.filter(question__slug=parts[0]).first().value

        value = value[0] if isinstance(value, list) else value
        mapping = args[0] if len(args) > 0 else None
        return mapping.get(value) if mapping else value
    except AttributeError:
        return None


def get_location(lookup, case):
    value = get_answer(lookup, case=case)
    if value:
        return Location.objects.get(pk=value).name
    return None  # pragma: no cover


def get_case_meta(lookup, case):
    return case.meta.get(lookup)


def get_submit_date_from_task(lookup, case):
    return case.work_items.get(task_id=lookup).closed_at


def get_submit_date_from_workflow_entry(workflow_item_ids, case):
    entry = WorkflowEntry.objects.filter(
        instance_id=case.instance.pk,
        workflow_item_id__in=workflow_item_ids,
    ).first()
    return entry.workflow_date.strftime("%Y-%m-%d") if entry else None


def get_client(lookup, options, case):
    # closure for shorthand calls
    def find_answer(lookup_key):
        config = options.get(lookup_key)
        if not config:
            return None

        mapping = None
        if type(config) is tuple:
            slug, mapping = config
        else:
            slug = config  # pragma: no cover

        answer = client.filter(question__slug=slug).first()

        value = answer.value if answer else None
        return mapping.get(value) if mapping else value

    try:
        client = form_models.Answer.objects.filter(
            document=case.document.answers.get(question__slug=lookup).documents.first()
        )

        return {
            "address": {
                "town": find_answer("address_town"),
                "swissZipCode": find_answer("address_swissZipCode"),
                "street": find_answer("address_street"),
                "houseNumber": find_answer("address_houseNumber"),
                "country": find_answer("address_country"),
            },
            "identification": {
                "personIdentification": {
                    "officialName": find_answer(
                        "identification_personIdentification_officialName"
                    ),
                    "firstName": find_answer(
                        "identification_personIdentification_firstName"
                    ),
                },
                "isOrganisation": find_answer("identification_isOrganisation"),
                "organisationIdentification": {
                    "organisationName": find_answer(
                        "identification_organisationIdentification_organisationName"
                    )
                },
            },
        }
    except form_models.Answer.DoesNotExist:  # pragma: no cover
        return None
