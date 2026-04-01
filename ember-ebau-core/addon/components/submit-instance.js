import { assert } from "@ember/debug";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { task } from "ember-concurrency";
import { confirm } from "ember-uikit";
import { trackedFunction } from "reactiveweb/function";

import { hasInstanceState } from "ember-ebau-core/abilities/instance";
import mainConfig from "ember-ebau-core/config/main";
import cleanObject from "ember-ebau-core/utils/clean-object";

const PREVENT_SUBMIT_MUNICIPALITY_RESPONSE_CODE = "municipality_not_allowed";

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

  get instanceId() {
    return this.args.context.instanceId;
  }

  get isAdditionalDemandChanges() {
    return (
      this.ebauModules.isPortal && this.args.context?.additionalDemandChanges
    );
  }

  get config() {
    const config = mainConfig.submitComponent;
    assert("Main config must contain `submitComponent` config", config);
    return config;
  }

  get action() {
    const action = this.args.field.question.raw.meta.action;
    assert("Question must have a meta property `action`", action);
    return this.isAdditionalDemandChanges
      ? "additional-demand-changes-submit"
      : action;
  }

  get requiredPermissions() {
    return this.permissions.fullyEnabled
      ? this.config.requiredPermissions?.[this.action]
      : null;
  }

  get buttonLabel() {
    if (this.isAdditionalDemandChanges) {
      return this.intl.t("cases.submit.additional-demand-changes.label");
    }

    return this.ebauModules.isPortal
      ? this.args.field.question.raw.label
      : this.intl.t("cases.submit.internal.label");
  }

  get buttonHintText() {
    const showHintText =
      this.config?.buttonHintEnabled?.(this.session) ?? false;

    return showHintText
      ? this.intl.t("cases.submit.hint-text", { htmlSafe: true })
      : null;
  }

  disabled = trackedFunction(this, async () => {
    if (!this.requiredPermissions) {
      // If the permissions module is not full enabled, we don't require any
      // permission and fully depend on the disabled state passed to the form
      // rendering.
      // In addition to that, we always disable it for the support role as they
      // should not be able to submit but the form is always editable.
      return this.args.disabled || this.session.isSupport;
    }

    // If the permissions module is enabled, we decouple the disabled state of
    // the button from the disabled state of the form. An instance may be
    // submittable while the form is not editable (e.g. in SG when it's locked
    // after the applicants confirmed the contents) and vice-versa (e.g. for
    // readonly and editor roles).
    const hasPermissions = await this.permissions.hasAll(
      this.instanceId,
      this.requiredPermissions,
    );

    return !hasPermissions;
  });

  submit = task({ drop: true }, async () => {
    // Show a confirm dialog if there is a translation configured for the
    // current action (currently BE only)
    const confirmKey = `cases.${this.action}.confirm`;
    if (
      this.intl.exists(confirmKey) &&
      !(await confirm(this.intl.t(confirmKey)))
    ) {
      return;
    }

    try {
      const instance = this.store.peekRecord("instance", this.instanceId);

      if (
        hasInstanceState(
          instance,
          mainConfig.correction?.instanceState ?? [],
        ) &&
        this.ebauModules.isPortal === false
      ) {
        // If we're in an active correction, we redirect to the corrections
        // module as the correction has to be finalized in there.
        return this.router.transitionTo("cases.detail.corrections");
      }

      // Mark instance as submitted (optimistic) because after submitting,
      // answer cannot be saved anymore
      this.args.field.answer.value =
        this.args.field.question.raw.multipleChoiceOptions?.edges[0]?.node.slug;
      await this.args.field.save.perform();

      // POST to submit endpoint
      const camacResponse = await this.fetch.fetch(
        `/api/v1/instances/${this.instanceId}/${this.action}`,
        { method: "POST", ignoreErrors: [400] },
      );

      if (!camacResponse.ok) {
        // If the backend returns a 400 bad response with a specific code, we
        // want to display that exact message instead of the generic one
        const { errors } = await camacResponse.json();
        const error = errors.find(
          (e) => e.code === PREVENT_SUBMIT_MUNICIPALITY_RESPONSE_CODE,
        );

        throw {
          errors: [
            new Error(
              error?.detail ?? this.intl.t("cases.submit.failed-camac"),
            ),
          ],
        };
      }

      if (this.config.export?.enabled(instance)) {
        // Export the form / signature PDF if enabled
        await this.exportPdf.perform();
      }

      // The success notification text may differ depending on the context
      // (additional demand, portal / internal)
      const successKey = this.isAdditionalDemandChanges
        ? "cases.submit.additional-demand-changes.success"
        : this.ebauModules.isPortal
          ? "cases.submit.success"
          : "cases.submit.internal.success";

      this.notification.success(this.intl.t(successKey));

      if (this.isAdditionalDemandChanges) {
        if (instance.additionalDemandChanges.length) {
          // If there is an additional demand linked, we redirect directly to
          // the detail view of that additional demand
          this.router.transitionTo(
            "instances.edit.additional-demand.detail",
            instance.additionalDemandChanges[0],
          );
        } else {
          // Otherwise we redirect to the additional demands overview
          this.router.transitionTo("instances.edit.additional-demand");
        }
      } else if (this.ebauModules.isPortal) {
        // In the portal, we redirect to the instance list
        this.router.transitionTo("instances.index");
      } else {
        // For paper / internal instances, we directly redirect to the submitted
        // instances work item list
        this.ebauModules.redirectToCaseWorkItems();
      }
    } catch (error) {
      console.error("Error during submission:", error);

      let reasons = error.errors
        ?.map((e) => e.message ?? e.detail)
        .join("<br>");

      // Prepend reasons with two linebreaks in order to generate spacing
      // between the general error message and the actual reasons.
      reasons = reasons ? `<br/><br/>${reasons}` : "";

      this.notification.danger(
        this.intl.t("cases.submit.failed-message", { reasons }),
      );

      // Un-mark as submitted
      this.args.field.answer.value = null;
      await this.args.field.save.perform();
    }
  });

  exportPdf = task({ drop: true }, async () => {
    try {
      const rootFormSlug = this.args.field.fieldset.document.rootForm.slug;
      const useCustomFormSlug =
        this.config.export?.customFormSlugs?.includes(rootFormSlug) ?? false;

      const lang = this.intl.primaryLocale.split("-")[0];

      await this.dms.generatePdf(
        this.instanceId,
        cleanObject({
          template: this.config.export?.templateName(lang),
          "form-slug": useCustomFormSlug ? rootFormSlug : null,
        }),
      );
    } catch {
      this.notification.danger(this.intl.t("dms.downloadError"));
    }
  });
}
