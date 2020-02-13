import Component from "@ember/component";
import { inject as service } from "@ember/service";
import { task } from "ember-concurrency";
import { saveAs } from "file-saver";
import slugify from "slugify";

export default Component.extend({
  notification: service(),
  intl: service(),
  fetch: service(),

  export: task(function*() {
    const { instanceId } = this.context;

    try {
      // Generate the PDF and prepare a filename.
      const formName = this.get("field.document.rootForm.name");
      const fileName = slugify(`${instanceId}-${formName}.pdf`.toLowerCase());
      const formSlug = this.get("field.document.rootForm.slug");

      let url = `/api/v1/instances/${instanceId}/generate_pdf`;

      if (["sb1", "sb2"].includes(formSlug)) {
        url += `?form-slug=${formSlug}`;
      }

      // generate document in CAMAC
      const response = yield this.fetch.fetch(url);

      const blob = yield response.blob();

      // Initialize PDF download in client.
      saveAs(blob, fileName);
    } catch (error) {
      this.notification.danger(this.intl.t("freigabequittung.downloadError"));
    }
  })
});
