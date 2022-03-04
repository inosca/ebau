from pathlib import Path

from django.conf import settings
from manabi.auth import ManabiAuthenticator
from manabi.filesystem import ManabiProvider
from manabi.lock import ManabiLockLockStorage
from manabi.log import HeaderLogger, verbose_logging
from wsgidav.dir_browser import WsgiDavDirBrowser  # type: ignore
from wsgidav.error_printer import ErrorPrinter  # type: ignore
from wsgidav.mw.debug_filter import WsgiDavDebugFilter  # type: ignore
from wsgidav.request_resolver import RequestResolver  # type: ignore
from wsgidav.wsgidav_app import WsgiDAVApp  # type: ignore


def get_dav():
    key = settings.MANABI_SHARED_KEY
    if not key:  # pragma: no cover
        raise RuntimeError("MANABI_SHARED_KEY is missing")
    refresh = settings.MANABI_TOKEN_REFRESH_TIMEOUT
    if settings.MANABI_DEBUG:
        verbose_logging()
    return WsgiDAVApp(
        {
            "mount_path": "/dav",
            "lock_storage": ManabiLockLockStorage(
                refresh, Path(settings.MEDIA_ROOT, "manabi")
            ),
            "provider_mapping": {
                "/": ManabiProvider(settings.MEDIA_ROOT),
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
        }
    )
