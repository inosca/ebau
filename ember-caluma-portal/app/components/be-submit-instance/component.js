import InViewportComponent from "ember-caluma-portal/components/in-viewport/component";
import { task, timeout } from "ember-concurrency";
import { inject as service } from "@ember/service";
import { computed } from "@ember/object";
import { all } from "rsvp";
import { next } from "@ember/runloop";
import config from "ember-caluma-portal/config/environment";
import { assert } from "@ember/debug";
import { queryManager } from "ember-apollo-client";
import slugify from "slugify";

const { environment } = config;

export default InViewportComponent.extend({
  intl: service(),
  notification: service(),
  router: service(),
  fetch: service(),
  documentExport: service(),

  apollo: queryManager(),

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
      const instanceId = this.get("context.instanceId");
      const action = this.get("field.question.meta.action");

      assert("Field must have a meta property `action`", action);

      // simulate waiting, until actual backend implementation has landed
      if (environment === "production") {
        yield timeout(8000 + Math.random() * 4000);
      }

      // submit instance in CAMAC
      const camacResponse = yield this.fetch.fetch(
        `/api/v1/instances/${instanceId}/${action}`,
        { method: "POST" }
      );

      if (!camacResponse.ok) {
        throw {
          errors: [new Error(this.intl.t("be-submit-instance.failed-camac"))]
        };
      }

      // Try to save/archive a document export as attachment.
      try {
        // Generate the PDF and prepare a filename.
        const blob = yield this.documentExport.merge(
          instanceId,
          this.field.document
        );
        const formName = this.field.document.rootForm.name;
        const fileName = slugify(`${instanceId}-${formName}.pdf`.toLowerCase());

        // Prepare the request data.
        const formData = new FormData();
        formData.append("instance", instanceId);
        formData.append("attachment_sections", "1");
        formData.append("path", blob, fileName);

        // Send the export to the backend.
        // The Content-Type must be `undefined` as we need multipart with
        // the correct delimiter the browser sets automatically when missing.
        const response = yield this.fetch.fetch("/api/v1/attachments", {
          method: "post",
          body: formData,
          headers: { "content-type": undefined }
        });

        if (!response.ok) {
          const {
            errors: [{ detail: error }]
          } = yield response.json();
          throw new Error(error);
        }
      } catch (error) {
        throw {
          errors: [new Error(this.intl.t("be-submit-instance.failed-archive"))]
        };
      }

      this.notification.success(this.intl.t("be-submit-instance.success"));

      yield this.router.transitionTo("instances");
    } catch (e) {
      // eslint-disable-next-line no-console
      console.error(e);
      const reasons = (e.errors || []).map(e => e.message).join("<br>\n");
      this.notification.danger(
        this.intl.t("be-submit-instance.failed-message", { reasons })
      );
      // un-mark as submitted
      this.field.set("answer.value", null);
      yield this.field.save.perform();
    }
  }).drop()
});
