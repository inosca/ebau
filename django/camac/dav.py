from django.conf import settings
from manabi import ManabiDAVApp
from manabi.auth import ManabiAuthenticator
from manabi.filesystem import ManabiProvider
from manabi.lock import ManabiDbLockStorage
from manabi.log import HeaderLogger, verbose_logging
from wsgidav.dir_browser import WsgiDavDirBrowser  # type: ignore
from wsgidav.error_printer import ErrorPrinter  # type: ignore
from wsgidav.mw.debug_filter import WsgiDavDebugFilter  # type: ignore
from wsgidav.request_resolver import RequestResolver  # type: ignore


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
    return ManabiDAVApp(
        {
            "mount_path": "/dav",
            "lock_storage": ManabiDbLockStorage(refresh, postgres_dsn),
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
