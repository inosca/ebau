from __future__ import annotations

import json
import typing
import uuid
from io import FileIO
from logging import getLogger
from typing import Generic, Optional, TypeVar

import magic
from django.conf import settings
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

if typing.TYPE_CHECKING:  # pragma: no cover
    import requests


from . import apimodels, models

log = getLogger(__name__)

EndpointType = TypeVar("EndpointType", bound=apimodels.BaseCMIObject)

DEFAULT_PARAMS_BY_TYPE = {
    # Document fetching: We want *all* versions
    apimodels.Dokument: {"latestOnly": "false", "originalOnly": "true"}
}


class Endpoint(Generic[EndpointType]):
    def __init__(self, client: GEVERClient, path: str, type_: type):
        self._client = client
        self._client_session = client._session
        self._path = path
        self._type = type_

    def _endpoint(self, name: str) -> str:
        return self._client._endpoint(f"{self._path}/{name}")

    def search_by_tentaql(self, search_expr: str) -> list[EndpointType]:
        """Search "Geschäft" - base implementation.

        Search Geschaeft entities by the given TentaQl Query object.
        """
        resp = self._client_session.post(
            self._endpoint("Search"),
            headers={"content-type": "application/json"},
            data=json.dumps(search_expr),
        )
        resp.raise_for_status()
        return self._type.schema().loads(resp.content, many=True)

    def all(self):
        return self.search_by_tentaql("FULLTEXT[*]")

    def by_guid(
        self, guid: uuid.UUID, params: Optional(dict) = None
    ) -> EndpointType | None:
        # Fetch default params, if defined
        params = params or DEFAULT_PARAMS_BY_TYPE.get(self._type)
        resp = self._client_session.get(self._endpoint(str(guid)), params=params)
        resp.raise_for_status()
        return self._type.schema().loads(resp.content)

    def _get_template_path(
        self, required_type: str, template: str | models.CMIObjectTemplate
    ) -> str | None:  # pragma: no cover
        # cov: This will be fully covered once we re-enable the GESCHAEFT_TEMPLATES
        # parametrisation
        """Return the path (in CMI) of the given template.

        Template can be either a models.CMIObjectTemplate object, or a slug
        that refers to one of those templates.
        """
        match template:
            case str(_):
                template_obj = models.CMIObjectTemplate.objects.get(slug=template)
            case models.CMIObjectTemplate():
                template_obj = template
            case None:
                return None
            case _:  # pragma: no cover
                raise RuntimeError(f"template param not understood: {template}")

        if str(template_obj.use_for) != required_type:  # pragma: no cover
            # This is a programming error - caller requests wrong template
            raise RuntimeError(
                f"Given template is for {template_obj.use_for}, "
                f"but we want to create a {required_type}"
            )

        return template_obj.template_path

    def create(
        self,
        obj: EndpointType,
        template: Optional[str] = None,
        raise_on_error: bool = True,
    ) -> requests.Response:
        """Create given object on the API, return the response object.

        If the response was successful, the object's GUID is updated according
        to the response, so you can start working with it.

        If the response was *not* successful, an exception will be raised,
        unless you pass in `raise_on_error=False`. In that case, the response
        object will be returned just as if it was successful. It will then be
        the caller's job to evaluate any status codes.
        """

        obj_type = type(obj).__name__
        template_path = self._get_template_path(obj_type, template)

        log.debug(f"Creating {obj_type} using template: {template_path}")
        resp = self._client_session.post(
            self._endpoint(""),
            json=obj.to_dict(),
            params={"vorlage": template_path} if template_path else None,
        )
        if raise_on_error and resp.status_code > 201:  # pragma: no cover
            raise RuntimeError(f"Could not create {type(obj).__name__}: {resp.content}")

        if resp.status_code in [200, 201]:
            new_guid = uuid.UUID(resp.json())
            obj.guid = new_guid

        return resp

    def delete(
        self, obj: EndpointType, raise_on_error: bool = True
    ) -> requests.Response:
        """Delete the given object on the CMI API.

        If the response was successful, it will be returned for optional further
        inspection.

        If the response was *not* successful, an exception will be raised,
        unless you pass in `raise_on_error=False`. In that case, the response
        object will be returned just as if it was successful. It will then be
        the caller's job to evaluate any status codes.
        """
        resp = self._client_session.delete(self._endpoint(obj.guid))
        if raise_on_error:
            resp.raise_for_status()
        return resp

    def update(
        self, obj: EndpointType, raise_on_error: bool = True
    ) -> requests.Response:
        """Update the given object on the CMI API.

        If the response was successful, it will be returned for optional further
        inspection.

        If the response was *not* successful, an exception will be raised,
        unless you pass in `raise_on_error=False`. In that case, the response
        object will be returned just as if it was successful. It will then be
        the caller's job to evaluate any status codes.
        """

        resp = self._client_session.put(self._endpoint(obj.guid), json=obj.to_dict())
        if raise_on_error:
            resp.raise_for_status()
        return resp


class GeschaeftEndpoint(Endpoint[apimodels.Geschaeft]):
    def __init__(self, client: GEVERClient):
        super().__init__(client, "Geschaeft", apimodels.Geschaeft)

    def search_by_ebau_nr(self, ebau_nr: str) -> list[apimodels.Geschaeft]:
        """Search "Geschäft" by the given EBAU-Number.

        Note: There should only ever be one GEVER Geschaeft for each eBau Number.
        There can be multiple instances however, each of them mapping their
        documents into their own folder in the Geschaeft.
        """
        return self.search_by_tentaql(f"customHerkunftsNummer[{ebau_nr}]")


class CustomErledigungsartEndpoint(Endpoint[apimodels.CustomErledigungsart]):
    def __init__(self, client: GEVERClient):
        super().__init__(client, "CustomErledigungsart", apimodels.CustomErledigungsart)


class FolderEndpoint(Endpoint):
    def __init__(self, client: GEVERClient):
        super().__init__(client, "Ordner", apimodels.Ordner)


class OrgunitEndpoint(Endpoint):
    def __init__(self, client: GEVERClient):
        super().__init__(client, "Organisationseinheit", apimodels.Organisatinseinheit)


class AmtEndpoint(Endpoint):
    def __init__(self, client: GEVERClient):
        super().__init__(client, "CustomAmt", apimodels.CustomAmt)


class BenutzerEndpoint(Endpoint):
    def __init__(self, client: GEVERClient):
        super().__init__(client, "Benutzer", apimodels.Benutzer)


class GemeindeEndpoint(Endpoint):
    def __init__(self, client: GEVERClient):
        super().__init__(client, "Gemeinde", apimodels.Gemeinde)


class RegistraturplanEndpoint(Endpoint):
    def __init__(self, client: GEVERClient):
        super().__init__(
            client, "CustomRegistraturplan", apimodels.CustomRegistraturplan
        )


class DocumentEndpoint(Endpoint):
    def __init__(self, client: GEVERClient):
        super().__init__(client, "Dokument", apimodels.Dokument)

    def download(
        self,
        document: apimodels.Dokument,
        version: float = None,
        raise_on_error: bool = True,
    ) -> requests.Response:
        """Download the given document.

        If you pass in a version, that specific version is downloaded. Otherwise,
        the newest version is taken
        """
        download_url = self._endpoint(f"FileContent/{document.guid}")
        resp = self._client_session.get(download_url, params={"version": version})
        if raise_on_error:
            resp.raise_for_status()

        return resp

    def upload_version(
        self,
        document: apimodels.Document,
        fh: FileIO,
        version_status: apimodels.DocStatus,
        comment: Optional[str] = None,
        raise_on_error: bool = True,
    ) -> None:
        endpoint_checkout = self._endpoint(f"CheckOut/{document.guid}")
        endpoint_checkin = self._endpoint(f"CheckIn/{document.guid}")

        if document.eDokument:
            # checked-in document exists - need to checkout before upload
            resp_checkout = self._client_session.post(endpoint_checkout)
            resp_checkout.raise_for_status()

        form_data = {
            "checkInComment": comment,
            "dokumentStatus": version_status.value,
        }

        mime_type = magic.from_buffer(fh.read(), mime=True)
        fh.seek(0)

        resp_checkin = self._client_session.post(
            endpoint_checkin,
            data=form_data,
            files={"file": (fh.name, fh, mime_type)},
        )
        if raise_on_error:
            resp_checkin.raise_for_status()


class GEVERClient:
    ENDPOINTS_BY_API_TYPE = {
        # yes we need both :(
        "Geschäft": "geschaeft",
        "Geschaeft": "geschaeft",
        "Ordner": "folder",
        "Dokument": "document",
        "Organisationseinheit": "orgunit",
        "CustomAmt": "amt",
        "Registraturplan": "registraturplan",
        "Benutzer": "user",
        "Gemeinde": "municipality",
        "CustomErledigungsart": "erledigungsart",
    }

    def __init__(self):
        # We want to know where the slashes are - so if the config has trailing
        # slashes, drop it
        self._token = {}
        self.base_url = settings.GEVER["API_BASE_URL"].strip("/")

        self._client = BackendApplicationClient(client_id=settings.GEVER["CLIENT_ID"])

        # TODO scopes: oidc metatool cmiScope
        # grant_type client_credentials

        self._session = OAuth2Session(
            token=self._token,
            client=self._client,
            client_id=settings.GEVER["CLIENT_ID"],
            auto_refresh_url=settings.GEVER["TOKEN_URL"],
            auto_refresh_kwargs={
                "client_secret": settings.GEVER["CLIENT_SECRET"],
                "client_id": settings.GEVER["CLIENT_ID"],
            },
            token_updater=self._save_token,
        )
        self._perform_login()

    def _save_token(self, token: dict) -> None:
        self._token.update(token)

    def _perform_login(self) -> None:
        self._save_token(
            self._session.fetch_token(
                settings.GEVER["TOKEN_URL"],
                client_secret=settings.GEVER["CLIENT_SECRET"],
                client_id=settings.GEVER["CLIENT_ID"],
            )
        )

    def get_endpoint(self, api_type: str) -> Endpoint:
        endpoint_attr = self.ENDPOINTS_BY_API_TYPE[api_type]
        return getattr(self, endpoint_attr)

    def _endpoint(self, name: str) -> str:
        return f"{self.base_url}/{name}"

    @property
    def geschaeft(self) -> GeschaeftEndpoint[apimodels.Geschaeft]:
        return GeschaeftEndpoint(self)

    @property
    def orgunit(self) -> OrgunitEndpoint[apimodels.Organisatinseinheit]:
        return OrgunitEndpoint(self)

    @property
    def amt(self) -> AmtEndpoint[apimodels.CustomAmt]:
        return AmtEndpoint(self)

    @property
    def registraturplan(
        self,
    ) -> RegistraturplanEndpoint[apimodels.CustomRegistraturplan]:
        return RegistraturplanEndpoint(self)

    @property
    def document(self) -> DocumentEndpoint[apimodels.Dokument]:
        return DocumentEndpoint(self)

    @property
    def folder(self) -> FolderEndpoint[apimodels.Ordner]:
        return FolderEndpoint(self)

    @property
    def user(self) -> BenutzerEndpoint[apimodels.Benutzer]:
        return BenutzerEndpoint(self)

    @property
    def erledigungsart(
        self,
    ) -> CustomErledigungsartEndpoint[apimodels.CustomErledigungsart]:
        return CustomErledigungsartEndpoint(self)

    @property
    def municipality(self) -> GemeindeEndpoint[apimodels.Gemeinde]:
        return GemeindeEndpoint(self)
