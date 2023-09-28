import { assert } from "@ember/debug";
import { inject as service } from "@ember/service";
import { getOwnConfig } from "@embroider/macros";
import { dropTask } from "ember-concurrency";
import DocumentValidityButtonComponent from "ember-ebau-core/components/document-validity-button";

export default class BeSubmitInstanceComponent extends DocumentValidityButtonComponent {
  @service intl;
  @service notification;
  @service router;
  @service fetch;
  @service session;

  validateOnEnter = true;
  showLoadingHint = true;
  showButtonHint = true;
  type = "submit";

  @dropTask
  *afterValidate() {
    // mark instance as submitted (optimistic) because after submitting, answer cannot be saved anymore
    this.args.field.answer.value =
      this.args.field.question.raw.multipleChoiceOptions.edges[0].node.slug;
    yield this.args.field.save.perform();

    try {
      const instanceId = this.args.context.instanceId;
      const action = this.args.field.question.raw.meta.action;

      assert("Field must have a meta property `action`", action);

      // submit instance in CAMAC
      const camacResponse = yield this.fetch.fetch(
        `/api/v1/instances/${instanceId}/${action}`,
        { method: "POST" },
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
        this.intl.t("be-submit-instance.failed-message", { reasons }),
      );
      // un-mark as submitted
      this.args.field.answer.value = null;
      yield this.args.field.save.perform();
    }
  }

  get buttonHintText() {
    if (getOwnConfig().application === "be" && this.session.isSupport) {
      return this.intl.t("be-submit-instance.button-hint-text", {
        htmlSafe: true,
      });
    }

    return null;
  }
}
