import Controller from "@ember/controller";
import { action, set } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";

import getProcessData from "camac-ng/utils/work-item";

export default class WorkItemsInstanceIndexController extends Controller {
  queryParams = ["role"];

  @service store;
  @service shoebox;
  @service apollo;

  // Filters
  @tracked role = "active";

  @calumaQuery({
    query: allWorkItems,
    options: "options"
  })
  readyWorkItemsQuery;

  @calumaQuery({
    query: allWorkItems,
    options: "options"
  })
  completedWorkItemsQuery;

  get options() {
    return {
      processNew: workItems => this.processNew(workItems)
    };
  }

  async processNew(workItems) {
    const { usernames, instanceIds, serviceIds } = getProcessData(workItems);

    if (usernames.length) {
      await this.store.query("user", { username: usernames.join(",") });
    }

    if (instanceIds.length) {
      await this.store.query("instance", {
        instance_id: instanceIds.join(","),
        include: "form"
      });
    }

    if (serviceIds.length) {
      await this.store.query("service", { service_id: serviceIds.join(",") });
    }

    return workItems;
  }

  @dropTask
  *fetchWorkItems() {
    const filterKey =
      this.role === "control" ? "controllingGroups" : "addressedGroups";

    const filter = [
      { hasDeadline: true },
      {
        rootCaseMetaValue: [{ key: "camac-instance-id", value: this.model.id }]
      },
      { [filterKey]: [this.shoebox.content.serviceId] }
    ];

    yield this.readyWorkItemsQuery.fetch({
      filter: [...filter, { status: "READY" }],
      order: [{ attribute: "DEADLINE", direction: "ASC" }]
    });

    yield this.completedWorkItemsQuery.fetch({
      filter: [...filter, { status: "COMPLETED" }],
      order: [{ attribute: "CLOSED_AT", direction: "DESC" }]
    });
  }

  @action
  updateFilter(type, value) {
    set(this, type, value);
    this.fetchWorkItems.perform();
  }
}
