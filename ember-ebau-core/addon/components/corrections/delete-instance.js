import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

import { confirmTask } from "ember-ebau-core/decorators";

export default class CorrectionsDeleteInstanceComponent extends Component {
  @service fetch;
  @service intl;
  @service notification;
  @service ebauModules;
  @service router;

  @dropTask
  @confirmTask("corrections.delete.confirm")
  *deleteInstance() {
    try {
      yield this.fetch.fetch(`/api/v1/instances/${this.args.instance.id}`, {
        method: "DELETE",
      });

      this.notification.success(this.intl.t("corrections.delete.success"));
      this.router.transitionTo("index");
    } catch {
      this.notification.danger(this.intl.t("corrections.delete.error"));
    }
  }
}
