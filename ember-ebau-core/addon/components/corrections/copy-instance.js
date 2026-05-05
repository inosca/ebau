import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

import { confirmTask } from "ember-ebau-core/decorators";

export default class CorrectionsCopyInstance extends Component {
  @service ebauModules;
  @service notification;
  @service fetch;
  @service intl;

  get isVisible() {
    return this.ebauModules.isSupportRole;
  }

  @dropTask
  @confirmTask("corrections.copy.confirm")
  *copyInstance() {
    try {
      const response = yield this.fetch.fetch(
        `/api/v1/instances/${this.args.instance.id}/copy`,
        { method: "POST" },
      );

      const result = yield response.json();
      const newInstanceId = result.data.id;

      this.ebauModules.redirectToInstance(newInstanceId);
    } catch {
      this.notification.danger(this.intl.t("corrections.copy.error"));
    }
  }
}
