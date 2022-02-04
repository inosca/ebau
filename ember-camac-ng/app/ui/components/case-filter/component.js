import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allForms } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { restartableTask, lastValue } from "ember-concurrency";

import caseFilters from "./filter-config";

import config from "camac-ng/config/environment";
import getBuildingPermitQuestion from "camac-ng/gql/queries/get-building-permit-question.graphql";

const externalServiceGroupIds = [
  "21",
  "70",
  "2",
  "65",
  "66",
  "62",
  "61",
  "63",
  "64",
  "41",
  "71",
];

export default class CaseFilterComponent extends Component {
  @queryManager apollo;

  caseFilters = caseFilters;

  @service store;
  @service intl;

  @tracked _filter = {};
  @calumaQuery({ query: allForms }) formsQuery;

  @lastValue("fetchFilterData") filterData;
  @restartableTask
  *fetchFilterData() {
    const optionQueries = {
      municipalities: async () => await this.store.findAll("location"),
      instanceStates: async () => await this.store.findAll("instance-state"),
      services: async () =>
        await this.store.query("service", {
          service_group_id: externalServiceGroupIds.join(","),
        }),
      buildingPermitTypes: async () =>
        (
          await this.apollo.query(
            {
              query: getBuildingPermitQuestion,
            },
            "allQuestions.edges"
          )
        )
          .map((edge) => edge.node.options.edges)[0]
          ?.map((edge) => edge.node),
      caseStatusOptions: () =>
        this.caseFilters.caseStatus.optionValues.map((option) => ({
          status: option,
          label: this.intl.t(`cases.status.${option}`),
        })),
      formOptions: async () =>
        (
          await this.formsQuery.fetch({
            filter: [
              { isPublished: true },
              { isArchived: false },
              { orderBy: "NAME_ASC" },
              {
                metaValue: [{ key: "is_creatable", value: true }],
              },
            ],
          })
        ).allForms.edges.map((form) => form.node),
    };

    const options = yield Promise.all(
      Object.entries(optionQueries)
        .filter(([key]) =>
          this.activeCaseFilters
            .map((filter) => this.caseFilters[filter].options)
            .includes(key)
        )
        .map(async ([key, fn]) => [key, await fn()])
    );

    return options.reduce(
      (obj, [key, value]) => ({ ...obj, [key]: value }),
      {}
    );
  }

  @action updateFilter(field, event) {
    // The || null is so queryParams with value "" are not put into the url
    this._filter = {
      ...this.args.filter,
      ...this._filter,
      [field]: event?.target?.value || null,
    };
  }

  @action applyFilter(event) {
    event.preventDefault();
    this.args.onChange(this._filter);
  }

  @action resetFilter() {
    this._filter = {};
    this.args.onChange(this._filter);
  }

  get activeCaseFilters() {
    return config.APPLICATION.activeCaseFilters ?? [];
  }
}
