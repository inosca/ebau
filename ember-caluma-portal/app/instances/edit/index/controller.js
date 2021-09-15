import Controller, { inject as controller } from "@ember/controller";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";
import UIkit from "uikit";

import config from "../../../config/environment";

export default class InstancesEditIndexController extends Controller {
  @service fetch;
  @service notification;
  @service intl;

  @calumaQuery({ query: allCases }) cases;

  @controller("instances.edit") editController;
  @reads("editController.hasFeedbackSection") hasFeedbackSection;
  @reads("editController.feedbackTask.isRunning") feedbackLoading;
  @reads("editController.decisionTask.isRunning") decisionLoading;
  @reads("editController.feedback") feedback;
  @reads("editController.decision") decision;
  @reads("editController.instance") instance;

  get isRejection() {
    return (
      parseInt(this.get("instance.instanceState.id")) ===
      config.APPLICATION.instanceStates.rejected
    );
  }

  get case() {
    return this.cases.value?.[0];
  }

  @dropTask
  *fetchCase() {
    yield this.cases.fetch({
      filter: [
        {
          metaValue: [{ key: "camac-instance-id", value: this.model }],
        },
      ],
    });
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

    yield this.transitionToRoute(
      "instances.edit.form",
      data.id,
      this.instance.calumaForm
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
      yield this.instance.destroyRecord();
      this.notification.success(this.intl.t("instances.deleteInstanceSuccess"));
      yield this.transitionToRoute("instances");
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
            "extend-validity-for": this.instance.id,
          },
          type: "instances",
        },
      }),
    });

    const {
      data: { id: instanceId },
    } = yield response.json();

    yield this.transitionToRoute(
      "instances.edit.form",
      instanceId,
      "verlaengerung-geltungsdauer"
    );
  }
}
