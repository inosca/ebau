import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allForms } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { findAll, query } from "ember-data-resources";
import { trackedFunction } from "ember-resources";
import { cached } from "tracked-toolbox";

import caseFilters from "./filter-config";

import caseTableConfig from "camac-ng/config/case-table";
import getBuildingPermitQuestion from "camac-ng/gql/queries/get-building-permit-question.graphql";

export default class CaseFilterComponent extends Component {
  @queryManager apollo;

  @service store;
  @service intl;
  @service shoebox;

  @tracked _filter;

  constructor(...args) {
    super(...args);

    this._filter = {
      ...this.args.filter,
      ...this.storedFilters,
    };

    this.args.onChange(this._filter);
  }

  formOptions = useCalumaQuery(this, allForms, () => ({
    filter: [
      { isPublished: true },
      { isArchived: false },
      { orderBy: "NAME_ASC" },
      { metaValue: [{ key: "is_creatable", value: true }] },
    ],
  }));

  instanceStates = query(this, "instance-state", () => ({
    instance_state_id: this.args.instanceStates,
  }));

  services = query(this, "service", () => ({
    service_group_id: (caseTableConfig.externalServiceGroupIds || []).join(","),
  }));

  servicesSZ = query(this, "public-service", () => ({
    available_in_distribution: true,
  }));

  formsSZ = query(this, "form", () => ({
    form_state: "1", // Published
    forms_all_versions: false,
  }));

  municipalities = findAll(this, "location", () => ({}));

  buildingPermitTypes = trackedFunction(this, async () => {
    const response = await this.apollo.query(
      { query: getBuildingPermitQuestion },
      "allQuestions.edges"
    );

    return response[0]?.node.options.edges.map((edge) => edge.node);
  });

  responsibleServices = query(this, "responsible-service", () => ({
    service: this.shoebox.content.serviceId,
    include: "responsible-user",
  }));

  get responsibleServiceUsers() {
    const userIds = this.responsibleServices.records?.map(
      (responsibleService) => responsibleService.get("responsibleUser.id")
    );

    return [
      ...this.store.peekAll("user").filter((user) => userIds.includes(user.id)),
      {
        id: "nobody",
        fullName: this.intl.t("cases.filters.responsibleServiceUser-nobody"),
      },
    ];
  }

  get caseStatusOptions() {
    return caseFilters.caseStatus.optionValues.map((option) => ({
      status: option,
      label: this.intl.t(`cases.status.${option}`),
    }));
  }

  @cached
  get caseFilters() {
    const activeFiltersConfig =
      caseTableConfig.activeFilters[this.args.casesBackend] ?? [];

    const activeFilters = Array.isArray(activeFiltersConfig)
      ? activeFiltersConfig
      : activeFiltersConfig[this.shoebox.role] ??
        activeFiltersConfig.default ??
        [];

    return Object.entries(caseFilters).reduce(
      (populatedFilters, [key, config]) => {
        const filter = activeFilters.includes(key)
          ? {
              [key]: {
                ...config,
                ...(config.options
                  ? {
                      options:
                        this[config.options]?.records ??
                        this[config.options]?.value ??
                        this[config.options] ??
                        [],
                    }
                  : {}),
              },
            }
          : {};

        return {
          ...populatedFilters,
          ...filter,
        };
      },
      {}
    );
  }

  get storedFiltersKey() {
    return [
      "case-list-filters",
      "user",
      this.shoebox.content.userId,
      "group",
      this.shoebox.content.groupId,
      "resource",
      this.shoebox.content.resourceId,
    ].join("-");
  }

  get storedFilters() {
    try {
      return JSON.parse(localStorage.getItem(this.storedFiltersKey));
    } catch (e) {
      return {};
    }
  }

  set storedFilters(value) {
    try {
      localStorage.setItem(this.storedFiltersKey, JSON.stringify(value));
    } catch (e) {
      // If the value is somehow corrupt and can't be saved into the local
      // storage, we keep the old value stored
    }
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
    this.storedFilters = this._filter;
  }

  @action resetFilter(event) {
    event.preventDefault();

    this._filter = {};
    this.args.onChange({});
    this.storedFilters = {};
  }
}
