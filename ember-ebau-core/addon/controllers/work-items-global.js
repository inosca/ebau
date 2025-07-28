import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { isEmpty } from "@ember/utils";
import { tracked } from "@glimmer/tracking";
import { query } from "ember-data-resources";
import { trackedFunction } from "reactiveweb/function";

import workItemListConfig from "ember-ebau-core/config/work-item-list";
import paginatedQuery from "ember-ebau-core/resources/paginated";
import cleanObject from "ember-ebau-core/utils/clean-object";

const { filterDefaults } = workItemListConfig;

export default class WorkItemsGlobalController extends Controller {
  @service intl;
  @service store;
  @service fetch;
  @service ebauModules;

  workItemListConfig = workItemListConfig;

  queryParams = [
    "order",
    "responsible",
    "type",
    "status",
    "role",
    "task",
    "preset",
  ];

  // Filters
  @tracked order = filterDefaults.order;
  @tracked responsible = filterDefaults.responsible;
  @tracked type = filterDefaults.type;
  @tracked role = filterDefaults.role;
  @tracked status = filterDefaults.status;
  @tracked task = filterDefaults.task;
  @tracked preset = filterDefaults.preset;

  // Pagination
  @tracked page = 1;

  allResponsibles = trackedFunction(this, async () => {
    const users = await this.store.query("user", {
      sort: "name",
    });
    return [
      { value: "all", label: this.intl.t("workItems.filters.all") },
      { value: "own", label: this.intl.t("workItems.filters.own") },
      ...users.map((u) => ({
        label: `${u.name} ${u.surname}`,
        value: u.username,
      })),
    ];
  });

  workItems = paginatedQuery(this, "work-item-list-row", () => ({
    "fields[work-item-list-rows]": this.requestedFields.fields.join(","),
    include: this.requestedFields.include.join(","),
    page: { number: this.page, size: workItemListConfig.pageSize || 20 },
    sort: this.sort,
    ...this.filters,
  }));

  taskOptions = query(this, "work-item-list-task-option", () => {
    // eslint-disable-next-line no-unused-vars
    const { task = null, ...filters } = this.filters;

    return filters;
  });

  get availableTasks() {
    return [
      { value: "all", label: this.intl.t("workItems.filters.all") },
      ...(this.taskOptions.records?.map((option) => option.asOption()) ?? []),
    ];
  }

  get sort() {
    if (this.order === "urgent") {
      return "deadline";
    } else if (this.order === "new") {
      return "-created_at";
    }

    return "";
  }

  get filters() {
    let responsible = null;
    if (this.responsible === "own") {
      responsible = this.ebauModules.userName;
    } else if (this.responsible !== "all") {
      responsible = this.responsible;
    }

    return cleanObject({
      role: this.role,
      status: this.status.toLowerCase(),
      unread: this.type === "unread" ? 1 : null,
      task: this.task !== "all" ? this.task : null,
      preset: this.preset,
      responsible,
    });
  }

  get columns() {
    return workItemListConfig.columns(this.status, this.ebauModules.baseRole);
  }

  get highlight() {
    return this.status !== "COMPLETED";
  }

  get requestedFields() {
    const columnToField = {
      __all__: {
        fields: [
          "is_addressed_to_current_service",
          "is_assigned_to_current_user",
          "is_controlled_by_current_service",
          "is_created_by_current_service",
          "is_manually_completable",
          "is_ready",
          ...(this.highlight ? ["unread"] : []),
        ],
      },
      applicants: { fields: ["applicants"] },
      closedAt: { fields: ["closed_at"] },
      closedBy: { fields: ["closed_by_user"], include: ["closed_by_user"] },
      deadline: { fields: ["deadline"] },
      description: { fields: ["description"] },
      instance: { fields: ["instance_name", "special_id"] },
      municipality: { fields: ["municipality"] },
      responsible: {
        fields: ["assigned_user", "addressed_service"],
        include: ["assigned_user", "addressed_service"],
      },
      task: { fields: ["task", "direct_link", "edit_link"] },
    };

    const used = Object.entries(columnToField).filter(
      ([column]) => this.columns.includes(column) || column === "__all__",
    );

    return {
      fields: used.flatMap(([, config]) => config.fields ?? []),
      include: used.flatMap(([, config]) => config.include ?? []),
    };
  }

  @action
  fetchMore() {
    this.page++;
  }

  @action
  setFilter(filter, value) {
    this[filter] = value;
  }

  @action
  refreshIfFilter(filter) {
    if (isEmpty(this.filters[filter])) return;

    this.workItems.retry();
  }
}
