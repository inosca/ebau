import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { macroCondition, getOwnConfig } from "@embroider/macros";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allCases } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

import config from "caluma-portal/config/environment";

export default class InstancesEditController extends Controller {
  @service store;

  @queryManager apollo;

  instance = trackedTask(this, this.fetchInstance, () => [this.model]);
  feedback = trackedTask(this, this.fetchFeedbackAttachments, () => [
    this.model,
  ]);
  cases = useCalumaQuery(this, allCases, () => ({
    filter: [
      {
        metaValue: [{ key: "camac-instance-id", value: this.model }],
      },
    ],
  }));

  get case() {
    return this.cases.value?.[0];
  }

  decision = trackedTask(this, this.fetchDecisionAttachments, () => [
    this.model,
  ]);

  @dropTask
  *fetchInstance() {
    yield Promise.resolve();

    const instance = yield this.store.findRecord("instance", this.model, {
      include: [
        "instance_state",
        "involved_applicants",
        "involved_applicants.invitee",
        "active_service",
      ].join(","),
      reload: true,
    });

    yield instance.getMainForm.perform();

    return instance;
  }

  @dropTask
  *fetchFeedbackAttachments() {
    if (!config.APPLICATION.documents.feedbackSections) {
      return [];
    }

    if (macroCondition(getOwnConfig().documentBackend === "camac")) {
      yield Promise.resolve();

      return yield this.store.query("attachment", {
        instance: this.model,
        attachment_sections:
          config.APPLICATION.documents.feedbackSections.join(","),
        include: "attachment_sections",
      });
    }
  }

  @dropTask
  *fetchDecisionAttachments() {
    yield Promise.resolve();
    if (macroCondition(getOwnConfig().documentBackend === "camac")) {
      return yield this.store.query("attachment", {
        instance: this.model,
        context: JSON.stringify({
          key: "isDecision",
          value: true,
        }),
        include: "attachment_sections",
      });
    }
    return [];
  }
}
