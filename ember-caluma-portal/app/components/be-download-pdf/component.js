import Component from "@ember/component";
import { inject as service } from "@ember/service";
import { saveAs } from "file-saver";
import { task } from "ember-concurrency";
import { warn, assert } from "@ember/debug";
import slugify from "slugify";

import { parseDocument } from "ember-caluma-portal/components/be-download-pdf/parsers";

const PEOPLE_SOURCES = {
  "personalien-gesuchstellerin": {
    familyName: "name-gesuchstellerin",
    givenName: "vorname-gesuchstellerin"
  },
  "personalien-vertreterin-mit-vollmacht": {
    familyName: "name-vertreterin",
    givenName: "vorname-vertreterin"
  },
  "personalien-grundeigentumerin": {
    familyName: "name-grundeigentuemerin",
    givenName: "vorname-grundeigentuemerin"
  },
  "personalien-gebaudeeigentumerin": {
    familyName: "name-gebaeudeeigentuemerin",
    givenName: "vorname-gebaeudeeigentuemerin"
  },
  "personalien-projektverfasserin": {
    familyName: "name-projektverfasserin",
    givenName: "vorname-projektverfasserin"
  }
};

const PEOPLE_TARGET = "8-freigabequittung";

export default Component.extend({
  notification: service(),
  intl: service(),
  fetch: service(),
  calumaStore: service(),

  prepareReceiptPage(data) {
    try {
      const sources = data.sections
        .find(section => section.slug === "1-allgemeine-informationen")
        .children.find(section => section.slug === "personalien")
        .children.filter(section =>
          Object.keys(PEOPLE_SOURCES).includes(section.slug)
        );

      const target = data.sections.find(
        section => section.slug === PEOPLE_TARGET
      );

      Object.assign(target, {
        slug: "8-unterschriften",
        label: `8. ${this.intl.t("pdf.signatures")}`,
        children: sources.map(table => ({
          type: "SignatureQuestion",
          label: table.label
            .replace(new RegExp(`^${this.intl.t("pdf.personalities")} -`), "")
            .trim(),
          people: table.rows.map(row => ({
            familyName: row.find(
              column => column.slug === PEOPLE_SOURCES[table.slug].familyName
            ).value,
            givenName: row.find(
              column => column.slug === PEOPLE_SOURCES[table.slug].givenName
            ).value
          }))
        }))
      });
    } catch (error) {
      warn("Failed to prepare receipt page", {
        id: "be-download-pdf.receipt-page-failed"
      });
    }

    return data;
  },

  /**
   * Submits the data (as JSON) to a service and gets a PDF back.
   * Service: https://github.com/adfinis-sygroup/document-merge-service/
   *
   * @method export
   */
  export: task(function*() {
    const { instanceId } = this.context;
    const document = this.field.document;
    const navigation = this.calumaStore.find(
      `Navigation:${this.field.document.pk}`
    );

    let data = {
      caseId: instanceId,
      caseType: document.rootForm.name,
      sections: parseDocument(document, navigation),
      signatureMetadata: this.intl.t("pdf.signatureMetadata"),
      signatureTitle: this.intl.t("pdf.signature")
    };

    if (document.findField("personalien")) {
      data = this.prepareReceiptPage(data);
    }

    const template = this.field.question.meta.template;

    assert("A template must be passed to the fields meta", template);

    try {
      const response = yield this.fetch.fetch(
        `/document-merge-service/api/v1/template/${template}/merge/`,
        {
          mode: "cors",
          method: "POST",
          headers: {
            "content-type": "application/json; charset=utf-8",
            accept: "*/*"
          },
          body: JSON.stringify({ data, convert: "pdf" })
        }
      );

      if (response.ok) {
        const body = yield response.blob();
        saveAs(
          body,
          slugify(`${instanceId}-${document.rootForm.name}.pdf`.toLowerCase())
        );
      } else {
        throw new Error(response.statusText || response.status);
      }
    } catch (error) {
      this.notification.danger(this.intl.t("freigabequittung.downloadError"));
    }
  })
});
