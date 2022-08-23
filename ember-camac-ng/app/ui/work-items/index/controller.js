import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import getProcessData, {
  processNewWorkItems,
} from "ember-ebau-core/utils/work-item";

export default class WorkItemsIndexController extends Controller {
  queryParams = ["order", "responsible", "type", "status", "role"];

  @queryManager apollo;

  @service store;
  @service shoebox;

  // Filters
  @tracked order = "urgent";
  @tracked responsible = "all";
  @tracked type = "all";
  @tracked status = "open";
  @tracked role = "active";

  workItemsQuery = useCalumaQuery(this, allWorkItems, () => ({
    options: {
      pageSize: 20,
      processNew: (workItems) => this.processNew(workItems),
    },
    filter: this.gqlFilter,
    order: this.gqlOrder,
  }));

  get columns() {
    return [
      "task",
      "instance",
      "description",
      ...(this.status === "open"
        ? ["deadline", "responsible"]
        : ["closedAt", "closedBy"]),
    ];
  }

  async processNew(workItems) {
    const { usernames, instanceIds } = getProcessData(workItems);

    await processNewWorkItems(this.store, workItems);

    if (!usernames.includes(this.shoebox.content.username)) {
      await this.store.query("public-user", {
        username: this.shoebox.content.username,
      });
    }

    if (
      instanceIds.length &&
      this.shoebox.content.application === "kt_schwyz"
    ) {
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
      { status: this.status === "closed" ? "COMPLETED" : "READY" },
      {
        addressedGroups: [String(this.shoebox.content.serviceId)],
        invert: this.role === "control",
      },
      ...(this.role === "control"
        ? [{ controllingGroups: [String(this.shoebox.content.serviceId)] }]
        : []),
      ...(this.responsible === "own"
        ? [{ assignedUsers: [this.shoebox.content.username] }]
        : []),
      ...(this.type === "unread"
        ? [{ metaValue: [{ key: "not-viewed", value: true }] }]
        : []),
    ];
  }

  get gqlOrder() {
    return this.order === "urgent"
      ? [{ attribute: "DEADLINE", direction: "ASC" }]
      : [{ attribute: "CREATED_AT", direction: "DESC" }];
  }
}
