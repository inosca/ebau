from caluma.caluma_form import models as form_models
from django.conf import settings

from camac.core.models import WorkflowEntry
from camac.user.models import Location


def resolve(lookup_key, case):
    config = settings.APPLICATION["GWR"].get("ANSWER_SLUGS", {}).get(lookup_key)
    if config:
        resolver = config[0]
        return globals()[f"get_{resolver}"](*config[1:], case=case)

    return None


def get_answer(lookup, *args, case):
    queryset = case.document.answers
    if not lookup:
        return None
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


def get_location(lookup, case):
    value = get_answer(lookup, case=case)
    if not value:
        return None
    return Location.objects.get(pk=value).name


def get_case_meta(lookup, case):
    return case.meta.get(lookup)


def get_submit_date_from_task(lookup, case):
    return case.work_items.get(task_id="submit").closed_at


def get_submit_date_from_workflow(workflow_item_ids, case):
    return WorkflowEntry.objects.get(
        instance_id=case.meta["camac-instance-id"],
        workflow_item_id__in=workflow_item_ids,
    ).workflow_date.strftime("%Y-%m-%d")


def get_client(lookup, options, case):
    try:

        def find_answer(lookup_key):
            config = options[lookup_key]

            mapping = None
            if type(config) is tuple:
                slug, mapping = config
            else:
                slug = config

            answer = client.filter(question__slug=slug).first()

            value = answer.value if answer else None
            return mapping.get(value) if mapping else value

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
