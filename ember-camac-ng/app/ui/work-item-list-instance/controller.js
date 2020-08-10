import Controller from "@ember/controller";
import { action, set } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";

export default class WorkItemListInstanceController extends Controller {
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

  get userId() {
    return this.shoebox.content.userId;
  }

  get options() {
    return {
      pageSize: 20,
      processAll: workItems => this.processAll(workItems)
    };
  }

  async processAll(workItems) {
    const users = [
      ...new Set([
        this.userId,
        ...workItems.reduce(
          (ids, workItem) => [...ids, ...workItem.assignedUsers],
          []
        )
      ])
    ];

    const usernames = [
      ...new Set(
        workItems.reduce(
          (names, workItem) => [...names, workItem.closedByUser],
          []
        )
      )
    ];

    if (users.length) {
      await this.store.query("user", {
        id: users.join(",")
      });
    }

    if (usernames.length) {
      await this.store.query("user", {
        username: usernames.join(",")
      });
    }

    return workItems;
  }

  @dropTask
  *fetchWorkItems() {
    const filter = [];

    if (this.filters.role === "control") {
      filter.push({ controllingGroups: [this.shoebox.content.serviceId] });
    } else {
      filter.push({ addressedGroups: [this.shoebox.content.serviceId] });
    }

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
