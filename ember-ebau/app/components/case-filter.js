import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allForms } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { restartableTask, lastValue } from "ember-concurrency";

import caseFilters from "ebau/components/case-filter/filter-config";
import config from "ebau/config/environment";
import getBuildingPermitQuestion from "ebau/gql/queries/get-building-permit-question.graphql";

export default class CaseFilterComponent extends Component {
  @queryManager apollo;

  caseFilters = caseFilters;

  @service store;
  @service intl;

  @tracked _filter = {};
  @calumaQuery({ query: allForms }) formsQuery;

  async buildingPermitTypes() {
    return (
      await this.apollo.query(
        {
          query: getBuildingPermitQuestion,
        },
        "allQuestions.edges"
      )
    )
      .map((edge) => edge.node.options.edges)[0]
      ?.map((edge) => edge.node);
  }

  async caseStatusOptions() {
    return this.caseFilters.caseStatus.optionValues.map((option) => ({
      status: option,
      label: this.intl.t(`cases.status.${option}`),
    }));
  }

  async formOptions() {
    return (
      await this.formsQuery.fetch({
        order: [{ attribute: "NAME", direction: "ASC" }],
        filter: [
          { isPublished: true },
          { isArchived: false },
          {
            metaValue: [{ key: "is_creatable", value: true }],
          },
        ],
      })
    ).allForms.edges.map((form) => form.node);
  }

  @lastValue("fetchFilterData") filterData;
  @restartableTask
  *fetchFilterData() {
    const optionQueries = {
      municipalities: async () => await this.store.findAll("location"),
      instanceStates: async () => await this.store.findAll("instance-state"),
      services: async () =>
        await this.store.query("service", {
          service_group_id:
            config.APPLICATION.externalServiceGroupIds.join(","),
        }),
      buildingPermitTypes: this.buildingPermitTypes.bind(this),
      caseStatusOptions: this.caseStatusOptions.bind(this),
      formOptions: this.formOptions.bind(this),
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
