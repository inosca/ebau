import Component from "@ember/component";
import { inject as service } from "@ember/service";
import { saveAs } from "file-saver";
import { task } from "ember-concurrency";
import { warn, assert } from "@ember/debug";

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

function prepareReceiptPage(data) {
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
      label: "8. Unterschriften",
      children: sources.map(table => ({
        type: "SignatureQuestion",
        label: table.label.replace(/^Personalien -\s*/, ""),
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
}

export default Component.extend({
  notification: service(),
  intl: service(),
  fetch: service(),
  calumaStore: service(),

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
      sections: parseDocument(document, navigation)
    };

    if (document.findField("personalien")) {
      data = prepareReceiptPage(data);
    }

    const template = this.field.question.meta.template;
    const filename = `${instanceId}-${document.rootForm.slug}.pdf`;

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
        saveAs(body, filename);
      } else {
        throw new Error(response.statusText || response.status);
      }
    } catch (error) {
      this.notification.danger(this.intl.t("freigabequittung.downloadError"));
    }
  })
});
