import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import { dropTask } from "ember-concurrency";
import mainConfig from "ember-ebau-core/config/main";
import { confirm } from "ember-uikit";

import config from "caluma-portal/config/environment";

export default class InstancesEditIndexController extends Controller {
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
      config.APPLICATION.name === "ur" &&
      parseInt(this.editController.instance?.get("instanceState.id")) ===
        config.APPLICATION.instanceStates.finished &&
      this.editController.instance?.calumaForm === "building-permit"
    );
  }

  get hasSpecialId() {
    return Boolean(mainConfig.answerSlugs.specialId);
  }

  @dropTask
  *createModification() {
    if (macroCondition(getOwnConfig().enableModificationConfirm)) {
      if (!(yield confirm(this.intl.t("instances.modificationConfirm")))) {
        return;
      }
    }

    yield this.copy.perform(true);
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
            "copy-source": this.editController.model,
            "is-modification": isModification,
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
  *deleteInstance() {
    if (!(yield confirm(this.intl.t("instances.deleteInstanceModal")))) {
      return;
    }

    try {
      yield this.editController.instance.destroyRecord();
      this.notification.success(this.intl.t("instances.deleteInstanceSuccess"));
      yield this.router.transitionTo("instances");
    } catch (error) {
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
            "extend-validity-for": this.editController.model,
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
      yield this.dms.generatePdf(this.editController.instance.id, {
        template: "eingabequittung",
      });
    } catch (e) {
      console.error(e);
      this.notification.danger(this.intl.t("dms.downloadError"));
    }
  }

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

  @dropTask
  *withdrawInstance() {
    if (!(yield confirm(this.intl.t("instances.withdrawInstanceModal")))) {
      return;
    }

    try {
      yield this.fetch.fetch(`/api/v1/instances/${this.model}/withdraw`, {
        method: "POST",
      });

      this.notification.success(
        this.intl.t("instances.withdrawInstanceSuccess"),
      );

      yield this.router.transitionTo("instances");
    } catch (error) {
      this.notification.danger(this.intl.t("instances.withdrawInstanceError"));
    }
  }
}
