import os
from datetime import timedelta
from logging import getLogger
from pathlib import Path
from shutil import copy2

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from manabi import ManabiDAVApp
from manabi.auth import ManabiAuthenticator
from manabi.filesystem import CallbackHookConfig, ManabiFileResource, ManabiProvider
from manabi.lock import ManabiDbLockStorage
from manabi.log import HeaderLogger, verbose_logging
from wsgidav.dav_error import HTTP_BAD_REQUEST, DAVError
from wsgidav.dir_browser import WsgiDavDirBrowser
from wsgidav.error_printer import ErrorPrinter
from wsgidav.mw.debug_filter import WsgiDavDebugFilter
from wsgidav.request_resolver import RequestResolver

log = getLogger(__name__)


class LoggedManabiFileResource(ManabiFileResource):
    def begin_write(self, *, content_type=None):
        if settings.LOG_FILE_WRITE_SIZES:
            _, attachment_id = self._token.payload
            log.info(
                f"-------------------- START DAV WRITE ATTACHMENT_ID {attachment_id} --------------------"
            )
            log.info(
                f"begin_write -- ATTACHMENT_ID {attachment_id}"
                f"\n\tcontent_length={self.environ['CONTENT_LENGTH']} (file size from the request)"
            )
        if int(self.environ["CONTENT_LENGTH"]) == 0:  # pragma: no cover
            raise DAVError(HTTP_BAD_REQUEST)
        return super().begin_write(content_type=content_type)


class LoggedManabiProvider(ManabiProvider):
    def get_file_resource(self, path, environ, fp):
        if Path(fp).exists():
            return LoggedManabiFileResource(
                path,
                environ,
                fp,
                cb_hook_config=self._cb_hook_config,
            )


def get_dav():
    key = settings.MANABI_SHARED_KEY
    if not key:  # pragma: no cover
        raise RuntimeError("MANABI_SHARED_KEY is missing")
    default_db = settings.DATABASES["default"]
    db_name = default_db["NAME"]
    db_user = default_db["USER"]
    db_host = default_db["HOST"]
    db_port = default_db["PORT"]
    db_pass = default_db["PASSWORD"]
    postgres_dsn = f"dbname={db_name} user={db_user} host={db_host} port={db_port} password={db_pass}"
    refresh = settings.MANABI_TOKEN_REFRESH_TIMEOUT
    if settings.MANABI_DEBUG:
        verbose_logging()
    cb_hook_config = CallbackHookConfig(
        pre_write_callback=pre_write_callback,
        post_write_callback=post_write_callback,
    )
    return ManabiDAVApp(
        {
            "mount_path": "/dav",
            "lock_storage": ManabiDbLockStorage(refresh, postgres_dsn),
            "provider_mapping": {
                "/dav": LoggedManabiProvider(
                    settings.MEDIA_ROOT, cb_hook_config=cb_hook_config
                ),
            },
            "middleware_stack": [
                HeaderLogger,
                WsgiDavDebugFilter,
                ErrorPrinter,
                ManabiAuthenticator,
                WsgiDavDirBrowser,
                RequestResolver,
            ],
            "manabi": {
                "key": key,
                "refresh": refresh,
                "initial": settings.MANABI_TOKEN_ACTIVATE_TIMEOUT,
            },
            "hotfixes": {
                "re_encode_path_info": False,
            },
            "suppress_version_info": True,
        }
    )


@transaction.atomic
def post_write_callback(token):
    from camac.document.models import Attachment
    from camac.user.models import User

    user, attachment = token.payload
    user = User.objects.get(id=user)
    attachment = Attachment.objects.get(attachment_id=attachment)
    path = Path(attachment.path.path)

    if path.exists():
        attachment.size = os.path.getsize(path)
        attachment.date = timezone.now()
        attachment.user = user
        attachment.save()
        if settings.LOG_FILE_WRITE_SIZES:
            log.info(
                f"post_write_callback -- ATTACHMENT_ID {attachment.pk}"
                f"\n\tattachment_name={attachment.name}"
                f"\n\tattachment_path={attachment.path}"
                f"\n\tattachment_size={attachment.size} (after writing)"
                f"\n\tuser={user.username}"
                f"\n\tattachment_group={attachment.group.pk if attachment.group else '-'}"
                f"\n\tattachment_instance={attachment.instance.pk}"
            )
            log.info(
                f"--------------------- END DAV WRITE ATTACHMENT_ID {attachment.pk} ---------------------"
            )


@transaction.atomic
def pre_write_callback(token):
    from camac.base import base36
    from camac.document.models import (
        Attachment,
        AttachmentVersion,
        version_path_directory_path,
    )
    from camac.user.models import User

    user, attachment = token.payload
    user = User.objects.get(id=user)
    attachment = Attachment.objects.get(attachment_id=attachment)
    create_version = attachment.user != user

    version_obj = attachment.version_history.order_by("version").last()

    if settings.APPLICATION.get("MANABI_VERSION_CREATION_THRESHOLD_ENABLED"):
        threshold = timedelta(
            seconds=settings.MANABI_VERSION_CREATION_THRESHOLD_SECONDS
        )
        delta = threshold * 2
        if version_obj:
            delta = timezone.now() - version_obj.created_at
        create_version = create_version or delta > threshold

    if create_version:
        version = 0
        if version_obj:
            version = version_obj.version + 1
        root = Path(settings.MEDIA_ROOT)
        path = Path(attachment.path.path)
        name = path.stem
        ext = path.suffix
        while True:
            suffix = base36.encode(version)
            suffix = suffix.rjust(2, "0")
            new_name = f"{name}_{suffix}{ext}"
            new_path = version_path_directory_path(attachment, new_name)
            version_path = root / new_path
            if not version_path.exists():  # pragma: no cover
                break
            version += 1  # pragma: no cover

        new = AttachmentVersion(
            name=new_name,
            attachment=attachment,
            size=attachment.size,
            path=new_path,
            created_at=attachment.date,
            created_by_user=attachment.user,
            version=version,
        )
        version_path.parent.mkdir(parents=True, exist_ok=True)
        copy2(path, version_path)
        new.save()
        if settings.LOG_FILE_WRITE_SIZES:
            log.info(
                f"pre_write_callback with new version -- ATTACHMENT_ID {attachment.pk}"
                f"\n\tversion={new.version}"
                f"\n\tversion_name={new.name}"
                f"\n\tversion_path={new.path}"
                f"\n\tversion_size={new.size} (before writing)"
                f"\n\tuser={user.username}"
                f"\n\tattachment_group={attachment.group.pk if attachment.group else '-'}"
                f"\n\tattachment_instance={attachment.instance.pk}"
            )
    elif settings.LOG_FILE_WRITE_SIZES:
        log.info(
            f"pre_write_callback without new version -- ATTACHMENT_ID {attachment.pk}"
            f"\n\tattachment_size={attachment.size} (before writing)"
            f"\n\tuser={user.username}"
            f"\n\tattachment_group={attachment.group.pk if attachment.group else '-'}"
            f"\n\tattachment_instance={attachment.instance.pk}"
        )

    return True
