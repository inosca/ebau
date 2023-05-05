import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import { dropTask } from "ember-concurrency";
import { confirm } from "ember-uikit";

import config from "caluma-portal/config/environment";

export default class InstancesEditIndexController extends Controller {
  @service fetch;
  @service notification;
  @service intl;
  @service router;

  @controller("instances.edit") editController;

  get hasFeedbackSection() {
    return Boolean(config.APPLICATION.documents.feedbackSections);
  }

  get feedback() {
    return this.editController.feedback;
  }

  get case() {
    return this.editController.case;
  }

  get decision() {
    return this.editController.decision;
  }

  get instance() {
    return this.editController.instance;
  }

  get isRejection() {
    return (
      parseInt(this.instance.value?.get("instanceState.id")) ===
      config.APPLICATION.instanceStates.rejected
    );
  }

  get showSubmitTechnischeBewilligung() {
    return (
      config.APPLICATION.name === "ur" &&
      parseInt(this.instance.value?.get("instanceState.id")) ===
        config.APPLICATION.instanceStates.finished &&
      this.instance.value?.mainForm.slug === "building-permit"
    );
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
            "copy-source": this.model,
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
      this.instance.value.calumaForm
    );
  }

  @dropTask
  *deleteInstance() {
    if (!(yield confirm(this.intl.t("instances.deleteInstanceModal")))) {
      return;
    }

    try {
      yield this.instance.value.destroyRecord();
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
            "extend-validity-for": this.model,
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
      "verlaengerung-geltungsdauer"
    );
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
      "technische-bewilligung"
    );
  }
}
