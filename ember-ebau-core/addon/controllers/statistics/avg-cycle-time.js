import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

import decisionProceduresQuery from "ember-ebau-core/gql/queries/decision-procedures.graphql";

export default class StatisticsAvgCycleTimeController extends Controller {
  @service fetch;
  @service intl;

  @queryManager apollo;

  queryParams = ["procedure"];

  @tracked procedure = "";

  procedures = trackedTask(this, this.fetchProcedures, () => []);

  @dropTask
  *fetchProcedures() {
    const response = yield this.apollo.query(
      {
        query: decisionProceduresQuery,
      },
      "allQuestions.edges",
    );

    return [
      { slug: "", label: this.intl.t("statistics.procedures.all") },
      {
        slug: "preliminary-clarification",
        label: this.intl.t("statistics.procedures.preliminary-clarification"),
      },
      ...response[0].node.options.edges.map((edge) => edge.node),
    ];
  }

  @lastValue("fetchCycleTimes") cycleTimes;
  @dropTask
  *fetchCycleTimes() {
    const response = yield this.fetch.fetch(
      `/api/v1/stats/instances-cycle-times?procedure=${this.procedure}`,
      {
        headers: { accept: "application/json" },
      },
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
