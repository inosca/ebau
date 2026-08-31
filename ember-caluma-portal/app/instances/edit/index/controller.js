import Controller, { inject as controller } from "@ember/controller";
import { service } from "@ember/service";
import { dropTask, task } from "ember-concurrency";
import mainConfig from "ember-ebau-core/config/main";
import { hasFeature } from "ember-ebau-core/helpers/has-feature";
import { isApplication } from "ember-ebau-core/helpers/is-application";
import { getAnswerDisplayValue } from "ember-ebau-core/utils/get-answer";
import { confirm } from "ember-uikit";

import config from "caluma-portal/config/environment";

export default class InstancesEditIndexController extends Controller {
  @service store;
  @service fetch;
  @service notification;
  @service intl;
  @service router;
  @service dms;

  @controller("instances.edit") editController;

  get isRejection() {
    return (
      parseInt(this.editController.instance?.get("instanceState.id")) ===
      config.APPLICATION.instanceStates.rejected
    );
  }

  get showSubmitTechnischeBewilligung() {
    return (
      isApplication("ur") &&
      parseInt(this.editController.instance?.get("instanceState.id")) ===
        config.APPLICATION.instanceStates.finished &&
      this.editController.instance?.calumaForm === "building-permit"
    );
  }

  get hasSpecialId() {
    return Boolean(mainConfig.answerSlugs.specialId);
  }

  get evenProjectNumber() {
    return this.editController?.case?.raw?.document
      ? getAnswerDisplayValue(
          this.editController.case.raw.document,
          mainConfig.answerSlugs.evenProjectNumber,
          false,
        )
      : undefined;
  }

  @dropTask
  *createModification() {
    if (
      hasFeature("modificationConfirm") &&
      !(yield confirm(this.intl.t("instances.modificationConfirm")))
    ) {
      return;
    }

    yield this.copy.perform(true);
  }

  @dropTask
  *createDemolitionPayment() {
    try {
      const response = yield this.fetch.fetch(`/api/v1/instances`, {
        method: "POST",
        body: JSON.stringify({
          data: {
            attributes: {
              "copy-source": this.editController.model,
              "copy-type": "demolition_payment",
            },
            type: "instances",
          },
        }),
      });
      const {
        data: {
          id: instanceId,
          attributes: { "caluma-form": calumaForm },
        },
      } = yield response.json();

      yield this.router.transitionTo(
        "instances.edit.form",
        instanceId,
        calumaForm,
      );
    } catch {
      this.notification.danger(this.intl.t("instances.demolitionPaymentError"));
    }
  }

  @dropTask
  *createNextPhase() {
    if (
      hasFeature("nextPhaseConfirm") &&
      !(yield confirm(this.intl.t("instances.nextPhaseConfirm")))
    ) {
      return;
    }

    yield this.nextPhase.perform(true);
  }

  @dropTask
  *createCopy() {
    yield this.copy.perform();
  }

  @dropTask
  *copy(isModification = false) {
    const response = yield this.fetch.fetch(`/api/v1/instances`, {
      method: "POST",
      body: JSON.stringify({
        data: {
          attributes: {
            "is-modification": isModification,
            "copy-source": this.editController.model,
            "copy-type": "full",
          },
          type: "instances",
        },
      }),
    });

    const { data } = yield response.json();

    yield this.router.transitionTo(
      "instances.edit.form",
      data.id,
      this.editController.instance.calumaForm,
    );
  }

  @dropTask
  *nextPhase() {
    const response = yield this.fetch.fetch(`/api/v1/instances`, {
      method: "POST",
      body: JSON.stringify({
        data: {
          attributes: {
            "copy-source": this.editController.model,
            "copy-type": "ebbw_next_phase",
          },
          type: "instances",
        },
      }),
    });
    const { data } = yield response.json();
    const newInstance = yield this.store.findRecord("instance", data.id);

    yield this.router.transitionTo(
      "instances.edit.form",
      data.id,
      newInstance.calumaForm,
    );
  }

  @dropTask
  *deleteInstance() {
    if (!(yield confirm(this.intl.t("instances.deleteInstanceModal")))) {
      return;
    }

    try {
      yield this.editController.instance.destroyRecord();
      this.notification.success(this.intl.t("instances.deleteInstanceSuccess"));
      yield this.router.transitionTo("instances");
    } catch {
      this.notification.danger(this.intl.t("instances.deleteInstanceError"));
    }
  }

  @dropTask
  *createNewFormExtensionPeriodOfValidity() {
    const response = yield this.fetch.fetch(`/api/v1/instances`, {
      method: "POST",
      body: JSON.stringify({
        data: {
          attributes: {
            "caluma-form": "verlaengerung-geltungsdauer",
            "copy-source": this.editController.model,
            "copy-type": "extend_validity",
          },
          type: "instances",
        },
      }),
    });

    const {
      data: { id: instanceId },
    } = yield response.json();

    yield this.router.transitionTo(
      "instances.edit.form",
      instanceId,
      "verlaengerung-geltungsdauer",
    );
  }

  @dropTask
  *downloadReceipt() {
    try {
      yield this.dms.generateReceipt(this.editController.instance);
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("dms.downloadError"));
    }
  }

  downloadFormAsPdf = task({ drop: true }, async () => {
    try {
      return await this.dms.generatePdf(this.editController.instance.id, {});
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("dms.downloadError"));
    }
  });

  @dropTask
  *createNewFormMessageBuildingServices() {
    const response = yield this.fetch.fetch(`/api/v1/instances`, {
      method: "POST",
      body: JSON.stringify({
        data: {
          attributes: {
            "caluma-form": "technische-bewilligung",
          },
          type: "instances",
        },
      }),
    });

    const {
      data: { id: instanceId },
    } = yield response.json();

    yield this.router.transitionTo(
      "instances.edit.form",
      instanceId,
      "technische-bewilligung",
    );
  }

  get withdrawalRequestDisabled() {
    return (
      hasFeature("withdrawal.light") &&
      this.editController.instance?.get("activeService.usesEchApi")
    );
  }

  get municipalityWebsite() {
    const url = this.editController.instance?.get("activeService.website");
    if (!url) {
      return null;
    }

    if (url.startsWith("https://") || url.startsWith("http://")) {
      return url;
    }

    return `https://${url}`;
  }

  @dropTask
  *withdrawInstance() {
    if (!(yield confirm(this.intl.t("instances.withdrawInstanceModal")))) {
      return;
    }

    try {
      yield this.fetch.fetch(`/api/v1/instances/${this.model}/withdraw`, {
        method: "POST",
      });

      if (hasFeature("withdrawal.light")) {
        this.notification.success(
          this.intl.t("instances.withdrawalRequestedSuccess"),
        );

        this.editController.refreshCase();
      } else {
        this.notification.success(
          this.intl.t("instances.withdrawInstanceSuccess"),
        );

        yield this.router.transitionTo("instances");
      }
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("instances.withdrawInstanceError"));
    }
  }
}
