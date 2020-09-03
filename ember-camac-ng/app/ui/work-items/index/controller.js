import Controller from "@ember/controller";
import { action, set } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";

import saveWorkItem from "../../../gql/mutations/save-workitem";

export default class WorkItemsIndexController extends Controller {
  queryParams = ["responsible", "type", "status", "role"];
  @service store;
  @service apollo;
  @service notifications;
  @service intl;
  @service shoebox;

  @tracked menuOpen = null;
  @tracked order = [{ attribute: "DEADLINE", direction: "ASC" }];
  // Filters
  @tracked responsible = "all";
  @tracked type = "all";
  @tracked status = "open";
  @tracked role = "active";

  @calumaQuery({ query: allWorkItems, options: "options" })
  workItemsQuery;

  get options() {
    return {
      pageSize: 20,
      processAll: workItems => this.processAll(workItems)
    };
  }

  async processAll(workItems) {
    let usernames = [this.shoebox.content.username];
    let instances = [];
    let services = [];

    workItems.forEach(workItem => {
      usernames.push(...workItem.assignedUsers);
      instances.push(workItem.case.meta["camac-instance-id"]);
      services.push(...workItem.addressedGroups);
    });

    usernames = [...new Set(usernames)];
    instances = [...new Set(instances)];
    services = [...new Set(services)];

    if (workItems.length) {
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
    const filter = [{ hasDeadline: true }];

    if (this.responsible === "own") {
      filter.push({ assignedUsers: [this.shoebox.content.username] });
    } else {
      filter.push({ assignedUsers: [] });
    }

    if (this.type === "new") {
      filter.push({ metaValue: [{ key: "not-viewed", value: true }] });
    }

    if (this.status === "closed") {
      filter.push({ status: "COMPLETED" });
    } else {
      filter.push({ status: "READY" });
    }

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

  @dropTask
  *fetchMoreWorkItems() {
    yield this.workItemsQuery.fetchMore();
  }

  @dropTask
  *workItemAssignUser(workitem) {
    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: workitem.id,
            assignedUsers: [
              ...workitem.assignedUsers,
              this.shoebox.content.username
            ]
          }
        }
      });

      set(workitem, "assignedUsers", [
        ...workitem.assignedUsers,
        this.shoebox.content.username
      ]);
    } catch (error) {
      this.notifications.error(this.intl.t("workitemlist.saveError"));
    }
  }

  @dropTask
  *workItemRead(workitem) {
    set(workitem.meta, "not-viewed", false);
    set(workitem, "notViewed", false);

    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: workitem.id,
            meta: JSON.stringify(workitem.meta)
          }
        }
      });
    } catch (error) {
      this.notifications.error(this.intl.t("workitemlist.saveError"));
    }
  }

  @action
  updateFilter(type, value) {
    set(this, type, value);
    this.fetchWorkItems.perform();
  }
}
