import { action } from "@ember/object";
import { next } from "@ember/runloop";
import { inject as service } from "@ember/service";
import { isTesting, macroCondition } from "@embroider/macros";
import { ensureSafeComponent } from "@embroider/util";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allForms } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { restartableTask, timeout } from "ember-concurrency";
import { findAll, query } from "ember-data-resources";
import { trackedFunction } from "ember-resources/util/function";
import { cached } from "tracked-toolbox";

import AsyncSelectMultipleComponent from "camac-ng/components/case-filter/async-select-multiple";
import DateComponent from "camac-ng/components/case-filter/date";
import caseFilters from "camac-ng/components/case-filter/filter-config";
import InputComponent from "camac-ng/components/case-filter/input";
import SelectComponent from "camac-ng/components/case-filter/select";
import SelectMultipleComponent from "camac-ng/components/case-filter/select-multiple";
import ToggleSwitchComponent from "camac-ng/components/case-filter/toggle-switch";
import caseTableConfig from "camac-ng/config/case-table";
import decisionsQuery from "camac-ng/gql/queries/decisions.graphql";
import getBuildingPermitQuestion from "camac-ng/gql/queries/get-building-permit-question.graphql";
import inquiryAnswersQuery from "camac-ng/gql/queries/inquiry-answers.graphql";
import municipalitiesQuery from "camac-ng/gql/queries/municipalities.graphql";
import rootFormsQuery from "camac-ng/gql/queries/root-forms.graphql";

const COMPONENT_MAPPING = {
  "async-select-multiple": AsyncSelectMultipleComponent,
  date: DateComponent,
  input: InputComponent,
  select: SelectComponent,
  "select-multiple": SelectMultipleComponent,
  "toggle-switch": ToggleSwitchComponent,
};

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

    next(this.args, "onChange", this._filter);
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

  selectedTags = trackedFunction(this, async () => {
    const key = Object.entries(this.caseFilters).find(
      ([, config]) => config.options === "selectedTags"
    )?.[0];

    const selected = this._filter[key];

    if (!selected?.length) {
      return [];
    }

    await Promise.resolve();

    return await this.store.query("tag", { name: String(selected) });
  });

  @restartableTask
  *searchTags(search) {
    if (!search) return [];

    if (macroCondition(isTesting())) {
      // no timeout
    } else {
      yield timeout(500);
    }

    yield Promise.resolve();

    return yield this.store.query("tag", {
      search,
      "page[size]": 50,
      "page[number]": 1,
    });
  }

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

  responsibleMunicipalities = trackedFunction(this, async () => {
    await Promise.resolve();

    const services = await this.store.query("public-service", {
      service_group_name: "municipality,district",
      has_parent: false,
    });

    return services.toArray().sort((a, b) => a.name.localeCompare(b.name));
  });

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
        value: [
          edge.node.slug,
          ...getRecursiveSources(edge.node, rawForms),
        ].join(","),
        category: edge.node.meta.category || "others",
        order: edge.node.meta.order,
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

  get constructionZoneLocationOptions() {
    return [
      {
        name: this.intl.t("cases.filters.constructionZoneLocationInside"),
        value: "innerhalb",
      },
      {
        name: this.intl.t("cases.filters.constructionZoneLocationOutside"),
        value: "ausserhalb",
      },
      {
        name: this.intl.t("cases.filters.constructionZoneLocationBoth"),
        value: "beides",
      },
    ];
  }

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

  inquiryAnswerOptions = trackedFunction(this, async () => {
    const response = await this.apollo.query(
      { query: inquiryAnswersQuery },
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
                component: ensureSafeComponent(
                  COMPONENT_MAPPING[config.type],
                  this
                ),
              },
            }
          : {};

        return { ...populatedFilters, ...filter };
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
