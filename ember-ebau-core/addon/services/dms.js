import Service, { service } from "@ember/service";
import { saveAs } from "file-saver";

import mainConfig from "ember-ebau-core/config/main";
import { MIME_TYPE_TO_EXTENSION } from "ember-ebau-core/utils/dms";
export default class DmsService extends Service {
  @service fetch;
  @service ebauModules;
  @service notification;
  @service intl;
  @service alexandriaDocuments;

  async generatePdf(instanceId, params = {}) {
    const query = Object.entries(params)
      .map(([k, v]) => `${k}=${v}`)
      .join("&");

    const fullQuery = query ? `?${query}` : "";
    const response = await this.fetch.fetch(
      `/api/v1/instances/${instanceId}/generate-pdf${fullQuery}`,
    );

    const filename = response.headers
      .get("content-disposition")
      .match(/filename="(.*)"/)[1];

    saveAs(await response.blob(), filename);
  }

  async processMerge({
    placeholders,
    templateSlug,
    filenameBase,
    instanceId,
    saveToDocuments = true,
    downloadPrefix = "",
  }) {
    const body = new FormData();
    const data = JSON.parse(JSON.stringify(placeholders));

    await Promise.all(
      Object.entries(data)
        .filter((entry) => String(entry[1]).startsWith("data:"))
        .map(async ([key, value]) => {
          const res = await fetch(value);
          const blob = await res.blob();

          body.append("files", blob, key);

          // Remove base64 string from JSON data to reduce payload size
          delete data[key];
        }),
    );

    body.append("data", JSON.stringify(data));

    try {
      const response = await this.fetch.fetch(
        `/document-merge-service/api/v1/template/${templateSlug}/merge/`,
        {
          method: "POST",
          headers: { "content-type": undefined, accept: "*/*" },
          body,
        },
      );

      const blob = await response.blob();
      const extension = MIME_TYPE_TO_EXTENSION[blob.type];
      const filename = `${filenameBase}${extension}`;

      if (saveToDocuments) {
        if (mainConfig.documentBackend === "camac") {
          await this.saveToDocumentsCamac(blob, filename, instanceId);
        } else {
          await this.saveToDocumentsAlexandria(blob, filename);
        }

        this.notification.success(this.intl.t("dms.merge-and-save-success"));
      } else {
        saveAs(blob, `${downloadPrefix}${filename}`);
      }
    } catch (error) {
      this.notification.danger(this.intl.t("dms.merge-error"));
      throw error;
    }
  }

  async saveToDocumentsCamac(blob, filename, instanceId) {
    const attachmentBody = new FormData();
    const attachmentSection = mainConfig.attachmentSections.internal;

    attachmentBody.append("attachment_sections", attachmentSection);
    attachmentBody.append("instance", instanceId);
    attachmentBody.append("path", blob, filename);

    await this.fetch.fetch(`/api/v1/attachments`, {
      method: "POST",
      headers: { "content-type": undefined },
      body: attachmentBody,
    });
  }

  async saveToDocumentsAlexandria(blob, filename) {
    const file = new File([blob], filename, { type: blob.type });
    await this.alexandriaDocuments.upload("intern", [file]);
  }
}
