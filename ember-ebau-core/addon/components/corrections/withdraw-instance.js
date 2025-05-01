import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

import { confirmTask } from "ember-ebau-core/decorators";

export default class CorrectionsWithdrawInstanceComponent extends Component {
  @service fetch;
  @service intl;
  @service notification;
  @service ebauModules;

  @dropTask
  @confirmTask("corrections.withdraw.confirm")
  *withdrawInstance() {
    try {
      yield this.fetch.fetch(
        `/api/v1/instances/${this.args.instance.id}/withdraw`,
        {
          method: "POST",
        },
      );

      this.notification.success(this.intl.t("corrections.withdraw.success"));

      yield this.ebauModules.redirectToWorkItems();
    } catch {
      this.notification.danger(this.intl.t("corrections.withdraw.error"));
    }
  }
}
