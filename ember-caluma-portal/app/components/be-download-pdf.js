import { service } from "@ember/service";
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

      const isMainForm =
        this.args.field.document.rootForm.raw.meta["is-main-form"] ?? false;
      const forAdditionalDemand =
        this.args.field.question.raw.meta.forAdditionalDemand ?? false;
      const template = this.args.field.question.raw.meta.template ?? null;

      if (!isMainForm && !forAdditionalDemand) {
        params["form-slug"] = this.args.field.document.rootForm.slug;
      }

      if (template) {
        params.template = template;
      }

      if (forAdditionalDemand) {
        params["for-additional-demand"] = this.args.field.document.uuid;
      }

      yield this.dms.generatePdf(this.args.context.instanceId, params);
    } catch (error) {
      this.notification.danger(this.intl.t("dms.downloadError"));
    }
  }
}
