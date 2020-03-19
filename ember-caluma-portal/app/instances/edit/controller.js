import Controller from "@ember/controller";
import { computed } from "@ember/object";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";
import QueryParams from "ember-parachute";

const FEEDBACK_ATTACHMENT_SECTION = 3;

export default class InstancesEditController extends Controller.extend(
  new QueryParams().Mixin
) {
  @service fetch;
  @service can;
  @service session;

  @queryManager apollo;

  setup() {
    this.instanceTask.perform();
    this.feedbackTask.perform();
  }

  reset() {
    this.instanceTask.cancelAll({ resetState: true });
    this.feedbackTask.cancelAll({ resetState: true });

    this.resetQueryParams();
  }

  @computed
  get embedded() {
    return window !== window.top;
  }

  @lastValue("instanceTask") instance;
  @dropTask
  *instanceTask() {
    const instance = yield this.store.findRecord("instance", this.model, {
      include: [
        "instance_state",
        "involved_applicants",
        "involved_applicants.invitee",
        "active_service"
      ].join(",")
    });

    yield instance.getDocuments.perform();

    return instance;
  }

  @lastValue("feedbackTask") feedback;
  @dropTask
  *feedbackTask() {
    return yield this.store.query("attachment", {
      instance: this.model,
      attachment_sections: FEEDBACK_ATTACHMENT_SECTION,
      include: "attachment_sections"
    });
  }
}
