import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

export default class BeDownloadPdfComponent extends Component {
  @service notification;
  @service intl;
  @service fetch;
  @service session;
  @service dms;

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

      yield this.dms.generatePdf(this.args.context.instanceId, params);
    } catch (error) {
      this.notification.danger(this.intl.t("dms.downloadError"));
    }
  }
}
