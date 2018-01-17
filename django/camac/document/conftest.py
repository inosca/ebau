import logging

import pytest
from pytest_factoryboy import register

from . import factories

register(factories.AttachmentFactory)
register(factories.AttachmentSectionFactory)
register(factories.AttachmentSectionRoleAclFactory)
register(factories.AttachmentSectionGroupAclFactory)


sorl_thumbnail_logger = logging.getLogger('sorl.thumbnail')
sorl_thumbnail_logger.setLevel(logging.INFO)


@pytest.fixture
def attachment_section(attachment_section_factory,
                       attachment_section_group_acl_factory, admin_user):
    attachment_section = attachment_section_factory()
    attachment_section_group_acl_factory(
        attachment_section=attachment_section,
        group=admin_user.groups.first()
    )
    return attachment_section


@pytest.fixture
def attachment_section_noacl(attachment_section_factory):
    return attachment_section_factory()


@pytest.fixture
def attachment__attachment_section(attachment_section):
    return attachment_section
