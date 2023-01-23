import { getOwner } from "@ember/application";
import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import DocumentValidityButtonComponent from "ember-ebau-core/components/document-validity-button";
import LinkAttachmentsComponent from "ember-ebau-core/components/link-attachments";
import UrGisComponent from "ember-ebau-core/components/ur-gis";

import BeClaimsFormComponent from "caluma-portal/components/be-claims-form";
import BeDisabledInputComponent from "caluma-portal/components/be-disabled-input";
import BeDocumentsFormComponent from "caluma-portal/components/be-documents-form";
import BeDownloadPdfComponent from "caluma-portal/components/be-download-pdf";
import BeGisComponent from "caluma-portal/components/be-gis";
import BeSubmitInstanceComponent from "caluma-portal/components/be-submit-instance";
import { isEmbedded } from "caluma-portal/helpers/is-embedded";

export default class ApplicationRoute extends Route {
  @service session;
  @service router;
  @service calumaOptions;

  queryParams = {
    language: { refreshModel: true },
    group: { refreshModel: true },
  };

  async beforeModel(transition) {
    super.beforeModel(transition);

    await this.session.setup();

    const { language, group: groupId } = transition.to?.queryParams ?? {};

    this.session.language = language ?? this.session.language;
    this.session.groupId = groupId ?? this.session.groupId;

    if (language || groupId) {
      // after the transition remove the query params so we don't persist the
      // language and group info twice (in the URL and in the session)
      transition.then(() => {
        this.router.replaceWith({
          queryParams: { language: null, group: null },
        });
      });
    }

    if (isEmbedded()) {
      getOwner(this)
        .lookup("service:-document")
        .querySelector("body")
        .classList.add("embedded");
    }

    this.calumaOptions.registerComponentOverride({
      label: "Karte",
      component: "be-gis",
      componentClass: BeGisComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "GIS-Karte (Kt. UR)",
      component: "ur-gis",
      componentClass: UrGisComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Einreichen Button",
      component: "be-submit-instance",
      componentClass: BeSubmitInstanceComponent,
      type: "CheckboxQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Dokument Formular",
      component: "be-documents-form",
      componentClass: BeDocumentsFormComponent,
      type: "FormQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Download (PDF)",
      component: "be-download-pdf",
      componentClass: BeDownloadPdfComponent,
      type: "StaticQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Nachforderungen Formular",
      component: "be-claims-form",
      componentClass: BeClaimsFormComponent,
      type: "Form",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Deaktiviert",
      component: "be-disabled-input",
      componentClass: BeDisabledInputComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "eBau Nummer Vorschlagen",
      component: "suggest-ebau-number",
      type: "StaticQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "eBau Nummer Weiter Button",
      component: "assign-ebau-number-button",
      type: "StaticQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Entscheid verfügen (Teilbaubewilligung)",
      component: "decision-submit-partial",
      type: "StaticQuestion",
    });
    this.calumaOptions.registerComponentOverride({
      label: "Validierungs Button",
      component: "document-validity-button",
      componentClass: DocumentValidityButtonComponent,
    });
    this.calumaOptions.registerComponentOverride({
      label: "Dokumente verlinken",
      component: "link-attachments",
      componentClass: LinkAttachmentsComponent,
    });
  }
}
