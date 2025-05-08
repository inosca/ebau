import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

import { confirmTask } from "ember-ebau-core/decorators";

export default class CorrectionsArchiveInstance extends Component {
  @service fetch;
  @service notification;
  @service intl;

  @dropTask
  @confirmTask("corrections.archive.confirm")
  *archive() {
    try {
      yield this.fetch.fetch(
        `/api/v1/instances/${this.args.instance.id}/archive`,
        {
          method: "POST",
        },
      );

      // sadly we need this to have current data on the whole page
      location.assign(
        `/index/redirect-to-instance-resource/instance-id/${this.args.instance.id}`,
      );
    } catch {
      this.notification.danger(this.intl.t("corrections.archive.error"));
    }
  }
}
