import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { dropTask } from "ember-concurrency";
import UIkit from "uikit";

import config from "../../../config/environment";

export default class InstancesEditIndexController extends Controller {
  @service fetch;
  @service notification;
  @service intl;
  @service router;

  cases = useCalumaQuery(this, allCases, () => ({
    filter: [
      {
        metaValue: [{ key: "camac-instance-id", value: this.model }],
      },
    ],
  }));

  @controller("instances.edit") editController;

  get hasFeedbackSection() {
    return Boolean(config.APPLICATION.documents.feedbackSection);
  }

  get feedback() {
    return this.editController.feedback;
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

  get case() {
    return this.cases.value?.[0];
  }

  @dropTask
  *createModification() {
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
    try {
      yield UIkit.modal.confirm(this.intl.t("instances.deleteInstanceModal"), {
        labels: {
          ok: this.intl.t("global.ok"),
          cancel: this.intl.t("global.cancel"),
        },
      });
    } catch (error) {
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
