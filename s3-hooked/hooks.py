import io
from typing import List, Optional, Tuple

import clamd
import magic
import requests
from aiohttp import web
from proxy.app import log
from proxy.conf import Settings
from proxy.default_hooks import *  # noqa: F401,F403
from proxy.events import on, post_upload, pre_upload_before_check, pre_upload_unsafe
from proxy.utils import extract_object_props
from yarl import URL


class HookSettings(Settings):
    CLAMD_TCP_ADDR: str = "clamav"
    CLAMD_TCP_SOCKET: int = 3310
    CLAMD_ENABLED: bool = True

    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/tiff",
        "image/bmp",
        "image/svg+xml",
        "image/webp",
        "application/pdf",
        "application/zip",
        "text/plain",
        "text/html",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/vnd.oasis.opendocument.text",
        "application/vnd.oasis.opendocument.spreadsheet",
        "application/vnd.oasis.opendocument.presentation",
        "application/vnd.oasis.opendocument.graphics",
        "application/vnd.oasis.opendocument.formula",
        "application/vnd.oasis.opendocument.database",
        "application/vnd.oasis.opendocument.chart",
    ]


settings = HookSettings()


@on(pre_upload_unsafe)
def hook_file_type(
    request: web.Request,
    data: bytes,
) -> Tuple[bool, Optional[str]]:
    passed, result = check_file_type(data, request.headers.get("Content-Type"))
    if not passed:
        log.info(f"File-type check failed for {request} ({result})")
    return passed, result


def check_file_type(content: bytes, declared_mimetype: str) -> Tuple[bool, str]:
    if declared_mimetype is None:
        msg = "File type checking requires that a content type is declared."
        return False, msg
    return (
        (identified_mime := magic.from_buffer(content, mime=True)) == declared_mimetype
        and identified_mime in settings.ALLOWED_FILE_TYPES,
        identified_mime,
    )


# The default hook for encryption is pos=0. So any following hook should be numbered
# with pos > 0 to avoid stealing its position.
@on(pre_upload_before_check)
def hook_scan_for_virus(
    request: web.Request,
    data: bytes,
) -> Tuple[bool, Optional[str]]:
    if not settings.CLAMD_ENABLED:
        return (True, None)

    clean, msg = scan_for_virus(data)
    return clean, msg


def scan_for_virus(bytestr: bytes) -> Tuple[bool, Optional[str]]:
    scanner = clamd.ClamdNetworkSocket(
        settings.CLAMD_TCP_ADDR, settings.CLAMD_TCP_SOCKET
    )
    f = io.BytesIO(bytestr)
    f.seek(0)
    try:
        result = scanner.instream(f)
    except IOError:
        # Ping the server if it fails than the server is down
        scanner.ping()
        # Server is up. This means that the file is too big.
        msg = "The file is too large."
        log.warning(
            "The file is too large for ClamD to scan it. Bytes Read {size}".format(
                size=f.tell()
            )
        )
        return False, msg

    if result and result["stream"][0] == "FOUND":
        msg = "Clamav detetcted an infection."
        log.info(msg)
        return False, msg

    return True, None


@on(post_upload)
def hook_alexandria_thumbnail(request: web.Request, data: Optional[bytes] = None):
    record = extract_object_props(request)
    payload = {
        "Records": [
            {"s3": {"bucket": {"name": record.bucket}, "object": {"key": record.name}}}
        ]
    }
    url = URL.build(host="django", scheme="http", path="/alexandria/api/v1/hook")
    with requests.Session() as session:
        resp = session.post(url, json=payload)
        return resp.status_code < 400, resp
