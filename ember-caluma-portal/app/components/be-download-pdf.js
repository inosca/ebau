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
      const params = {};

      if (!this.args.field.document.rootForm.raw.meta["is-main-form"]) {
        params["form-slug"] = this.args.field.document.rootForm.slug;
      }

      if (this.args.field.question.raw.meta.template) {
        params.template = this.args.field.question.raw.meta.template;
      }

      const query = Object.entries(params)
        .map(([k, v]) => `${k}=${v}`)
        .join("&");

      const fullQuery = query ? `?${query}` : "";

      // generate document in CAMAC
      const response = yield this.fetch.fetch(
        `/api/v1/instances/${this.args.context.instanceId}/generate-pdf${fullQuery}`,
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
