import Component from "@ember/component";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";
import { saveAs } from "file-saver";

export default Component.extend({
  notification: service(),
  intl: service(),
  fetch: service(),

  export: task(function* () {
    try {
      const query = this.get("field.document.rootForm.meta.is-main-form")
        ? ""
        : `?form-slug=${this.get("field.document.rootForm.slug")}`;

      // generate document in CAMAC
      const response = yield this.fetch.fetch(
        `/api/v1/instances/${this.context.instanceId}/generate-pdf${query}`
      );

      const filename = response.headers
        .get("content-disposition")
        .match(/filename="(.*)"/)[1];

      saveAs(yield response.blob(), filename);
    } catch (error) {
      this.notification.danger(this.intl.t("freigabequittung.downloadError"));
    }
  }),
});
