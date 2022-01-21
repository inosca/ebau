import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { dropTask, lastValue } from "ember-concurrency-decorators";

export default class StatisticsAvgCycleTimeController extends Controller {
  @service fetch;

  queryParams = ["procedure"];

  @tracked procedure = "";

  get procedures() {
    return [
      "PRELIM",
      "BAUBEWILLIGUNG",
      "GESAMT",
      "KLEIN",
      "GENERELL",
      "TEILBAUBEWILLIGUNG",
      "PROJEKTAENDERUNG",
      "BAUABSCHLAG_OHNE_WHST",
      "BAUABSCHLAG_MIT_WHST",
      "ABSCHREIBUNGSVERFUEGUNG",
      "BAUBEWILLIGUNGSFREI",
      "TEILWEISE_BAUBEWILLIGUNG_MIT_TEILWEISEM_BAUABSCHLAG_UND_TEILWEISER_WIEDERHERSTELLUNG",
    ];
  }

  @lastValue("fetchCycleTimes") cycleTimes;
  @dropTask
  *fetchCycleTimes() {
    const response = yield this.fetch.fetch(
      `/api/v1/stats/instances-cycle-times?procedure=${this.procedure}`,
      {
        headers: { accept: "application/json" },
      }
    );

    return yield response.json();
  }

  @action
  setProcedure(event) {
    event.preventDefault();
    this.procedure = event.target.value;
    this.fetchCycleTimes.perform();
  }
}
