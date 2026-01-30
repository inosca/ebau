import uuid
from collections import namedtuple

import pytest
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_form.factories import QuestionFactory
from django.core.cache import cache

from camac.tests.data import so_personal_row_factory
from camac.tests.utils import Utils

from ..extensions.countries import COUNTRIES
from ..extensions.data_sources import (
    Attachments,
    Authorities,
    Buildings,
    Countries,
    GEVERErledigungsart,
    Landowners,
    Locations,
    Mitberichtsverfahren,
    Municipalities,
    PreliminaryClarificationTargets,
    Sanctions,
    Services,
    ServicesForFinalReport,
)


@pytest.mark.parametrize(
    "role,expected_count", [("Portal User", 1), ("Some internal role", 2)]
)
def test_locations(db, role, location_factory, expected_count):
    User = namedtuple("OIDCUser", "camac_role")
    user = User(camac_role=role)

    location_factory(name="Foo", zip=123)
    location_factory(name="Foo", zip=None)

    data = Locations().get_data(user, None, None)
    assert len(data) == expected_count


@pytest.mark.parametrize(
    "role,expected_count",
    [("Koordinationsstelle Baugesuche BG", 4), ("Something else", 0)],
)
def test_mitberichtsverfahren(db, role, location_factory, expected_count):
    User = namedtuple("OIDCUser", "camac_role")
    user = User(camac_role=role)

    location_factory(name="Foo", zip=123)
    location_factory(name="Foo", zip=None)

    data = Mitberichtsverfahren().get_data(user, None, None)
    assert len(data) == expected_count


@pytest.mark.parametrize(
    "test_class,expected,is_rsta",
    [
        (Authorities, [[1, "Baukommission Altdorf"]], False),
        (Municipalities, [[1, {"de": "Bern", "fr": "Berne", "it": "Bern"}]], False),
        (
            Municipalities,
            [
                [
                    2,
                    {
                        "de": "Biel (nicht aktiviert)",
                        "fr": "Bienne (non activé)",
                        "it": "Biel (nicht aktiviert)",
                    },
                ]
            ],
            True,
        ),
        (
            Services,
            [
                ["-1", {"de": "Andere", "fr": "Autres", "it": "altri"}],
                [
                    "1",
                    {
                        "de": "Gemeinde Bern",
                        "fr": "Municipalité Berne",
                        "it": "Gemeinde Bern",
                    },
                ],
                ["3", {"de": "service3", "fr": "service3", "it": "service3"}],
                ["4", {"de": "service4", "fr": "service4", "it": "service4"}],
            ],
            False,
        ),
        (
            Countries,
            list(COUNTRIES.keys()),
            False,
        ),
    ],
)
def test_data_sources(
    db,
    multilang,
    service_factory,
    service_t_factory,
    service_group_factory,
    test_class,
    expected,
    is_rsta,
    authority_factory,
):
    if is_rsta:
        service1 = service_factory(
            pk=1,
            trans__name="service1",
            trans__language="de",
            disabled=False,
            service_group__name="district",
        )
    else:
        service1 = service_factory(
            pk=1,
            trans__name="Leitbehörde Bern",
            trans__language="de",
            disabled=False,
            service_group__name="municipality",
        )
        service_t_factory(
            service=service1, name="Autorité directrice Berne", language="fr"
        )
        authority_factory(pk=1, name="Baukommission Altdorf")

    service2 = service_factory(
        pk=2,
        trans__name="Leitbehörde Biel",
        trans__language="de",
        disabled=True,
        service_group__name="municipality",
    )
    service_t_factory(
        service=service2, name="Autorité directrice Bienne", language="fr"
    )

    service_factory(
        pk=3,
        trans__name="service3",
        trans__language="de",
        disabled=False,
        service_group__name="district",
    )

    service_factory(
        pk=4,
        trans__name="service4",
        trans__language="de",
        disabled=False,
        service_group__name="service",
    )
    # make sure that "light" municipalities (Kt. AG) are not considered
    service_factory(pk=5, service_group__name="municipality-light")

    User = namedtuple("OIDCUser", "group")
    user = User(group=service1.pk)

    data = test_class().get_data(user, None, None)

    assert data == expected


@pytest.mark.parametrize("document_backend", ["camac-ng", "alexandria"])
@pytest.mark.parametrize(
    "has_instance,has_attachment_section,expected_count",
    [(False, False, 0), (True, False, 0), (False, True, 0), (True, True, 3)],
)
def test_attachments(
    db,
    alexandria_category_factory,
    alexandria_document_factory,
    application_settings,
    attachment_attachment_section_factory,
    attachment_section_factory,
    caluma_admin_user,
    document_backend,
    expected_count,
    has_attachment_section,
    has_instance,
    instance_factory,
):
    application_settings["DOCUMENT_BACKEND"] = document_backend

    question = QuestionFactory()

    if document_backend == "camac-ng":
        section1 = attachment_section_factory()
        section2 = attachment_section_factory()
    else:
        section1 = alexandria_category_factory()
        section2 = alexandria_category_factory()

    instance1 = instance_factory()
    instance2 = instance_factory()

    if document_backend == "camac-ng":
        # attachments in section 1
        attachment_attachment_section_factory.create_batch(
            3, attachmentsection=section1, attachment__instance=instance1
        )
        attachment_attachment_section_factory.create_batch(
            2, attachmentsection=section1, attachment__instance=instance2
        )

        # attachments in section 2
        attachment_attachment_section_factory.create_batch(
            1, attachmentsection=section2, attachment__instance=instance1
        )
        attachment_attachment_section_factory.create_batch(
            2, attachmentsection=section2, attachment__instance=instance2
        )
    else:
        # documents in category 1
        alexandria_document_factory.create_batch(
            3, category=section1, metainfo={"camac-instance-id": instance1.pk}
        )
        alexandria_document_factory.create_batch(
            2, category=section1, metainfo={"camac-instance-id": instance2.pk}
        )

        # documents in category 2
        alexandria_document_factory.create_batch(
            1, category=section2, metainfo={"camac-instance-id": instance1.pk}
        )
        alexandria_document_factory.create_batch(
            2, category=section2, metainfo={"camac-instance-id": instance2.pk}
        )

    if has_attachment_section:
        if document_backend == "camac-ng":
            question.meta["attachmentSection"] = section1.pk
        else:
            question.meta["alexandriaCategory"] = section1.pk
        question.save()

    if has_instance:
        context = {"instanceId": instance1.pk}
    else:
        context = {}

    cache.clear()

    data = Attachments().get_data(caluma_admin_user, question, context)

    assert len(data) == expected_count


def test_landowners_be(
    db,
    caluma_admin_user,
    be_instance,
    utils: Utils,
    be_master_data_settings,
    master_data_is_visible_mock,
):
    question = QuestionFactory(
        slug="personalien-grundeigentumerin",
        type=caluma_form_models.Question.TYPE_TABLE,
    )

    utils.add_table_answer(
        be_instance.case.document,
        question,
        [
            {
                "juristische-person-grundeigentuemerin": "juristische-person-grundeigentuemerin-nein",
                "vorname-grundeigentuemerin": "Foo",
                "name-grundeigentuemerin": "Bar",
            },
            {
                "juristische-person-grundeigentuemerin": "juristische-person-grundeigentuemerin-ja",
                "name-juristische-person-grundeigentuemerin": "Foobar AG",
            },
        ],
    )

    context = {"instanceId": be_instance.pk}
    data = Landowners().get_data(caluma_admin_user, question, context)

    names = [item[1] for item in data]

    assert len(data) == 2
    assert "Foobar AG" in names
    assert "Foo Bar" in names


def test_landowners_so(
    db,
    caluma_admin_user,
    so_instance,
    utils: Utils,
    so_master_data_settings,
    master_data_is_visible_mock,
    snapshot,
    settings,
):
    settings.APPLICATION_NAME = "kt_so"

    utils.add_table_answer(
        so_instance.case.document,
        "bauherrin",
        [so_personal_row_factory(True), so_personal_row_factory(False)],
    )
    utils.add_table_answer(
        so_instance.case.document,
        "grundeigentuemerin",
        [so_personal_row_factory(True), so_personal_row_factory(False)],
    )

    data = Landowners().get_data(
        caluma_admin_user, None, {"instanceId": so_instance.pk}
    )

    names = [item[1] for item in data]

    assert len(names) == 4
    assert names == snapshot


def test_landowners_dynamic_on_copy(
    db,
    caluma_document_factory,
    caluma_question_factory,
    caluma_dynamic_option_factory,
    utils: Utils,
    settings,
):
    settings.DATA_SOURCE_CLASSES = ["camac.caluma.extensions.data_sources.Landowners"]

    # test default fallback values
    data_source = Landowners()
    assert (None, None) == data_source.on_copy(None, None, (None, None))
    assert (None, None) == data_source.on_copy(None, None, ("invalid-uuid", None))

    main_document = caluma_document_factory()
    test_document_a = caluma_document_factory()
    test_document_b = caluma_document_factory()
    test_document_c = caluma_document_factory()

    dynamic_choice_question = caluma_question_factory(
        slug="dynamic-reference-test",
        type=caluma_form_models.Question.TYPE_DYNAMIC_MULTIPLE_CHOICE,
    )
    dynamic_choice_question.data_source = "Landowners"
    dynamic_choice_question.save()

    dynamic_answer = utils.add_answer(
        document=main_document,
        question=dynamic_choice_question,
        value=[
            str(test_document_a.pk),
            str(test_document_b.pk),
            str(test_document_c.pk),
        ],
        label="MFH 1, MFH 2",
    )
    dynamic_option1 = caluma_dynamic_option_factory(
        document=main_document,
        question=dynamic_choice_question,
        slug=str(test_document_a.pk),
        label="MFH 1",
    )
    dynamic_option2 = caluma_dynamic_option_factory(
        document=main_document,
        question=dynamic_choice_question,
        slug=str(test_document_b.pk),
        label="MFH 2",
    )
    caluma_dynamic_option_factory(
        document=main_document,
        question=dynamic_choice_question,
        slug=str(test_document_c.pk),
        label="MFH 3",
    )

    # example docs for a/b to test moving a reference while copying an answer
    # c will be discarded
    referenced_document1 = caluma_document_factory()
    referenced_document1.source = test_document_a
    referenced_document1.save()
    referenced_document2 = caluma_document_factory()
    referenced_document2.source = test_document_b
    referenced_document2.save()

    # copy the document with answers
    new_document = main_document.copy()
    new_answer = caluma_form_models.Answer.objects.get(
        question=dynamic_choice_question, document=new_document
    )
    new_dynamic_options = caluma_form_models.DynamicOption.objects.filter(
        question=dynamic_choice_question, document=new_document
    )

    # c is discarded, only a and b are copied
    assert new_dynamic_options.count() == 2

    # check that the new anser and dynamic option are linked to the referenced document
    assert str(dynamic_answer.pk) != str(new_answer.pk)
    assert str(dynamic_option1.pk) != str(new_dynamic_options.first().pk)
    assert str(dynamic_option2.pk) != str(new_dynamic_options.last().pk)
    assert new_answer.value == [
        str(referenced_document1.pk),
        str(referenced_document2.pk),
    ]
    assert set([option.slug for option in new_dynamic_options]) == {
        str(referenced_document1.pk),
        str(referenced_document2.pk),
    }


def test_municipalities_so(db, service_factory, service_t_factory):
    service = service_factory(service_group__name="municipality")
    service_t_factory(service=service, name="Gemeinde Solothurn")

    User = namedtuple("OIDCUser", "group")
    user = User(group=service.pk)

    data = Municipalities().get_data(user, None, None)

    assert len(data) == 1
    assert data[0][0] == service.pk
    assert data[0][1]["de"] == "Solothurn"


@pytest.mark.parametrize(
    "role,expected", [("applicant", ["Full"]), ("municipality", ["Full", "Light"])]
)
def test_municipalities_ag(
    db, role, service_factory, service_t_factory, set_application_ag, expected
):
    service = service_factory(service_group__name="municipality")
    service_light = service_factory(service_group__name="municipality-light")
    service_t_factory(service=service, name="Gemeinde Full")
    service_t_factory(service=service_light, name="Gemeinde Light")

    User = namedtuple("OIDCUser", ["group", "camac_role"])
    user = User(group=service.pk, camac_role=role)

    data = Municipalities().get_data(user, None, None)

    assert set([r[1]["de"] for r in data]) == set(expected)


def test_preliminary_clarfication_targets(db, caluma_admin_user, service_factory):
    service_factory(
        trans__name="AfU",
        trans__language="de",
        service_group__name="service-cantonal",
    )
    service_factory(
        trans__name="Procap",
        trans__language="de",
        service_group__name="service-extra-cantonal",
    )
    service_factory(
        trans__name="ARP",
        trans__language="de",
        service_group__name="service-bab",
    )

    data = PreliminaryClarificationTargets().get_data(caluma_admin_user, None, None)

    assert data[0][1]["de"] == "Andere"
    assert data[1][1]["de"] == "Örtliche Baubehörde"
    assert data[2][1]["de"] == "AfU"
    assert data[3][1]["de"] == "ARP"
    assert data[4][1]["de"] == "Procap"


def test_buildings(
    db, caluma_admin_user, caluma_question_factory, so_instance, utils: Utils
):
    question = caluma_question_factory(
        slug="gebaeude",
        type=caluma_form_models.Question.TYPE_TABLE,
    )

    utils.add_table_answer(
        so_instance.case.document,
        question,
        [
            {"gebaeude-bezeichnung": "MFH 1"},
            {"gebaeude-bezeichnung": "MFH 2"},
            {"gebaeude-bezeichnung": "EFH 1"},
        ],
    )

    data = Buildings().get_data(
        caluma_admin_user,
        question,
        {"instanceId": so_instance.pk},
    )

    names = set([item[1] for item in data])

    assert len(data) == 3
    assert names == {"MFH 1", "MFH 2", "EFH 1"}


def test_buildings_dynamic_on_copy(
    db,
    caluma_document_factory,
    caluma_question_factory,
    caluma_dynamic_option_factory,
    utils: Utils,
    settings,
):
    settings.DATA_SOURCE_CLASSES = ["camac.caluma.extensions.data_sources.Buildings"]

    # test default fallback values
    data_source = Buildings()
    assert (None, None) == data_source.on_copy(None, None, (None, None))
    assert (None, None) == data_source.on_copy(None, None, ("invalid-uuid", None))

    main_document = caluma_document_factory()
    test_document = caluma_document_factory()
    dynamic_choice_question = caluma_question_factory(
        slug="dynamic-reference-test",
        type=caluma_form_models.Question.TYPE_DYNAMIC_CHOICE,
    )
    dynamic_choice_question.data_source = "Buildings"
    dynamic_choice_question.save()

    dynamic_answer = utils.add_answer(
        document=main_document,
        question=dynamic_choice_question,
        value=str(test_document.pk),
        label="MFH 1",
    )
    dynamic_option = caluma_dynamic_option_factory(
        document=main_document,
        question=dynamic_choice_question,
        slug=str(test_document.pk),
        label="MFH 1",
    )

    # example doc to test moving a reference while copying an answer
    referenced_document = caluma_document_factory()
    referenced_document.source = test_document
    referenced_document.save()

    # copy the document with answers
    new_document = main_document.copy()
    new_answer = caluma_form_models.Answer.objects.get(
        question=dynamic_choice_question, document=new_document
    )
    new_dynamic_option = caluma_form_models.DynamicOption.objects.get(
        question=dynamic_choice_question, document=new_document
    )

    # check that the new anser and dynamic option are linked to the referenced document
    assert str(dynamic_answer.pk) != str(new_answer.pk)
    assert str(dynamic_option.pk) != str(new_dynamic_option.pk)
    assert new_answer.value == str(referenced_document.pk)
    assert new_dynamic_option.slug == str(referenced_document.pk)


def test_services_for_final_report(
    db,
    caluma_admin_user,
    caluma_question_factory,
    utils: Utils,
    ur_instance,
    caluma_work_item_factory,
    service_factory,
    ur_distribution_settings,
):
    services_that_wants_to_be_invited = service_factory()

    distribution = caluma_work_item_factory(
        task_id="distribution",
        case=ur_instance.case,
        child_case__family=ur_instance.case,
    )

    inquiry_1 = caluma_work_item_factory(
        task_id="inquiry",
        case=distribution.child_case,
        addressed_groups=[str(services_that_wants_to_be_invited.pk)],
    )

    utils.add_answer(
        inquiry_1.child_case.document,
        "inquiry-answer-invite-service",
        "inquiry-answer-invite-service-yes",
    )

    data = ServicesForFinalReport().get_data(
        caluma_admin_user,
        caluma_question_factory(),
        {"instanceId": ur_instance.pk},
    )

    service_names = set([service[1] for service in data])

    assert len(data) == 1
    assert service_names == {services_that_wants_to_be_invited.name}


@pytest.mark.parametrize(
    "sanction_steps, question_step, expected_count",
    [
        # Test 'regular' sanction steps, with some already controlled:
        ([("b", True), ("b", False), ("b", False), ("e", False)], "b", 2),
        ([("b", True), ("b", False), ("b", False), ("e", False)], "r", 0),
        ([("b", True), ("b", False), ("b", False), ("e", False)], "e", 1),
        ([("b", True), ("b", False), ("b", False), ("e", False)], None, 0),
        # Variable sanctions should not show up anywhere:
        ([("v", False)], "b", 0),
        ([("v", False)], "r", 0),
        ([("v", False)], "e", 0),
        ([("v", False)], None, 0),
    ],
)
def test_sanctions(
    db,
    instance_factory,
    caluma_question_factory,
    new_sanction_factory,
    sanction_steps,
    question_step,
    expected_count,
):
    instance = instance_factory()
    step_map = {
        "b": "baufreigabe",
        "r": "realisierung",
        "e": "endabnahme",
        "v": "variabel",
    }

    for sanction_step in sanction_steps:
        new_sanction_factory(
            instance=instance,
            control_step=step_map[sanction_step[0]],
            controlled=sanction_step[1],
        )

    question = caluma_question_factory(
        **(
            {"meta": {"sanction_step": step_map[question_step]}}
            if question_step
            else {}
        ),
    )
    context = {"instanceId": instance.pk}

    data = Sanctions().get_data(instance.user, question, context)
    if expected_count == 0:
        assert len(data) == 1 and data[0][0] is None
    else:
        assert len(data) == expected_count


@pytest.mark.vcr(match_on=["method", "path", "query"])
@pytest.mark.django_db(reset_sequences=True)
def test_gever_erledigungsart_datasource(be_gever_settings):
    ds = GEVERErledigungsart()

    # No need to make up parameters, the data source doesn't actually
    # use them, so in this case, it's fine
    res = ds.get_data(None, None, None)

    assert len(res)
    for id, label in res:
        assert uuid.UUID(id)
        assert label
