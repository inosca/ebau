import { assert } from "@ember/debug";
import { computed } from "@ember/object";
import { next } from "@ember/runloop";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import InViewportComponent from "ember-caluma-portal/components/in-viewport/component";
import { task } from "ember-concurrency";
import { all } from "rsvp";

export default InViewportComponent.extend({
  intl: service(),
  notification: service(),
  router: service(),
  fetch: service(),

  apollo: queryManager(),

  onEnter() {
    next(this, () => this.validate.perform());
  },

  invalidFields: computed(
    "field.document.fields.@each.{optional,hidden,isInvalid}",
    function () {
      return this.field.document.fields.filter(
        (field) => !field.hidden && !field.optional && field.isInvalid
      );
    }
  ),

  validate: task(function* () {
    yield all(
      this.field.document.fields.map((field) => field.validate.perform())
    );
  }).restartable(),

  buttonDisabled: computed(
    "disabled",
    "validate.{performCount,isRunning}",
    "invalidFields.length",
    function () {
      return (
        this.disabled ||
        this.validate.performCount === 0 ||
        this.validate.isRunning ||
        this.invalidFields.length > 0
      );
    }
  ),

  submit: task(function* () {
    // mark instance as submitted (optimistic) because after submitting, answer cannot be saved anymore
    this.field.set(
      "answer.value",
      this.field.get(
        "question.multipleChoiceOptions.edges.firstObject.node.slug"
      )
    );
    yield this.field.save.perform();

    try {
      const instanceId = this.get("context.instanceId");
      const action = this.get("field.question.meta.action");

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
      this.field.set("answer.value", null);
      yield this.field.save.perform();
    }
  }).drop(),
});
