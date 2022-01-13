import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { saveAs } from "file-saver";

export default class CfDownloadComponent extends Component {
  @service notification;
  @service intl;
  @service fetch;

  @dropTask
  *export() {
    try {
      const query = this.args.field.document.rootForm.meta["is-main-form"]
        ? ""
        : `?form-slug=${this.field?.document.rootForm.slug}`;

      // generate document in CAMAC
      const response = yield this.fetch.fetch(
        `/api/v1/instances/${this.args.context.instanceId}/generate-pdf${query}`
      );

      const filename = response.headers
        .get("content-disposition")
        .match(/filename="(.*)"/)[1];

      saveAs(yield response.blob(), filename);
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("form.downloadError"));
    }
  }
}
