import Component from "@ember/component";
import { inject as service } from "@ember/service";
import { saveAs } from "file-saver";
import { task } from "ember-concurrency";
import slugify from "slugify";

export default Component.extend({
  notification: service(),
  intl: service(),
  documentExport: service(),

  export: task(function*() {
    const { instanceId } = this.context;

    try {
      // Generate the PDF and prepare a filename.
      const blob = yield this.documentExport.merge(
        instanceId,
        this.field.document
      );
      const formName = this.field.document.rootForm.name;
      const fileName = slugify(`${instanceId}-${formName}.pdf`.toLowerCase());

      // Initialize PDF download in client.
      saveAs(blob, fileName);
    } catch (error) {
      this.notification.danger(this.intl.t("freigabequittung.downloadError"));
    }
  })
});
