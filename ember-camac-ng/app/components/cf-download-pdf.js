import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

export default class CfDownloadComponent extends Component {
  @service notification;
  @service intl;
  @service fetch;
  @service dms;

  @dropTask
  *export() {
    try {
      const params = {};
      if (this.args.field.document.rootForm.meta["is-main-form"]) {
        params["form-slug"] = this.field?.document.rootForm.slug;
      }
      yield this.dms.generatePdf(this.args.context.instanceId, params);
    } catch (error) {
      console.error(error);
      this.notification.danger(this.intl.t("form.downloadError"));
    }
  }
}
