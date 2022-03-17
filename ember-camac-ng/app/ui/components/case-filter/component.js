import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allForms } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { restartableTask, lastValue } from "ember-concurrency";

import caseFilters from "./filter-config";

import caseTableConfig from "camac-ng/config/case-table";
import getBuildingPermitQuestion from "camac-ng/gql/queries/get-building-permit-question.graphql";

export default class CaseFilterComponent extends Component {
  @queryManager apollo;

  caseFilters = caseFilters;

  @service store;
  @service intl;
  @service shoebox;

  @tracked _filter;
  @calumaQuery({ query: allForms }) formsQuery;

  constructor(...args) {
    super(...args);

    this._filter = {
      ...this.args.filter,
      ...this.storedFilters,
    };
  }

  get storedGroupFilters() {
    return JSON.parse(
      localStorage.getItem(this.shoebox.content.groupId) ?? JSON.stringify({})
    );
  }

  get storedFilters() {
    return this.storedGroupFilters[this.shoebox.content.userId] ?? {};
  }

  updateStoredFilters(value) {
    const shoeboxContent = this.shoebox.content;
    localStorage.setItem(
      shoeboxContent.groupId,
      JSON.stringify({
        ...this.storedGroupFilters,
        ...{ [shoeboxContent.userId]: value },
      })
    );
  }

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
        filter: [
          { isPublished: true },
          { isArchived: false },
          { orderBy: "NAME_ASC" },
          {
            metaValue: [{ key: "is_creatable", value: true }],
          },
        ],
      })
    ).allForms.edges.map((form) => form.node);
  }

  async responsibleServiceUsers() {
    const responsibleServices = await this.store.query("responsible-service", {
      service: this.shoebox.content.serviceId,
      include: "responsible-user",
    });
    const responsibleServiceUsers = responsibleServices.map(
      (responsibleService) => {
        const responsibleUser = responsibleService.responsibleUser;
        return {
          label: responsibleUser.get("fullName"),
          value: responsibleUser.get("id"),
        };
      }
    );
    return [
      ...responsibleServiceUsers,
      {
        label: this.intl.t("cases.filters.responsibleServiceUser-nobody"),
        value: "nobody",
      },
    ];
  }

  @lastValue("fetchFilterData") filterData;
  @restartableTask
  *fetchFilterData() {
    const optionQueries = {
      municipalities: async () => await this.store.findAll("location"),
      instanceStates: async () =>
        await this.store.query("instance-state", {
          instance_state_id: this.args.instanceStates,
        }),
      services: async () =>
        await this.store.query("service", {
          service_group_id: (
            caseTableConfig.externalServiceGroupIds || []
          ).join(","),
        }),
      servicesSZ: async () =>
        await this.store.query("public-service", {
          available_in_distribution: true,
        }),
      buildingPermitTypes: this.buildingPermitTypes.bind(this),
      caseStatusOptions: this.caseStatusOptions.bind(this),
      formOptions: this.formOptions.bind(this),
      responsibleServiceUsers: this.responsibleServiceUsers.bind(this),
      formsSZ: async () =>
        await this.store.query("form", {
          form_state: "1", // Published
          forms_all_versions: false,
        }),
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
    this.updateStoredFilters(this._filter);
  }

  @action resetFilter() {
    this._filter = {};
    this.args.onChange(this._filter);
    this.updateStoredFilters({});
  }

  get activeCaseFilters() {
    const activeCaseFilters =
      caseTableConfig.activeFilters[this.args.casesBackend] ?? [];

    if (Array.isArray(activeCaseFilters)) {
      return activeCaseFilters;
    }

    const role = this.shoebox.role;
    return activeCaseFilters[role] ?? activeCaseFilters.default ?? [];
  }
}
