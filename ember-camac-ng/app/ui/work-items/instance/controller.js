import Controller from "@ember/controller";
import { action, set } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";

export default class WorkItemsInstanceController extends Controller {
  @service store;
  @service shoebox;

  @tracked order = [{ attribute: "DEADLINE", direction: "ASC" }];
  @tracked filters = {
    role: "active"
  };

  @calumaQuery({
    query: allWorkItems,
    options: "options"
  })
  workItemsQuery;

  get options() {
    return {
      pageSize: 20,
      processAll: workItems => this.processAll(workItems)
    };
  }

  async processAll(workItems) {
    const workItemRelatedUsers = [
      ...new Set(
        workItems.reduce(
          (names, workItem) => [
            ...names,
            workItem.closedByUser,
            ...workItem.assignedUsers
          ],
          []
        )
      )
    ];

    if (workItemRelatedUsers.length) {
      await this.store.query("user", {
        username: workItemRelatedUsers.join(",")
      });
    }

    return workItems;
  }

  @dropTask
  *fetchWorkItems() {
    const filterKey =
      this.filters.role === "control" ? "controllingGroups" : "addressedGroups";
    const filter = [
      { hasDeadline: true },
      { [filterKey]: [this.shoebox.content.serviceId] }
    ];

    yield this.workItemsQuery.fetch({
      filter,
      order: this.order
    });
  }

  get activeWorkItems() {
    return this.workItemsQuery.value.filter(workItem => {
      return workItem.raw.status.toLowerCase() === "ready";
    });
  }

  get doneWorkItems() {
    return this.workItemsQuery.value.filter(workItem => {
      return workItem.raw.status.toLowerCase() !== "ready";
    });
  }

  @action
  updateFilter(type, value) {
    set(this, `filters.${type}`, value);
    this.fetchWorkItems.perform();
  }
}
