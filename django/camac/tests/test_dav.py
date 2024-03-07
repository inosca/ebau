import os
from functools import partial
from io import BytesIO
from pathlib import Path

import pytest
from django.conf import settings
from django.urls import reverse
from manabi.token import Key, Token
from manabi.util import from_string
from pytest_factoryboy import LazyFixture

from camac.document import models, permissions

from ..base import base36
from ..dav import get_dav

environ = {
    "SERVER_PORT": "80",
    "REMOTE_HOST": "",
    "CONTENT_LENGTH": "",
    "SCRIPT_NAME": "/dav",
    "SERVER_PROTOCOL": "HTTP/1.1",
    "SERVER_SOFTWARE": "WSGIServer/0.2",
    "REQUEST_METHOD": "GET",
    "PATH_INFO": "/dav/1Ui3IS5xxIedbhSdPFPoGQRnTUtPVTmleMGJe1KyvWsVU704wk68k3YC70txTn5ZEJ4Ms3bh5Esy0OD4mZM0TnumUymWglgp3wq0CHo3W89DyW0/asdf_1tJa2fV.docx",
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


def do_get(dav, environ, start_response, file_):
    token = make_token(file_)
    environ["PATH_INFO"] = f"/dav/{token.as_url()}"
    list(dav(environ, start_response))


def do_put(dav, environ, start_response, file_, attachment, user):
    token = make_token(file_, user=user.id, attachment=attachment.attachment_id)
    put_environ = make_put(environ, token)
    list(dav(put_environ, start_response))


def make_put(environ, token):
    environ = dict(environ)
    environ["REQUEST_METHOD"] = "PUT"
    environ["CONTENT_LENGTH"] = "2"
    environ["wsgi.input"] = BytesIO(b"11")
    environ["PATH_INFO"] = f"/dav/{token.as_url()}"
    return environ


def make_token(path, user=1, attachment=2):
    key = Key(from_string(settings.MANABI_SHARED_KEY))
    payload = (user, attachment)
    return Token(key, path, payload=payload)


def prepare_file():
    file_path = Path(settings.MEDIA_ROOT, file_exists)
    os.makedirs(file_path.parent, exist_ok=True)
    file_path.touch(exist_ok=True)
    return file_path


@pytest.mark.parametrize(
    "role__name,instance__user", [("Municipality", LazyFixture("admin_user"))]
)
def test_callback(
    db,
    user_factory,
    attachment,
    attachment_section,
    mocker,
    admin_client,
    role,
):
    prepare_file()
    orig_encode = base36.encode
    encodes = []

    # fix permissions
    mode = permissions.AdminPermission
    mocker.patch(
        "camac.document.permissions.PERMISSIONS",
        {"test": {role.name.lower(): {mode: [attachment_section.pk]}}},
    )
    attachment.attachment_sections.add(attachment_section)

    def log_encodes(value):
        encodes.append(value)
        return orig_encode(value)

    mocker.patch("camac.base.base36.encode", log_encodes)
    results = []
    user1 = user_factory()
    user2 = user_factory()
    dav = get_dav()

    def start_response(status, headers, exc_info):
        results.append(status)

    get = partial(do_get, dav, environ, start_response)
    put = partial(do_put, dav, environ, start_response, file_exists, attachment)
    get(file_exists)

    put(user1)
    assert encodes == [0]

    put(user1)
    assert encodes == [0]

    put(user2)
    assert encodes == [0, 1]
    get(file_exists)
    assert results == ["200 OK"] + ["204 No Content"] * 3 + ["200 OK"]

    # Get version via API
    url = reverse("attachmentversion-list")
    response = admin_client.get(url)
    json = response.json()
    first_version = json["data"][0]
    version_id = first_version["relationships"]["attachment"]["data"]["id"]
    assert int(version_id) == int(attachment.attachment_id)

    # Download version
    path = first_version["attributes"]["path"]
    file_path = Path(settings.MEDIA_ROOT, "/".join(path.split("/")[-4:]))
    response = admin_client.get(path)
    assert response.status_code == 200
    assert Path(response.headers["X-Sendfile"]) == file_path

    # Delete
    version = models.AttachmentVersion.objects.first()
    file_path = Path(version.path.path)
    assert file_path.exists()
    version.delete()
    assert not file_path.exists()


def test_mock(mocker):
    prepare_file()
    results = []
    calls = []

    def callback(token):
        calls.append(token)
        return True

    mocker.patch("camac.dav.pre_write_callback", callback)
    mocker.patch("camac.dav.post_write_callback", callback)
    dav = get_dav()

    def start_response(status, headers, exc_info):
        results.append(status)

    # Drive the generator with list()
    list(dav(environ, start_response))

    get = partial(do_get, dav, environ, start_response)
    get(file_exists)

    token = make_token(file_exists)
    put_environ = make_put(environ, token)
    list(dav(put_environ, start_response))

    get(file_not_exists)

    assert results == ["403 Forbidden", "200 OK", "204 No Content", "404 Not Found"]
    assert len(calls) == 2
    assert calls[0].check(10)
