from functools import partial

import pyexcel
import pytest
from dateutil.relativedelta import relativedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from camac.billing.export.views import BillingV2EntryExportView
from camac.billing.models import BillingV2Entry


@pytest.mark.freeze_time("2023-11-06")
@pytest.mark.parametrize(
    "parcels",
    [
        # List of number, X, Y coord
        [  # No parcels in dossier
        ],
        [
            # Single-parcel dossier
            (134, 2222, 3333)
        ],
        [
            # Multi-parcel dossier
            (231, 1111, 2222),
            (232, 4444, 5555),
            (233, 6666, 7777),
        ],
    ],
)
@pytest.mark.parametrize(
    "role__name,billing_params,entries_count, expected_count, filter_date_added",
    [
        ("Municipality", {"calculation": BillingV2Entry.CALCULATION_FLAT}, 3, 3, False),
        (
            "Municipality",
            {"calculation": BillingV2Entry.CALCULATION_PERCENTAGE},
            3,
            3,
            False,
        ),
        (
            "Municipality",
            {
                "calculation": BillingV2Entry.CALCULATION_HOURLY,
                "tax_mode": BillingV2Entry.TAX_MODE_INCLUSIVE,
            },
            3,
            3,
            False,
        ),
        (
            "Municipality",
            {
                "calculation": BillingV2Entry.CALCULATION_FLAT,
                "tax_mode": BillingV2Entry.TAX_MODE_EXEMPT,
            },
            3,
            3,
            False,
        ),
        ("Applicant", {"calculation": BillingV2Entry.CALCULATION_FLAT}, 3, 0, False),
        ("Support", {"calculation": BillingV2Entry.CALCULATION_FLAT}, 3, 3, False),
        ("Service", {"calculation": BillingV2Entry.CALCULATION_FLAT}, 3, 3, False),
        ("Service", {"calculation": BillingV2Entry.CALCULATION_FLAT}, 3, 1, True),
    ],
)
def test_billing_export(
    admin_client,
    billing_v2_entry_factory,
    snapshot,
    instance_with_document_for_billing,
    billing_params,
    entries_count,
    expected_count,
    filter_date_added,
    parcels,
):
    instance, parcel_ans = instance_with_document_for_billing

    billing_v2_entry_factory.create_batch(
        entries_count, **{**billing_params, "instance": instance}
    )
    query_params = {"instance": instance.pk}

    for idx, (parcel_nr, coord_x, coord_y) in enumerate(parcels):
        row_doc = parcel_ans.documents.create(
            through_defaults={"sort": idx},
            form=parcel_ans.question.row_form,
            family_id=parcel_ans.document_id,
        )
        row_doc.answers.create(question_id="parzellennummer", value=parcel_nr)
        row_doc.answers.create(question_id="lagekoordinaten-ost", value=coord_x)
        row_doc.answers.create(question_id="lagekoordinaten-nord", value=coord_y)

    if filter_date_added:
        date_added = timezone.now()  # freezed
        date_later = (date_added + relativedelta(months=1)).date()
        entry = BillingV2Entry.objects.first()
        entry.date_added = date_later
        entry.save()
        query_params = {**query_params, "filter[date_added_after]": date_later}

    url = reverse("billing-export")
    response = admin_client.get(url, query_params)

    assert response.status_code == status.HTTP_200_OK
    book = pyexcel.get_book(file_content=response.content, file_type="xlsx")
    sheet = book.get_dict()["pyexcel sheet"]
    assert len(sheet) - 1 == expected_count  # substract header row
    if len(sheet) > 1:
        data = sheet[1]
        data.pop(7)  # remove ebau-Nr as it is not stable

        snapshot.assert_match(data)


@pytest.fixture
def instance_with_document_for_billing(
    instance,
    question_factory,
    answer_factory,
    form_factory,
    case_factory,
    form_question_factory,
):
    instance.case = case_factory()
    instance.save()
    parcel_table = question_factory(type="table")
    parcel_field = partial(
        form_question_factory, form=parcel_table.row_form, question__type="integer"
    )
    parcel_field(question__slug="parzellennummer")
    parcel_field(question__slug="lagekoordinaten-ost")
    parcel_field(question__slug="lagekoordinaten-nord")
    instance.case.document.form.questions.add(parcel_table)

    parcel_ans = answer_factory(document=instance.case.document, question=parcel_table)
    return instance, parcel_ans


@pytest.mark.parametrize(
    "role__name,method,has_access,expected_count",
    [
        ("Municipality", "get_queryset_for_municipality", True, 1),
        ("Service", "get_queryset_for_service", True, 1),
        ("Applicant", "_get_queryset_for_applicant", True, 0),
        ("Public", "get_queryset_for_public", True, 0),
        ("Municipality", "get_queryset_for_municipality", False, 0),
        ("Service", "get_queryset_for_service", False, 0),
        ("Applicant", "_get_queryset_for_applicant", False, 0),
        ("Public", "get_queryset_for_public", False, 0),
    ],
)
def test_billing_entry_export_visibilities(
    db,
    admin_client,
    instance,
    mocker,
    billing_v2_entry_factory,
    role,
    group,
    method,
    expected_count,
    has_access,
):
    is_public = role.name == "Public"
    mocker.patch(
        "camac.user.permissions.get_group", return_value=None if is_public else group
    )
    billingv2entry = billing_v2_entry_factory(instance=instance)
    mocker.patch(
        f"camac.instance.mixins.InstanceQuerysetMixin.{method}",
        return_value=BillingV2Entry.objects.filter(pk=billingv2entry.pk)
        if has_access
        else BillingV2Entry.objects.none(),
    )

    view = BillingV2EntryExportView()
    assert view.get_queryset().count() == expected_count
    if expected_count:
        assert billingv2entry in view.get_queryset()
