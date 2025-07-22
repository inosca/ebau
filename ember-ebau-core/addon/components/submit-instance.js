import { assert } from "@ember/debug";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { dropTask } from "ember-concurrency";

import { hasInstanceState } from "ember-ebau-core/abilities/instance";
import featuresConfig from "ember-ebau-core/config/features";
import mainConfig from "ember-ebau-core/config/main";

export default class SubmitInstanceComponent extends Component {
  @service ebauModules;
  @service intl;
  @service notification;
  @service router;
  @service fetch;
  @service store;
  @service dms;
  @service session;
  @service permissions;

  validateOnEnter = true;
  showLoadingHint = true;
  config;
  type = "submit";

  constructor(...args) {
    super(...args);
    this.config = featuresConfig?.features?.submitComponent;
    if (!this.config) {
      console.error("No submitComponent config found!");
    }
  }

  get requiredPermissions() {
    return this.permissions.fullyEnabled
      ? this.config?.requiredPermissions
      : null;
  }

  get buttonLabel() {
    return this.ebauModules.isPortal
      ? this.args.field.question.raw.label
      : this.intl.t("cases.submit.internal.label");
  }

  @dropTask
  *afterValidate() {
    // mark instance as submitted (optimistic) because after submitting, answer cannot be saved anymore
    this.args.field.answer.value =
      this.args.field.question.raw.multipleChoiceOptions?.edges[0]?.node.slug;
    yield this.args.field.save.perform();

    try {
      const instanceId = this.args.context.instanceId;
      const action = this.args.field.question.raw.meta.action;

      assert("Field must have a meta property `action`", action);
      const instance = yield this.store.peekRecord("instance", instanceId);

      if (
        hasInstanceState(
          instance,
          mainConfig.correction?.instanceState ?? [],
        ) &&
        this.ebauModules.isPortal === false
      ) {
        yield this.router.transitionTo("cases.detail.corrections");
        return;
      }

      // submit instance in CAMAC
      const camacResponse = yield this.fetch.fetch(
        `/api/v1/instances/${instanceId}/${action}`,
        { method: "POST" },
      );

      if (!camacResponse.ok) {
        throw {
          errors: [new Error(this.intl.t("cases.submit.failed-camac"))],
        };
      }

      if (this.config?.export?.enabled(instance)) {
        yield this.export.perform();
      }

      if (this.ebauModules.isPortal) {
        this.notification.success(this.intl.t("cases.submit.success"));
        yield this.router.transitionTo("instances.index");
      } else {
        this.notification.success(this.intl.t("cases.submit.internal.success"));
        this.ebauModules.redirectToCaseWorkItems();
      }
    } catch (e) {
      console.error("Error during submission:", e);
      const reasons = (e.errors || []).map((e) => e.message).join("<br>\n");
      this.notification.danger(
        this.intl.t("cases.submit.failed-message", { reasons }),
      );
      // un-mark as submitted
      this.args.field.answer.value = null;
      yield this.args.field.save.perform();
    }
  }

  @dropTask
  *export() {
    try {
      yield this.dms.generatePdf(this.args.context.instanceId, {
        template: this.config?.export?.templateName(
          this.intl.primaryLocale.split("-")[0],
        ),
      });
    } catch {
      this.notification.danger(this.intl.t("dms.downloadError"));
    }
  }

  get buttonHintText() {
    return this.config?.buttonHintEnabled &&
      this.config?.buttonHintEnabled(this.session)
      ? this.intl.t("cases.submit.hint-text", { htmlSafe: true })
      : null;
  }
}
