import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

export default class StatisticsProcessTimeController extends Controller {
  @service fetch;

  get averageProcessingTime() {
    const seconds = this.inquiriesSummary.value?.["avg-processing-time"];

    return Math.round(seconds / 60 / 60 / 24);
  }

  get deadlineQuota() {
    return this.inquiriesSummary.value?.["deadline-quota"];
  }

  inquiriesSummary = trackedTask(this, this.fetchInquiriesSummary, () => []);

  @dropTask
  *fetchInquiriesSummary() {
    const response = yield this.fetch.fetch("/api/v1/stats/inquiries-summary", {
      headers: { accept: "application/json" },
    });

    return yield response.json();
  }
}
