from __future__ import annotations

import datetime
import typing
import uuid
from logging import getLogger

from django.conf import settings

from camac.document.views import AttachmentView
from camac.instance.master_data import MasterData
from camac.user.models import Group

if typing.TYPE_CHECKING:  # pragma: no cover
    from camac.document.models import Attachment
    from camac.instance.models import Instance


from camac.gever.utils import get_all_agr_service_slugs

from . import apimodels, client, models

log = getLogger(__name__)


class MissingGeschaeftError(RuntimeError):
    """Missing Geschaeft for given Instance.

    This could happen if you try to create a folder for an instance without
    first creating a Geschaeft (Or when the required Geschaeft could not be
    found for some other reason)
    """


class GeverAPI:
    """Internal API to perform sync operations to GEVER REST API."""

    # Internal Meta keys to use
    META_KEY_BASE_GESCHAEFT = "gever_base_geschaeft_id"
    META_KEY_SHOOTING_NOISE_GESCHAEFT = "gever_shooting_noise_geschaeft_id"
    META_KEY_BASE_ORDNER = "gever_base_ordner_id"
    META_KEY_SHOOTING_NOISE_ORDNER = "gever_shooting_noise_ordner_id"
    META_KEY_DOCUMENT = "gever_document_id"

    def __init__(self, instance: Instance):
        self.client = client.GEVERClient()
        self.instance = instance
        self.mapping = InstanceGeschaeftMapping(self.instance, self.client)

        self._geschaeft = None

    def sync_full(self):
        geschaeft = self.get_gever_geschaeft()
        if geschaeft:
            self.update_gever_geschaeft()
            return {"updated": True, "guid": str(geschaeft.guid)}
        else:
            geschaeft = self.create_gever_geschaeft()
            return {"created": True, "guid": str(geschaeft.guid)}

    def _verfahrensstand(self, slug):
        try:
            cv = models.CMIConstantValue.objects.get(
                use_for=models.CMIField.VERFAHRENSSTAND, slug=slug
            )
        except models.CMIConstantValue.DoesNotExist:  # pragma: no cover
            raise RuntimeError(f"Missing Constant Value: Verfahrensstand '{slug}'")
        return self.client.verfahrensstand.by_attribute("bezeichnung", cv.label)[0]

    def _origin_obj(self, origin_type):
        try:
            cv = models.CMIConstantValue.objects.get(
                use_for=models.CMIField.HERKUNFT, slug=f"herkunft-{origin_type}"
            )
        except models.CMIConstantValue.DoesNotExist:  # pragma: no cover
            raise RuntimeError(
                f"Missing Constant Value: Herkunft:'herkunft-{origin_type}'"
            )
        return self.client.origin.by_attribute("bezeichnung", cv.label)[0]

    def update_gever_geschaeft(self):
        gesch = self._geschaeft

        # TODO Verify with CMI: API says this is required (on update) but
        # during create, we could leave it as None...
        gesch.customGrundbucheintrag = (
            self.mapping.mapped_answer("agr-grundbucheintrag") or False
        )

        gesch.customKoordinatenX = self.mapping.gever_answerdata.get(
            "agr-koordinate-ost"
        )
        gesch.customKoordinatenY = self.mapping.gever_answerdata.get(
            "agr-koordinate-nord"
        )
        gesch.customParzellen = self.mapping.gever_answerdata.get("agr-parzellen")
        gesch.customMitVoranfrage = self.mapping.mapped_answer("agr-voranfrage")
        gesch.customSachbearbeiter = self.mapping.responsible_user()
        gesch.customMitVoranfrage = self.mapping.mapped_answer("agr-voranfrage")
        gesch.customErledigungsart = self.mapping.api_ref_from_answer(
            "agr-erledigungsart-auswahl"
        )

        self.client.geschaeft.update(gesch)
        self.sync_documents()

    def create_gever_geschaeft(self):
        """Create corresponding Geschaeft in GEVER, including files folder.

        Create Geschaeft, and corresponding folder, and sync the documents to it
        as well.
        """
        self._geschaeft = apimodels.Geschaeft(
            guid=None,  # will be set by API
            typeName="Geschäft",
            version=0,
            lifecycleStatus=apimodels.LifecycleStatus.IN_BEARBEITUNG,
            geschaeftsstatus=apimodels.GeschaeftsStatus.IN_BEARBEITUNG,
            titel=self.mapping.geschaeft_titel(),
            beginn=datetime.date.today(),
            customErledigungsart=self.mapping.api_ref_from_answer(
                "agr-erledigungsart-auswahl"
            ),
            customGrundbucheintrag=self.mapping.mapped_answer("agr-grundbucheintrag"),
            customVerfahrensstand=self._verfahrensstand(
                settings.GEVER["VERFAHRENSSTAND_OPEN"]
            ),
            customKoordinatenX=self.mapping.gever_answerdata.get("agr-koordinate-ost"),
            customKoordinatenY=self.mapping.gever_answerdata.get("agr-koordinate-nord"),
            customParzellen=self.mapping.gever_answerdata.get("agr-parzellen"),
            customMitVoranfrage=self.mapping.mapped_answer("agr-voranfrage"),
            customSachbearbeiter=self.mapping.responsible_user(),
            customHerkunft=self._origin_obj(self.mapping.get_origin()),
            customHerkunftsNummer=self.mapping.get_ebau_number(),
        )
        self._geschaeft.set_linked_instance_ids([self.instance.pk])
        self.client.geschaeft.create(
            self._geschaeft, template=self.mapping.get_geschaeft_template()
        )

        # We forward-link, which is better than having backwards-links,
        # especially in testing.
        # TODO: This will need to be extended for the secondary "Schiesslärm" geschaeft
        self.instance.case.meta[self.META_KEY_BASE_GESCHAEFT] = str(
            self._geschaeft.guid
        )
        self.instance.case.meta[self.META_KEY_SHOOTING_NOISE_GESCHAEFT] = None

        folder = apimodels.Ordner(
            guid=None,
            titel=self.mapping.folder_name(),
            parent=self._geschaeft,
            geschaeft=self._geschaeft,
        )
        self.client.folder.create(folder)
        self.instance.case.meta[self.META_KEY_BASE_ORDNER] = str(folder.guid)
        self.instance.case.meta[self.META_KEY_SHOOTING_NOISE_ORDNER] = None
        self.instance.case.save()

        return self._geschaeft

        # TODO: Also create "Aufgabe" and "Beteiligung" from template

    def get_gever_geschaeft(self) -> apimodels.Geschaeft | None:
        """Return the matching GEVER Geschaeft for our instance.

        The primary match is done via ebau-number, but to ensure correctness,
        we check the results such that the Geschaeft's parentkey references
        our instance as well
        """
        if self._geschaeft:
            # cached, yay
            return self._geschaeft

        geschaeft_guid = self.instance.case.meta.get(self.META_KEY_BASE_GESCHAEFT)
        if geschaeft_guid:
            self._geschaeft = self.client.geschaeft.by_guid(geschaeft_guid)
            return self._geschaeft

        # Fallback: Maybe we are a "new" instance for the same dossier?
        other_instances = self.instance.get_linked_instances().select_related("case")
        for inst in other_instances:  # pragma: todo cover
            other_guid = inst.case.meta.get(self.META_KEY_BASE_GESCHAEFT)
            if other_guid:
                self._geschaeft = self.client.geschaeft.by_guid(other_guid)
                return self._geschaeft

    def reload_geschaeft(self):
        self._geschaeft = self.get_gever_geschaeft().ref().resolve(self.client)
        return self._geschaeft

    def get_or_create_instance_folder(self):
        # TODO: This needs extending for the "shooting noise" vairant of the
        # Geschaeft as well
        gesch = self.get_gever_geschaeft()
        if not gesch:  # pragma: no cover
            raise MissingGeschaeftError()

        existing_folder = None
        if folder_guid := self.instance.case.meta.get(self.META_KEY_BASE_ORDNER):
            existing_folder = self.client.folder.by_guid(folder_guid)

        if existing_folder:
            log.debug(
                f"Existing folder found: {existing_folder.titel} "
                f"id={existing_folder.guid}"
            )
            return existing_folder
        else:
            if folder_guid:  # pragma: no cover
                log.error(
                    "GEVER Ordner with guid %s was not found on GEVER server. "
                    "Likely deleted in GEVER, creating new one",
                    folder_guid,
                )
            new_folder = apimodels.Ordner(
                parent=gesch,
                geschaeft=gesch,
                guid=None,
                titel=self.mapping.folder_name(),
            )
            self.client.folder.create(new_folder)
            log.debug(f"New folder created: '{new_folder.titel}' id={new_folder.guid}")
            self.instance.case.meta[self.META_KEY_BASE_ORDNER] = str(new_folder.guid)
            self.instance.case.meta[self.META_KEY_SHOOTING_NOISE_ORDNER] = None
            self.instance.case.save()

            return new_folder

    def sync_documents(self):
        geschaeft = self.get_gever_geschaeft()
        folder = self.get_or_create_instance_folder()

        res = {"created": 0, "updated": 0}
        for ebau_doc in self.get_documents_to_sync():
            gever_doc = None
            if document_guid := ebau_doc.context.get(self.META_KEY_DOCUMENT):
                try:
                    gever_doc = self.client.document.by_guid(document_guid)
                except Exception:  # pragma: no cover
                    # GEVER doc does not exist anymore - probably deleted.
                    # We'll just upload it again via "new" code path below
                    log.debug(
                        "GEVER Document with guid=%s is missing, will create again",
                        document_guid,
                    )
                    pass

            if gever_doc:
                # Existing, matching GEVER doc. Check if we need to update
                if self._needs_update(ebau_doc, gever_doc):
                    self._upload(ebau_doc, gever_doc)
                    res["updated"] += 1

            else:
                # Document does not yet exist in GEVER - create it
                new_gever_doc = apimodels.Dokument(
                    guid=None,
                    titel=self.mapping.document_titel(ebau_doc),
                    parentkey=self._make_doc_ref(ebau_doc),
                    geschaeftPosteingangExplorer=folder,
                    geschaeft=geschaeft,
                )
                self.client.document.create(new_gever_doc)
                ebau_doc.context[self.META_KEY_DOCUMENT] = str(new_gever_doc.guid)
                ebau_doc.save()
                self._upload(ebau_doc, new_gever_doc)
                res["created"] += 1
        return res

    def get_documents_to_sync(self):
        """Return a list of all the document-module attachments to be copied."""
        # This (ab)uses the AttachmentView to get the visible documents
        res = {}
        av = AttachmentView()
        for service_slug in get_all_agr_service_slugs():
            av.request = GeverAPI._fake_request(
                group=Group.objects.get(service__slug=service_slug)
            )
            res.update(
                {
                    doc.pk: doc
                    for doc in av.get_queryset(av.request.group).exclude(
                        # exclude the ones we already got - there may be overlap
                        # between the groups, and we don't want to double-sync
                        # documents
                        pk__in=list(res.keys())
                    )
                }
            )
        return list(res.values())

    class _fake_request:
        # We sync not "in the name of the user" but for all of AGR, even if
        # the current user wouldn't see an "internal" document. Therefore,
        # we fake a request object, to abuse documents module to give us all the
        # documents for syncing
        def __init__(self, group):
            self.query_params = {}
            self.group = group
            self.user = None

    def _upload(self, ebau_doc, gever_doc):
        log.debug(
            "Uploading eBau %s:%s doc to GEVER: %s",
            ebau_doc.pk,
            ebau_doc.path,
            gever_doc.titel,
        )
        try:
            with ebau_doc.path.open("rb") as fh:
                self.client.document.upload_version(
                    gever_doc, fh, apimodels.DocStatus.HAUPTVERSION
                )
        except Exception as exc:  # pragma: no cover
            log.error(
                "Could not upload document to GEVER: %s: %s", ebau_doc.pk, str(exc)
            )

    def _is_matching_document(self, attachment, document: apimodels.Dokument):
        """Check if the given attachment matches the GEVER document."""

        if not document.parentkey:  # pragma: no cover
            # Non-eBau document, ignoring (and also not being tested)
            return False

        version_tag = f"ebaube:{attachment.pk}:"
        return document.parentkey.startswith(version_tag)

    def _needs_update(self, attachment, document: apimodels.Dokument):
        """Return True if the given documents-module attachment matches the GEVER document."""

        if not document.parentkey:  # pragma: no cover
            raise RuntimeError(
                "Document mismatch - given GEVER doc is not linked to eBau"
            )

        if not self._is_matching_document(attachment, document):  # pragma: no cover
            raise RuntimeError(
                "Document mismatch - given GEVER doc does not belong to given eBau Attachment"
            )

        # The doc ref contains the version (timestamp), so if we have a new
        # version, we'll need to update.
        return document.parentkey != self._make_doc_ref(attachment)

    def _make_doc_ref(self, attachment):
        """
        Return a string that represents the current version of the attachment.

        This is used as a back-reference in the GEVER system.
        """
        # Regardless of attachment version objects, the latest version is always
        # the one in the attachment itself, and it's "date" attribute is updated
        # on uploads / changes
        version_date = attachment.date.isoformat(timespec="seconds")
        return f"ebaube:{attachment.pk}:{version_date}"


class InstanceGeschaeftMapping:
    def __init__(self, instance, client):
        self.client = client
        self.instance = instance

        self.md = MasterData(self.instance.case)

        self.gever_workitem = self.instance.case.work_items.filter(task="gever").first()
        if not self.gever_workitem:  # pragma: no cover
            raise RuntimeError("GEVER Data missing in eBau Dossier")

        gever_caluma_doc = self.gever_workitem.document
        self.gever_answerdata = {
            ans.question_id: ans.value for ans in gever_caluma_doc.answers.all()
        }

    def folder_name(self) -> str:
        """Return the name of the folder to be used for documents in the GEVER GEschäft.

        Specification:
        > Text; eBau erstellt pro Dossier einen neuen
        > Ordner im GEVER. Der Titel wird zusammen-
        > gesetzt aus Dossier-Nr., Gesuchstyp und
        > Parzellennummer, z.B. «123456 Voranfrage
        > Parzelle(n) 3456, 3457» oder «234567 Bau-
        > gesuch, Parzelle(n) 3456, 3457».
        """

        instance_id = self.instance.pk

        plot_numbers = ", ".join(
            [str(plot.get("plot_number")) for plot in self.md.plot_data]
        )

        if not plot_numbers:
            # TODO should not happen - cannot happen? Exception or nah?
            # This is not exactly according to spec
            return f"{instance_id} {self.dossier_type()} ohne Parzellenangabe"
        return f"{instance_id} {self.dossier_type()} Parzelle(n) {plot_numbers}"

    def geschaeft_titel(self) -> str:
        answervalue = self.gever_answerdata.get("agr-titel")
        if not answervalue:  # pragma: no cover
            raise RuntimeError("GEVER Data missing in eBau Dossier")
        return answervalue

    def document_titel(self, doc: Attachment) -> str:
        return doc.name

    def dossier_type_short(self):
        """Return "VA" or "BG" depending on dossier type."""
        return settings.GEVER["INSTANCE_TYPE_SHORT"][self.dossier_type()]

    def dossier_type(self):
        return self.instance.case.document.form.name.de

    def get_geschaeft_template(self):
        """Return Geschaeft template slug for given instance."""
        # TODO: This is currently incomplete (but not yet specified), as the
        # client noted that there are four additional variants for "Schiesslärm"
        # as well that we didn't know about before
        templates = settings.GEVER["GESCHAEFT_TEMPLATES"]

        template_defs = {
            "BG": {
                "municipality": templates["TEMPLATE_GESCHAEFT_EBAU_BG_GEMEINDE"],
                "rsta": templates["TEMPLATE_GESCHAEFT_EBAU_BG_RSTA"],
            },
            "PÄ": {
                "municipality": templates["TEMPLATE_GESCHAEFT_EBAU_BG_GEMEINDE"],
                "rsta": templates["TEMPLATE_GESCHAEFT_EBAU_BG_RSTA"],
            },
            "VA": {
                "municipality": templates["TEMPLATE_GESCHAEFT_EBAU_VA_GEMEINDE"],
                "rsta": templates["TEMPLATE_GESCHAEFT_EBAU_VA_RSTA"],
            },
        }
        dossier_type = str(self.dossier_type_short())

        rstakey = self.get_origin()

        return template_defs.get(dossier_type, {}).get(rstakey, None)

    def get_origin(self):
        """Return either "rsta" or "municipality" depending on lead authority."""
        svc = self.instance.responsible_service()
        if svc.service_group.name == "municipality":
            return "municipality"
        return "rsta"

    def mapped_answer(self, slug):
        value = self.gever_answerdata.get(slug)
        # We can be a bit "naive" here, as the options are all nicely prefixed
        # with the corresponding question's slug
        mappings = {
            # Grundbucheintrag?
            "agr-grundbucheintrag-ja": True,
            "agr-grundbucheintrag-nein": False,
            # "Mit Voranfrage"
            "agr-voranfrage-ja": True,
            "agr-voranfrage-nein": False,
        }
        return mappings.get(value, None)

    def api_ref(self, ref_key):
        """
        Return a CMI-style "foreign key reference" to the given object (or None).

        If the given key is not a UUID (or GUID, in windows-speak), then we'll
        just return None. Otherwise, a dict with a single "guid" key and our
        value of course
        """
        if not isinstance(ref_key, uuid.UUID):
            try:
                uuid.UUID(ref_key)
            except Exception:
                return None
        return {
            "guid": str(ref_key),
        }

    def api_ref_from_answer(self, slug):
        return self.api_ref(self.gever_answerdata.get(slug))

    def responsible_user(self):
        """Fetch responsible user from instance, map to GEVER ref."""
        # TODO: This should match one of the AGR groups (as of now,
        # the main AGR group; later: shooting noise group as well)
        responsible = self.instance.responsible_services.filter(
            service__slug=settings.GEVER["AGR_SERVICE_SLUG_BAUEN"]
        ).first()

        if not responsible:
            # This happens if AGR didn't define a responsible person
            # before triggering the sync
            return None

        user = responsible.responsible_user

        gever_matching_users = self.client.user.search_by_tentaql(
            f"email[{user.email}]"
        )

        if gever_matching_users:
            return gever_matching_users[0].ref()

    def get_ebau_number(self):
        return self.instance.case.meta["ebau-number"]
