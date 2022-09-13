import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";

export default class BeDownloadPdfComponent extends Component {
  @service notification;
  @service intl;
  @service fetch;

  @dropTask
  *export() {
    try {
      const query = this.args.field.document.rootForm.raw.meta["is-main-form"]
        ? ""
        : `?form-slug=${this.args.field.document.rootForm.slug}`;

      // generate document in CAMAC
      const response = yield this.fetch.fetch(
        `/api/v1/instances/${this.args.context.instanceId}/generate-pdf${query}`
      );

      const filename = response.headers
        .get("content-disposition")
        .match(/filename="(.*)"/)[1];

      saveAs(yield response.blob(), filename);
    } catch (error) {
      this.notification.danger(this.intl.t("freigabequittung.downloadError"));
    }
  }
}
