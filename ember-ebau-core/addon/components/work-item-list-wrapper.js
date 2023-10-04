import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";

import getProcessData, {
  processNewWorkItems,
} from "ember-ebau-core/utils/work-item";

export default class WorkItemListWrapperComponent extends Component {
  @queryManager apollo;

  @service store;

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
      ...(this.args.type === "unread"
        ? [{ metaValue: [{ key: "not-viewed", value: true }] }]
        : []),
    ];
  }

  get gqlOrder() {
    return this.args.order === "urgent"
      ? [{ attribute: "DEADLINE", direction: "ASC" }]
      : [{ attribute: "CREATED_AT", direction: "DESC" }];
  }
}
