import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency-decorators";

export default class TaskFormButtonComponent extends Component {
  @service notifications;
  @service intl;
  @service fetch;

  @queryManager apollo;

  @dropTask
  *completeAssignEbauNumber(validateFn) {
    if (!(yield validateFn())) return;

    try {
      const ebauNumber = this.args.field.document.findAnswer(
        "bestehende-ebau-nummer"
      );

      yield this.fetch.fetch(
        `/api/v1/instances/${this.args.context.instanceId}/set-ebau-number`,
        {
          method: "POST",
          body: JSON.stringify({
            data: {
              type: "instance-set-ebau-numbers",
              id: this.args.context.instanceId,
              attributes: {
                "ebau-number": ebauNumber ?? "",
              },
            },
          }),
        }
      );

      window.location.replace(
        `/index/redirect-to-instance-resource/instance-id/${this.args.context.instanceId}`
      );
    } catch (error) {
      this.notifications.error(this.intl.t("ebauNumber.completeInvalid"));
    }
  }
}
