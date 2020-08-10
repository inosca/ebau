import Controller from "@ember/controller";
import { action, set } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";

import saveWorkItem from "../../gql/mutations/save-workitem";

export default class WorkitemListController extends Controller {
  @service store;
  @service apollo;
  @service notifications;
  @service intl;
  @service shoebox;

  @tracked menuOpen = null;
  @tracked filters = {
    responsible: "all",
    type: "all",
    status: "open",
    role: "active"
  };
  @tracked order = [{ attribute: "DEADLINE", direction: "ASC" }];

  @calumaQuery({ query: allWorkItems, options: "options" })
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

    const instances = [
      ...new Set(
        workItems.map(workItem => workItem.case.meta["camac-instance-id"])
      )
    ];

    if (instances.length) {
      await this.store.query("instance", {
        id: instances.join(","),
        include: "form"
      });
    }

    if (users.length) {
      await this.store.query("user", { id: users.join(",") });
    }

    return workItems;
  }

  @dropTask
  *fetchWorkItems() {
    const filter = [];

    if (this.filters.responsible === "own") {
      filter.push({ assignedUsers: [this.userId] });
    } else {
      filter.push({ assignedUsers: [] });
    }

    if (this.filters.type === "new") {
      filter.push({ metaValue: [{ key: "not-viewed", value: true }] });
    }

    if (this.filters.status === "closed") {
      filter.push({ status: "READY", invert: true });
    } else {
      filter.push({ status: "READY" });
    }

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
            assignedUsers: [...workitem.assignedUsers, this.userId]
          }
        }
      });

      set(workitem, "assignedUsers", [...workitem.assignedUsers, this.userId]);
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
    set(this, `filters.${type}`, value);
    this.fetchWorkItems.perform();
  }
}
