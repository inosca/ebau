import Controller from "@ember/controller";
import { action, set } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";

export default class WorkItemListInstanceController extends Controller {
  queryParams = ["role"];

  @service store;
  @service shoebox;

  @tracked order = [{ attribute: "DEADLINE", direction: "ASC" }];
  // Filters
  @tracked role = "active";

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
    let users = [];
    let usernames = [];
    let instances = [];
    let services = [];

    workItems.forEach(workItem => {
      users.push(...workItem.assignedUsers);
      instances.push(workItem.case.meta["camac-instance-id"]);
      services.push(...workItem.addressedGroups);
      usernames.push(workItem.closedByUser, workItem.createdByUser);
    });

    users = [...new Set(users)];
    usernames = [...new Set(usernames)];
    instances = [...new Set(instances)];
    services = [...new Set(services)];

    if (users.length) {
      await this.store.query("user", { id: users.join(",") });
    }

    if (usernames.length) {
      await this.store.query("user", { username: usernames.join(",") });
    }

    if (instances.length) {
      await this.store.query("instance", {
        instance_id: instances.join(","),
        include: "form"
      });
    }

    if (services.length) {
      await this.store.query("service", { service_id: services.join(",") });
    }

    return workItems;
  }

  @dropTask
  *fetchWorkItems() {
    const filter = [];

    if (this.role === "control") {
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
    set(this, type, value);
    this.fetchWorkItems.perform();
  }

  @action
  newWorkItem() {
    this.transitionToRoute("work-item");
  }
}
