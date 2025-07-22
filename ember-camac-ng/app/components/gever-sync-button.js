import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { task } from "ember-concurrency";

export default class GeverSyncButtonComponent extends Component {
  @tracked dots = ".";
  @service fetch;
  @service intl;
  @service notification;

  sync = task(this, { drop: true }, async (event) => {
    event?.preventDefault?.();

    try {
      await this.fetch.fetch(
        `/api/v1/instances/${this.args.context.instanceId}/sync-gever`,
        {
          method: "POST",
        },
      );
      this.notification.success(this.intl.t("gever.success"));
    } catch ({ response }) {
      this.notification.danger(
        response?.statusText ?? this.intl.t("gever.error"),
      );
    }
  });
}
