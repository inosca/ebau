import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask, lastValue } from "ember-concurrency";
import { DateTime } from "luxon";

export default class StatisticsIndexController extends Controller {
  @service fetch;

  queryParams = ["from", "to"];

  @tracked from = "";
  @tracked to = "";

  get period() {
    return [this.from, this.to].join(",");
  }

  @lastValue("fetchInstancesSummary") instanceCount;
  @dropTask
  *fetchInstancesSummary() {
    const response = yield this.fetch.fetch(
      `/api/v1/stats/instances-summary?period=${this.period}`,
      {
        headers: { accept: "application/json" },
      }
    );

    return yield response.json();
  }

  @lastValue("fetchClaimsSummary") claimCount;
  @dropTask
  *fetchClaimsSummary() {
    const response = yield this.fetch.fetch(
      `/api/v1/stats/claims-summary?period=${this.period}`,
      {
        headers: { accept: "application/json" },
      }
    );

    return yield response.json();
  }

  @action
  setFilter(name, value) {
    const date = DateTime.fromJSDate(value);

    this[name] = date.isValid ? date.toISODate() : null;

    this.fetchInstancesSummary.perform();
    this.fetchClaimsSummary.perform();
  }
}
