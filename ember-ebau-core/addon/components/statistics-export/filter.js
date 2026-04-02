import { action } from "@ember/object";
import { service } from "@ember/service";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { query } from "ember-data-resources";
import { DateTime } from "luxon";
import { trackedFunction } from "reactiveweb/function";

import mainConfig from "ember-ebau-core/config/main";
import statExportCfg from "ember-ebau-core/config/statistics-export";
import filterConfig from "ember-ebau-core/config/statistics-export-filters";
import decisionsQuery from "ember-ebau-core/gql/queries/decisions.graphql";
import rootFormsQuery from "ember-ebau-core/gql/queries/root-forms.graphql";
import { getRecursiveSources } from "ember-ebau-core/utils/form-filters";

export default class StatisticsExportFilterComponent extends Component {
  @queryManager apollo;

  @service intl;
  @service ebauModules;
  @service session;

  @tracked _filter;

  constructor(...args) {
    super(...args);
    this._filter = { ...this.args.filter };
  }

  instanceStates = query(this, "instance-state", () => ({}));

  taskOptions = query(this, "work-item-list-task-option", () => ({}));

  forms = trackedFunction(this, async () => {
    const rawForms = await this.apollo.query(
      { query: rootFormsQuery },
      "allForms.edges",
    );

    return rawForms
      .filter((edge) => edge.node.isPublished)
      .map((edge) => ({
        name: edge.node.name,
        value: [
          edge.node.slug,
          ...getRecursiveSources(edge.node, rawForms),
        ].join(","),
      }))
      .sort((a, b) => a.name.localeCompare(b.name));
  });

  decisionOptions = trackedFunction(this, async () => {
    const response = await this.apollo.query(
      {
        query: decisionsQuery,
        variables: { decisionSlug: mainConfig.decision?.answerSlugs.decision },
      },
      "allQuestions.edges",
    );

    return response[0]?.node.options.edges.map((edge) => edge.node);
  });

  get exportTypes() {
    const role = this.ebauModules?.baseRole;
    const serviceGroup = this.session.serviceGroup?.slug;
    if (!role && !serviceGroup) return [];

    const allowedExportTypes =
      statExportCfg?.exportTypes?.byRoles?.[role] ??
      statExportCfg?.exportTypes?.byServiceGroups?.[serviceGroup] ??
      [];

    return allowedExportTypes.map((type) => {
      return {
        value: type,
        label: this.intl.t(`statistics-export.export-types.${type}`),
      };
    });
  }

  get availableFilters() {
    const exportType = this._filter.exportType;
    if (!exportType) return [];
    return filterConfig[exportType] ?? [];
  }

  get selectedForm() {
    const forms = this._filter.form;
    if (!forms?.length) return [];
    return this.forms.value?.filter((f) => forms.includes(f.value)) ?? [];
  }

  get selectedInstanceState() {
    const ids = this._filter.instanceState;
    if (!ids?.length) return [];
    return (
      this.instanceStates.records?.filter((s) =>
        ids.map(String).includes(String(s.id)),
      ) ?? []
    );
  }

  get availableTaskOptions() {
    return (
      this.taskOptions.records?.map((record) => {
        const labelKey = `workItems.filters.task.${record.id}`;
        const label = this.intl.exists(labelKey)
          ? this.intl.t(labelKey)
          : record.label;
        return { id: record.id, label };
      }) ?? []
    );
  }

  get selectedTask() {
    const ids = this._filter.task;
    if (!ids?.length) return [];
    return this.availableTaskOptions.filter((t) =>
      ids.map(String).includes(String(t.id)),
    );
  }

  get selectedDecision() {
    const slug = this._filter.decision;
    return slug
      ? this.decisionOptions.value?.find((d) => d.slug === slug)
      : null;
  }

  get selectedExportType() {
    const exportType = this._filter.exportType;
    return exportType
      ? this.exportTypes.find((t) => t.value === exportType)
      : null;
  }

  get roleOptions() {
    return [
      {
        value: "active",
        label: this.intl.t("workItems.filters.active"),
      },
      {
        value: "control",
        label: this.intl.t("workItems.filters.control"),
      },
    ];
  }

  get selectedRole() {
    const role = this._filter.role;
    return role ? this.roleOptions.find((o) => o.value === role) : null;
  }

  get involvedOptions() {
    return [
      {
        value: "true",
        label: this.intl.t("global.yes"),
      },
      {
        value: "false",
        label: this.intl.t("global.no"),
      },
    ];
  }

  get selectedInvolved() {
    const involved = this._filter.involved;
    return involved !== null && involved !== undefined
      ? this.involvedOptions.find((o) => o.value === String(involved))
      : null;
  }

  @action
  selectForm(options) {
    this._filter = {
      ...this._filter,
      form: options.length ? options.map((o) => o.value) : null,
    };
    this.args.onChange(this._filter);
  }

  @action
  selectInstanceState(options) {
    this._filter = {
      ...this._filter,
      instanceState: options.length ? options.map((o) => o.id) : null,
    };
    this.args.onChange(this._filter);
  }

  @action
  selectTask(options) {
    this._filter = {
      ...this._filter,
      task: options.length ? options.map((o) => o.id) : null,
    };
    this.args.onChange(this._filter);
  }

  @action
  selectDecision(option) {
    this._filter = {
      ...this._filter,
      decision: option?.slug ?? null,
    };
    this.args.onChange(this._filter);
  }

  @action
  selectRole(option) {
    this._filter = {
      ...this._filter,
      role: option?.value ?? null,
    };
    this.args.onChange(this._filter);
  }

  @action
  selectInvolved(option) {
    this._filter = {
      ...this._filter,
      involved: option?.value ?? null,
    };
    this.args.onChange(this._filter);
  }

  @action
  selectExportType(option) {
    this._filter = {
      ...this._filter,
      exportType: option?.value ?? null,
      role: option?.value === "work-items" ? "active" : null,
    };
    this.args.onChange(this._filter);
  }

  @action
  updateDateFilter(field, value) {
    const date = value instanceof Date ? DateTime.fromJSDate(value) : null;
    this._filter = {
      ...this._filter,
      [field]: date?.isValid ? date.toISODate() : null,
    };
    this.args.onChange(this._filter);
  }

  @action
  applyFilter(event) {
    event.preventDefault();
    this.args.onChange(this._filter);
  }

  @action
  resetFilter(event) {
    event.preventDefault();
    const exportType = this._filter.exportType;
    this._filter = {
      exportType,
      role: exportType === "work-items" ? "active" : null,
    };
    this.args.onChange(this._filter);
  }
}
