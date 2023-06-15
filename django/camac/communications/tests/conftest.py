import pytest


@pytest.fixture
def topic_with_admin_involved(admin_user, communications_topic, role):
    if role.name == "Applicant":
        entity = "APPLICANT"
    else:
        entity = admin_user.get_default_group().service_id

    communications_topic.involved_entities.append(entity)
    communications_topic.save()
    return communications_topic
