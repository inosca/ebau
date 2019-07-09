import InViewportComponent from "ember-caluma-portal/components/in-viewport/component";
import { task, timeout } from "ember-concurrency";
import { inject as service } from "@ember/service";
import { computed } from "@ember/object";
import { all } from "rsvp";
import { next } from "@ember/runloop";

const INSTANCE_STATE_SUBMITTED = 20000;

export default InViewportComponent.extend({
  notification: service(),
  apollo: service(),
  ajax: service(),
  router: service(),
  fetch: service(),

  onEnter() {
    next(this, () => this.validate.perform());
  },

  invalidFields: computed(
    "field.document.fields.@each.{optional,hidden,isInvalid}",
    function() {
      return this.field.document.fields.filter(
        field => !field.hidden && !field.optional && field.isInvalid
      );
    }
  ),

  validate: task(function*() {
    yield all(
      this.field.document.fields.map(field => field.validate.perform())
    );
  }).restartable(),

  buttonDisabled: computed(
    "disabled",
    "validate.{performCount,isRunning}",
    "invalidFields.length",
    function() {
      return (
        this.disabled ||
        this.validate.performCount === 0 ||
        this.validate.isRunning ||
        this.invalidFields.length > 0
      );
    }
  ),

  submit: task(function*() {
    // mark instance as submitted (optimistic) because after submitting, answer cannot be saved anymore
    this.field.set(
      "answer.value",
      this.field.get(
        "question.multipleChoiceOptions.edges.firstObject.node.slug"
      )
    );
    yield this.field.save.perform();

    try {
      const caseId = this.get("context.caseId");
      const instanceId = this.get("context.instanceId");

      // simulate waiting, until actual backend implementation has landed
      yield timeout(8000 + Math.random() * 4000);

      // submit instance in CAMAC
      const camacResponse = yield this.fetch.fetch(
        `/api/v1/instances/${instanceId}`,
        {
          method: "PATCH",
          body: JSON.stringify({
            data: {
              type: "instances",
              id: instanceId,
              attributes: {
                "caluma-case-id": caseId
              },
              relationships: {
                "instance-state": {
                  data: {
                    id: INSTANCE_STATE_SUBMITTED,
                    type: "instance-states"
                  }
                }
              }
            }
          })
        }
      );

      if (!camacResponse.ok) {
        throw new Error("NG API call failed");
      }

      this.notification.success("Das Gesuch wurde erfolgreich eingereicht");

      yield this.router.transitionTo("instances");
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      const reasons = (e.errors || []).map(e => e.message).join("<br>\n");
      this.notification.danger(
        `Hoppla, etwas ist schief gelaufen. Bitte überprüfen Sie Ihre Eingabedaten nochmals. ${reasons}`
      );
      // un-mark as submitted
      this.field.set("answer.value", null);
      yield this.field.save.perform();
    }
  }).drop()
});
