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
import decisionsQuery from "camac-ng/gql/queries/decisions.graphql";
import getBuildingPermitQuestion from "camac-ng/gql/queries/get-building-permit-question.graphql";
import municipalitiesQuery from "camac-ng/gql/queries/municipalities.graphql";
import rootFormsQuery from "camac-ng/gql/queries/root-forms.graphql";

const getRecursiveSources = (form, forms) => {
  if (!form.source?.slug) {
    return [];
  }

  const source = forms.find((edge) => edge.node.slug === form.source.slug);

  return [source.node.slug, ...getRecursiveSources(source.node, forms)];
};

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
    order: [{ attribute: "NAME", direction: "ASC" }],
    filter: [
      { isPublished: true },
      { isArchived: false },
      { metaValue: [{ key: "is_creatable", value: true }] },
    ],
  }));

  instanceStates = query(this, "instance-state", () => ({
    instance_state_id: this.args.instanceStates.join(","),
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

  tags = findAll(this, "tag", () => ({}));

  buildingPermitTypes = trackedFunction(this, async () => {
    const response = await this.apollo.query(
      { query: getBuildingPermitQuestion },
      "allQuestions.edges"
    );

    return response[0]?.node.options.edges.map((edge) => edge.node);
  });

  responsibleServices = query(this, "responsible-service", () => ({
    service: this.shoebox.content.serviceId,
  }));

  responsibleServiceUsers = trackedFunction(this, async () => {
    await Promise.resolve();

    const users = await this.store.query("user", {
      responsible_for_instances: true,
      sort: "name",
    });

    return [
      ...users.toArray(),
      {
        id: "nobody",
        fullName: this.intl.t("cases.filters.responsibleServiceUser-nobody"),
      },
    ];
  });

  get caseStatusOptions() {
    return [
      { status: "RUNNING", label: this.intl.t("cases.status.RUNNING") },
      { status: "COMPLETED", label: this.intl.t("cases.status.COMPLETED") },
    ];
  }

  responsibleMunicipalities = query(this, "public-service", () => ({
    service_group_name: "municipality,district",
    has_parent: false,
    sort: "-service_group__name,trans__name",
  }));

  forms = trackedFunction(this, async () => {
    const categories = [
      "preliminary-clarification",
      "building-permit",
      "special-procedure",
      "others",
    ];

    const rawForms = await this.apollo.query(
      { query: rootFormsQuery },
      "allForms.edges"
    );

    const forms = rawForms
      .filter((edge) => edge.node.isPublished)
      .map((edge) => ({
        name: edge.node.name,
        value: [edge.node.slug, ...getRecursiveSources(edge.node, rawForms)],
        category: edge.node.meta.category || "others",
        order: edge.node.meta.order,
        isEqual(other) {
          return this.value.join(",") === other.value.join(",");
        },
      }));

    return categories
      .map((category) => {
        const options = forms
          .filter((form) => form.category === category)
          .sort((a, b) => a.order - b.order);

        return options.length
          ? {
              groupName: this.intl.t(`cases.formCategories.${category}`),
              options,
            }
          : null;
      })
      .filter(Boolean);
  });

  municipalitiesFromCaluma = trackedFunction(this, async () => {
    const response = await this.apollo.query(
      { query: municipalitiesQuery },
      "allQuestions.edges"
    );

    return response[0]?.node.options.edges.map((edge) => edge.node);
  });

  get paperOptions() {
    return [
      { value: "1", label: this.intl.t("cases.paper.only") },
      { value: "0", label: this.intl.t("cases.paper.none") },
    ];
  }

  get inquiryStateOptions() {
    return [
      { value: "pending", label: this.intl.t("cases.inquiryState.pending") },
      {
        value: "completed",
        label: this.intl.t("cases.inquiryState.completed"),
      },
    ];
  }

  decisionOptions = trackedFunction(this, async () => {
    const response = await this.apollo.query(
      { query: decisionsQuery },
      "allQuestions.edges"
    );

    return response[0]?.node.options.edges.map((edge) => edge.node);
  });

  get presets() {
    return (
      caseTableConfig.filterPresets?.[this.shoebox.baseRole] ??
      caseTableConfig.filterPresets?.default ??
      []
    );
  }

  @cached
  get caseFilters() {
    const activeFiltersConfig =
      caseTableConfig.activeFilters[this.args.casesBackend] ?? [];

    const activeFilters = Array.isArray(activeFiltersConfig)
      ? activeFiltersConfig
      : activeFiltersConfig[this.shoebox.baseRole] ??
        activeFiltersConfig.default ??
        [];

    return Object.entries(caseFilters)
      .sort((a, b) => activeFilters.indexOf(a[0]) - activeFilters.indexOf(b[0]))
      .reduce((populatedFilters, [key, config]) => {
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
      }, {});
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

  @action applyPreset(filters, event) {
    event.preventDefault();

    this._filter = filters;
    this.args.onChange(filters);
    this.storedFilters = filters;
  }
}
