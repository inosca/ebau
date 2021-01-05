import os
from pathlib import Path

from django.conf import settings
from manabi.token import Key, Token
from manabi.util import from_string

from ..dav import get_dav

environ = {
    "SERVER_PORT": "80",
    "REMOTE_HOST": "",
    "CONTENT_LENGTH": "",
    "SCRIPT_NAME": "/dav",
    "SERVER_PROTOCOL": "HTTP/1.1",
    "SERVER_SOFTWARE": "WSGIServer/0.2",
    "REQUEST_METHOD": "GET",
    "PATH_INFO": "/1Ui3IS5xxIedbhSdPFPoGQRnTUtPVTmleMGJe1KyvWsVU704wk68k3YC70txTn5ZEJ4Ms3bh5Esy0OD4mZM0TnumUymWglgp3wq0CHo3W89DyW0/asdf_1tJa2fV.docx",
    "QUERY_STRING": "",
    "REMOTE_ADDR": "172.21.0.12",
    "CONTENT_TYPE": "text/plain",
    "HTTP_USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    "HTTP_ACCEPT": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "HTTP_ACCEPT_ENCODING": "gzip,deflate",
    "HTTP_ACCEPT_LANGUAGE": "en-US,en;q=0.9,de;q=0.8",
}

file_exists = Path("attachments/files/2/asdf.docx")
file_not_exists = Path("attachments/files/2/not.docx")


def test_dav():
    file_path = Path(settings.MEDIA_ROOT, file_exists)
    results = []

    def start_response(status, headers, exc_info):
        results.append(status)

    dav = get_dav()
    # Drive the generator with list()
    list(dav(environ, start_response))

    os.makedirs(file_path.parent, exist_ok=True)
    file_path.touch(exist_ok=True)
    key = Key(from_string(settings.MANABI_SHARED_KEY))
    token = Token(key, file_exists)
    environ["PATH_INFO"] = f"/{token.as_url()}"
    list(dav(environ, start_response))

    token = Token(key, file_not_exists)
    environ["PATH_INFO"] = f"/{token.as_url()}"
    list(dav(environ, start_response))

    assert results == ["403 Forbidden", "200 OK", "404 Not Found"]
