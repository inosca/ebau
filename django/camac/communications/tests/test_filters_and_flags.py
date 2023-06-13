import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture
def some_read_and_some_unread_topics(
    db,
    admin_client,
    be_instance,
    communications_topic_factory,
    communications_message_factory,
):
    main_service = admin_client.user.groups.first()
    users_entity = str(main_service.service.pk) if main_service else "APPLICANT"

    topics_with_all_read = communications_topic_factory.create_batch(
        2, instance=be_instance, involved_entities=[users_entity]
    )
    topics_with_unread = communications_topic_factory.create_batch(
        2, instance=be_instance, involved_entities=[users_entity]
    )

    for topic in topics_with_all_read:
        # some message that has been read
        read = communications_message_factory(topic=topic)
        read.read_by.create(entity=users_entity)
    for topic in topics_with_unread:
        # some unread message, some read
        m1, _ = communications_message_factory.create_batch(2, topic=topic)
        m1.read_by.create(entity=users_entity)

    return topics_with_all_read, topics_with_unread


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_topic_flag_has_unread(
    db, admin_client, be_instance, some_read_and_some_unread_topics
):
    topics_with_all_read, topics_with_unread = some_read_and_some_unread_topics

    resp = admin_client.get(reverse("communications-topic-list"))

    assert resp.status_code == status.HTTP_200_OK

    unread_ids = [str(topic.pk) for topic in topics_with_unread]
    read_ids = [str(topic.pk) for topic in topics_with_all_read]

    received_ids_unread = [
        rec["id"] for rec in resp.json()["data"] if rec["attributes"]["has-unread"]
    ]
    received_ids_read = [
        rec["id"] for rec in resp.json()["data"] if not rec["attributes"]["has-unread"]
    ]

    assert set(received_ids_unread) == set(unread_ids)
    assert set(received_ids_read) == set(read_ids)


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("filter", [True, False])
def test_topic_filter_has_unread(
    db, be_instance, admin_client, some_read_and_some_unread_topics, filter
):
    topics_with_all_read, topics_with_unread = some_read_and_some_unread_topics

    resp = admin_client.get(
        reverse("communications-topic-list"), {"has_unread": str(filter).lower()}
    )
    assert resp.status_code == status.HTTP_200_OK
    received_ids = [rec["id"] for rec in resp.json()["data"]]

    if filter:
        expected_ids = [str(topic.pk) for topic in topics_with_unread]
    else:
        expected_ids = [str(topic.pk) for topic in topics_with_all_read]

    assert set(received_ids) == set(expected_ids)


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "filter, expect_set", [(True, "read"), (False, "unread"), (None, "all")]
)
def test_message_read_flags_and_filter(
    db, admin_client, communications_message_factory, be_instance, filter, expect_set
):
    my_entity = admin_client.user.groups.first().service_id
    unread_messages = communications_message_factory.create_batch(
        2, topic__involved_entities=[my_entity], topic__instance=be_instance
    )
    read_messages = communications_message_factory.create_batch(
        2, topic__involved_entities=[my_entity], topic__instance=be_instance
    )
    all_messages = unread_messages + read_messages

    for msg in read_messages:
        msg.read_by.create(entity=my_entity)
        msg.save()

    expected_sets = {
        "unread": [str(msg.pk) for msg in unread_messages],
        "read": [str(msg.pk) for msg in read_messages],
        "all": [str(msg.pk) for msg in all_messages],
    }

    expected_ids = set(expected_sets[expect_set])

    filter_params = {"is_read": filter} if filter is not None else {}

    resp = admin_client.get(reverse("communications-message-list"), data=filter_params)
    received_ids = set([rec["id"] for rec in resp.json()["data"]])

    assert resp.status_code == status.HTTP_200_OK
    assert received_ids == expected_ids

    if expect_set == "all":
        # just checking if the is_read flags are set properly on all
        # listed messages
        for msg_obj in resp.json()["data"]:
            is_read = msg_obj["attributes"]["read-at"]
            if is_read:
                assert msg_obj["id"] in expected_sets["read"]
            else:
                assert msg_obj["id"] in expected_sets["unread"]
