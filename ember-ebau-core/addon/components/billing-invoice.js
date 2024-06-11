import { service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";

import DmsGenerateComponent from "ember-ebau-core/components/dms/generate";
import mainConfig from "ember-ebau-core/config/main";
import { MIME_TYPE_TO_EXTENSION } from "ember-ebau-core/utils/dms";

export default class BillingInvoice extends DmsGenerateComponent {
  @service notification;
  @service intl;
  @service fetch;

  chargeAndMerge = dropTask(this, async () => {
    const body = new FormData();
    const saveToDocuments = true;

    body.append("data", JSON.stringify(this.placeholders.value));

    await Promise.all(
      Object.entries(this.placeholders.value)
        .filter((entry) => String(entry[1]).startsWith("data:"))
        .map(async ([key, value]) => {
          const res = await fetch(value);
          const blob = await res.blob();

          body.append("files", blob, key);
        }),
    );

    try {
      const response = await this.fetch.fetch(
        `/document-merge-service/api/v1/template/${this.template.slug}/merge/`,
        {
          method: "POST",
          headers: { "content-type": undefined, accept: "*/*" },
          body,
        },
      );
      const blob = await response.blob();

      const extension = MIME_TYPE_TO_EXTENSION[blob.type];
      const filename = `${this.template.description}${extension}`;

      if (saveToDocuments) {
        if (mainConfig.documentBackend === "camac") {
          await this.saveToDocumentsCamac(blob, filename);
        } else {
          await this.saveToDocumentsAlexandria(blob, filename);
        }
      } else {
        saveAs(blob, `${this.args.instanceId} - ${filename}`);
      }

      await this.args.charge.perform();

      this.template = null;
    } catch {
      this.notification.danger(this.intl.t("dms.merge-error"));
    }
  });
}
