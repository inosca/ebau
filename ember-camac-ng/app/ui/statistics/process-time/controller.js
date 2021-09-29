import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency-decorators";

export default class StatisticsProcessTimeController extends Controller {
  @service fetch;

  get averageProcessingTime() {
    const seconds = this.activationsSummary?.["avg-processing-time"];

    return Math.round(seconds / 60 / 60 / 24);
  }

  get deadlineQuota() {
    return this.activationsSummary?.["deadline-quota"];
  }

  @lastValue("fetchActivationsSummary") activationsSummary;
  @dropTask
  *fetchActivationsSummary() {
    const response = yield this.fetch.fetch(
      "/api/v1/stats/activations-summary",
      {
        headers: { accept: "application/json" },
      }
    );

    return yield response.json();
  }
}
