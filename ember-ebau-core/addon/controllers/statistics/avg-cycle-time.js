import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";
import { trackedTask } from "reactiveweb/ember-concurrency";
import { trackedFunction } from "reactiveweb/function";

import decisionProceduresQuery from "ember-ebau-core/gql/queries/decision-procedures.graphql";
import rootFormsQuery from "ember-ebau-core/gql/queries/root-forms.graphql";
import {
  getRecursiveSources,
  groupFormsByCategories,
} from "ember-ebau-core/utils/form-filters";

export default class StatisticsAvgCycleTimeController extends Controller {
  @service fetch;
  @service intl;

  @queryManager apollo;

  queryParams = ["procedure", "form"];

  @tracked procedure = "";
  @tracked form = "";

  procedures = trackedTask(this, this.fetchProcedures, () => []);

  forms = trackedFunction(this, async () => {
    const categories = [
      "preliminary-clarification",
      "building-permit",
      "special-procedure",
      "others",
    ];

    const rawForms = await this.apollo.query(
      { query: rootFormsQuery },
      "allForms.edges",
    );

    const forms = rawForms
      .filter((edge) => edge.node.isPublished)
      .map((edge) => ({
        name: edge.node.name,
        value: [
          edge.node.slug,
          ...getRecursiveSources(edge.node, rawForms),
        ].join(","),
        category: edge.node.meta.category || "others",
        order: edge.node.meta.order,
      }));

    return groupFormsByCategories(forms, categories, this.intl);
  });

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
      ...response[0].node.options.edges.map((edge) => edge.node),
    ];
  }

  @lastValue("fetchCycleTimes") cycleTimes;
  @dropTask
  *fetchCycleTimes() {
    const response = yield this.fetch.fetch(
      `/api/v1/stats/instances-cycle-times?procedure=${this.procedure}&form=${this.form}`,
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

  @action
  setForm(event) {
    event.preventDefault();
    const value = event.target.value;
    this.form = value === "all" ? "" : value;
    this.fetchCycleTimes.perform();
  }
}
