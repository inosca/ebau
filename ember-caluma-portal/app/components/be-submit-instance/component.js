import { assert } from "@ember/debug";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { queryManager } from "ember-apollo-client";
import { dropTask, restartableTask } from "ember-concurrency-decorators";
import { all } from "rsvp";

export default class BeSubmitInstanceComponent extends Component {
  @service intl;
  @service notification;
  @service router;
  @service fetch;

  @queryManager apollo;

  @computed(
    "args.field.document.fields",
    "args.field.document.fields.@each.{hidden,isInvalid,optional}"
  )
  get invalidFields() {
    return this.args.field.document.fields.filter(
      (field) => !field.hidden && !field.optional && field.isInvalid
    );
  }

  @restartableTask
  *validate() {
    yield all(
      this.args.field.document.fields.map((field) => field.validate.perform())
    );
  }

  @computed(
    "disabled",
    "validate.{performCount,isRunning}",
    "invalidFields.length"
  )
  get buttonDisabled() {
    return (
      this.disabled ||
      this.validate.performCount === 0 ||
      this.validate.isRunning ||
      this.invalidFields.length > 0
    );
  }

  @dropTask
  *submit() {
    // mark instance as submitted (optimistic) because after submitting, answer cannot be saved anymore
    this.args.field.answer.value =
      this.args.field.question.multipleChoiceOptions.edges[0].node.slug;
    yield this.args.field.save.perform();

    try {
      const instanceId = this.args.context.instanceId;
      const action = this.args.field.question.meta.action;

      assert("Field must have a meta property `action`", action);

      // submit instance in CAMAC
      const camacResponse = yield this.fetch.fetch(
        `/api/v1/instances/${instanceId}/${action}`,
        { method: "POST" }
      );

      if (!camacResponse.ok) {
        throw {
          errors: [new Error(this.intl.t("be-submit-instance.failed-camac"))],
        };
      }

      this.notification.success(this.intl.t("be-submit-instance.success"));

      yield this.router.transitionTo("instances.index");
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      const reasons = (e.errors || []).map((e) => e.message).join("<br>\n");
      this.notification.danger(
        this.intl.t("be-submit-instance.failed-message", { reasons })
      );
      // un-mark as submitted
      this.args.field.answer.value = null;
      yield this.args.field.save.perform();
    }
  }
}
