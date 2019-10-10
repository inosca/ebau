from django.urls import reverse
from rest_framework import status

from camac.core.models import Answer, Chapter, Question, QuestionT, QuestionType

from .caluma_responses import full_document


def test_application_retrieve_full(
    admin_client,
    ech_instance,
    instance_factory,
    docx_decision_factory,
    requests_mock,
    attachment,
):
    docx_decision_factory(instance=ech_instance.pk)

    i = instance_factory()

    attachment.instance = ech_instance
    attachment.context = {"tags": ["berechnung-kinderspielplaetze-dokument"]}
    attachment.save()

    qtype = QuestionType.objects.create(name="text")
    q = Question.objects.create(question_type=qtype)
    QuestionT.objects.create(question=q, name="eBau-Nummer", language="de")
    chapter = Chapter.objects.create()
    Answer.objects.create(
        instance=i, question=q, answer="2019-23", item=1, chapter=chapter
    )
    Answer.objects.create(
        instance=ech_instance, question=q, answer="2019-23", item=1, chapter=chapter
    )

    url = reverse("application", args=[ech_instance.pk])

    requests_mock.post("http://caluma:8000/graphql/", json=full_document)

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_applications_list(admin_client, admin_user, instance, instance_factory):
    i = instance_factory(user=admin_user)
    url = reverse("applications")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(i.instance_id)
