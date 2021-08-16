from caluma.caluma_form import models as form_models
from django.conf import settings
from rest_framework import serializers

from camac.core.models import WorkflowEntry
from camac.user.models import Location


class GwrLookupField(serializers.Field):
    def __init__(self, *args, complex=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.complex = complex

    def get_attribute(self, instance):
        if self.complex:
            return {
                key: self.parent.resolve(value) for key, value in self.complex.items()
            }

        return self.parent.resolve(self.field_name)

    def to_representation(self, value):
        return value


class GwrSerializer(serializers.Serializer):
    client = GwrLookupField()
    officialConstructionProjectFileNo = GwrLookupField()
    constructionProjectDescription = GwrLookupField()
    constructionLocalisation = GwrLookupField(
        complex={"municipalityName": "constructionLocalisation_municipalityName"}
    )
    typeOfConstructionProject = GwrLookupField()
    typeOfConstruction = GwrLookupField()
    totalCostsOfProject = GwrLookupField()
    realestateIdentification = GwrLookupField(
        complex={
            "EGRID": "realestateIdentification_EGRID",
            "number": "realestateIdentification_number",
        }
    )
    projectAnnouncementDate = GwrLookupField()

    def resolve(self, lookup_key):
        config = settings.APPLICATION["GWR_DATA"].get(lookup_key)
        if config:
            resolver, *args = config
            return getattr(self, resolver)(*args)

    def answer(self, lookup, *args):
        if not lookup:
            return None  # pragma: no cover
        queryset = self.instance.document.answers

        try:
            if type(lookup) == list:
                value = queryset.filter(question__slug__in=lookup).first().value
            else:
                parts = lookup.split(".")
                if len(parts) > 1:
                    queryset = form_models.Answer.objects.filter(
                        document=queryset.filter(question__slug=parts[0])
                        .first()
                        .documents.first()
                    )
                    value = queryset.filter(question__slug=parts[1]).first().value
                else:
                    value = queryset.filter(question__slug=parts[0]).first().value

            value = value[0] if isinstance(value, list) else value
            mapping = args[0] if len(args) > 0 else None
            return mapping.get(value) if mapping else value
        except AttributeError:
            return None

    def location(self, lookup):
        value = self.answer(lookup)
        if value:
            return Location.objects.get(pk=value).name
        return None  # pragma: no cover

    def case_meta(self, lookup):
        return self.instance.meta.get(lookup)

    def submit_date_from_task(self, lookup):
        return self.instance.work_items.get(task_id=lookup).closed_at

    def submit_date_from_workflow_entry(self, workflow_item_ids):
        entry = WorkflowEntry.objects.filter(
            instance_id=self.instance.instance.pk,
            workflow_item_id__in=workflow_item_ids,
        ).first()
        return entry.workflow_date.strftime("%Y-%m-%d") if entry else None

    def applicant(self, lookup, options):
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
                document=self.instance.document.answers.get(
                    question__slug=lookup
                ).documents.first()
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
