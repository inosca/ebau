import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { camelize } from "@ember/string";
import Component from "@glimmer/component";
import { tracked } from "@glimmer/tracking";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "ember-resources/util/function";
import { gql } from "graphql-tag";

import workItemListConfig from "ember-ebau-core/config/work-item-list";
import getProcessData, {
  processNewWorkItems,
} from "ember-ebau-core/utils/work-item";

export default class WorkItemListWrapperComponent extends Component {
  @queryManager apollo;

  @service store;
  @service calumaOptions;
  @service intl;
  @tracked responsible = "all";

  workItemsQuery = useCalumaQuery(this, allWorkItems, () => ({
    options: {
      pageSize: 20,
      processNew: (workItems) => this.processNew(workItems),
    },
    filter: this.gqlFilter,
    order: this.gqlOrder,
  }));

  workItemListConfig = workItemListConfig;

  get columns() {
    return [
      "task",
      "instance",
      "description",
      ...(this.args.status === "COMPLETED"
        ? ["closedAt", "closedBy"]
        : ["deadline", "responsible"]),
    ];
  }

  async processNew(workItems) {
    const { usernames, instanceIds } = getProcessData(workItems);

    await processNewWorkItems(this.store, workItems);

    if (!usernames.includes(this.args.username)) {
      await this.store.query("public-user", {
        username: this.args.username,
      });
    }

    if (instanceIds.length && this.args.application === "kt_schwyz") {
      await this.store.query("form-field", {
        instance: instanceIds.join(","),
        name: "bezeichnung,bezeichnung-override",
      });
    }

    return workItems;
  }

  get gqlFilter() {
    return [
      { hasDeadline: true },
      { status: this.args.status },
      {
        addressedGroups: [String(this.args.serviceId)],
        invert: this.args.role === "control",
      },
      ...(this.args.role === "control"
        ? [{ controllingGroups: [String(this.args.serviceId)] }]
        : []),
      ...(this.args.responsible === "own"
        ? [{ assignedUsers: [this.args.username] }]
        : []),
      ...(!["own", "all"].includes(this.args.responsible)
        ? [{ assignedUsers: [this.args.responsible] }]
        : []),
      ...(this.args.type === "unread"
        ? [{ metaValue: [{ key: "not-viewed", value: true }] }]
        : []),
      ...(this.args.task !== "all" ? [{ task: this.args.task }] : []),
    ];
  }

  get gqlOrder() {
    return this.args.order === "urgent"
      ? [{ attribute: "DEADLINE", direction: "ASC" }]
      : [{ attribute: "CREATED_AT", direction: "DESC" }];
  }

  get _taskSlugs() {
    if (!workItemListConfig.showTaskFilter) {
      return [];
    }

    const availableTasks = workItemListConfig.availableTasks;

    return [
      ...(availableTasks.roles[this.args.roleId] ?? []),
      ...(availableTasks.services[this.args.serviceId] ?? []),
      ...(availableTasks.default ?? []),
    ];
  }

  availableTasks = trackedFunction(this, async () => {
    if (!this.workItemsQuery.value || this._taskSlugs.length === 0) {
      return [];
    }

    /* In order to avoid having 1 request per task filter btn we do a single query.
      However, as we have a dynamic number of tasks and we need to use the task slug in the filter
      we need to build the query dynamically. The code below will generate graphql query like this:

      query WorkItemsForTasks {
        myFirstTask: allTasks(filter: [{ hasDeadline: true }, .... { task: "my-first-task" }]) {
          totalCount
        }
        mySecondTask: allTasks(filter: [{ hasDeadline: true }, .... { task: "my-second-task" }]) {
          totalCount
        }
      }
    */

    const body = this._taskSlugs
      .map(camelize)
      .map((snakeCaseTaskSlug, i) => {
        const filters = [...this.gqlFilter];
        const existingTaskFilter = filters.find((filter) => filter.task);

        if (existingTaskFilter) {
          existingTaskFilter.task = this._taskSlugs[i];
        } else {
          filters.push({ task: this._taskSlugs[i] });
        }

        // The weird string stuff and replacement stuff is required because of the differences between JSON and GraphQL
        // such as graphql enums, etc.
        return `${snakeCaseTaskSlug}: allWorkItems(filter: ${JSON.stringify(
          filters,
        )
          .replace(/"(\w+)":/g, "$1:")
          .replace(/"SUSPENDED"/g, "SUSPENDED")
          .replace(/"COMPLETED"/g, "COMPLETED")
          .replace(/"READY"/g, "READY")}) {
          totalCount
        }`;
      })
      .join("\n");

    const query = gql`
      query WorkItemsForTasks {
        ${body}
      }
    `;

    const allTasks = await this.apollo.query({
      query,
    });

    return [
      { value: "all", label: this.intl.t("workItems.filters.all") },
      ...Object.keys(allTasks).map((task, i) => ({
        label: this.intl.t(`workItems.filters.task.${this._taskSlugs[i]}`, {
          count: allTasks[task].totalCount,
        }),
        value: this._taskSlugs[i],
      })), // prepare options for select
    ];
  });

  allResponsibles = trackedFunction(this, async () => {
    await Promise.resolve();
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

  get selectedResponsible() {
    return this.allResponsibles.value?.find(
      (r) => r.value === this.responsible,
    );
  }

  @action
  setResponsible(person) {
    this.responsible = person.value;
    this.args.setFilter("responsible", person.value);
  }
}
