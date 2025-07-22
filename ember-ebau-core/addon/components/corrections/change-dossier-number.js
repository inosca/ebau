import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";
import { localCopy } from "tracked-toolbox";

import { confirmTask } from "ember-ebau-core/decorators";
import parseError from "ember-ebau-core/utils/parse-error";

export default class CorrectionsChangeDossierNumber extends Component {
  @service fetch;
  @service intl;
  @service notification;

  @localCopy("args.instance.ebauNumber") ebauNumber;

  @dropTask
  @confirmTask("corrections.ebau-number.confirm")
  *changeEbauNumber() {
    try {
      yield this.fetch.fetch(
        `/api/v1/instances/${this.args.instance.id}/set-ebau-number`,
        {
          method: "POST",
          body: JSON.stringify({
            data: {
              type: "instance-set-ebau-numbers",
              id: this.args.instanceId,
              attributes: {
                "ebau-number": this.ebauNumber,
              },
            },
          }),
        },
      );

      // sadly we need this to have current data on the whole page
      location.reload();
    } catch (error) {
      let text = this.intl.t("corrections.ebau-number.error");

      if (error.body?.errors) {
        text = parseError(error.body);
      }

      this.notification.danger(text);
    }
  }
}
