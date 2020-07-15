import Controller from "@ember/controller";
import { action, set } from "@ember/object";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";

import saveWorkItem from "../../gql/mutations/save-workitem";

async function processAll(workitems) {
  let users = [];
  let instances = [];

  workitems.forEach(workitem => {
    users = [...new Set([...users, ...workitem.assignedUsers])];
    instances = [
      ...new Set([...instances, workitem.case.meta["camac-instance-id"]])
    ];
  });

  if (instances.length) {
    this.store.query("instance", { id: instances.join(","), include: "form" });
  }
  if (users.length) {
    await this.store.query("user", { id: users.join(",") });
  }

  return workitems;
}

export default class WorkitemListController extends Controller {
  @service store;
  @service apollo;
  @service notifications;
  @service intl;
  @service shoebox;

  @tracked menuOpen = null;
  @tracked filters = {
    responsible: "all",
    status: "open",
    type: "active"
  };
  order = [{ attribute: "DEADLINE", direction: "ASC" }];

  @calumaQuery({
    query: allWorkItems,
    options: {
      pageSize: 20,
      processAll
    }
  })
  workItemsQuery;

  @dropTask
  *fetchWorkitems() {
    const filter = [];

    if (this.filters.responsible === "own") {
      filter.push({ assignedUsers: [this.shoebox.content.userId] });
    } else {
      filter.push({ assignedUsers: [] });
    }

    if (this.filters.status === "closed") {
      filter.push({ status: "READY", invert: true });
    } else {
      filter.push({ status: "READY" });
    }

    if (this.filters.type === "control") {
      filter.push({ controllingGroups: [this.shoebox.content.groupId] });
    } else {
      filter.push({ addressedGroups: [this.shoebox.content.groupId] });
    }

    yield this.workItemsQuery.fetch({
      filter,
      order: this.order
    });
  }

  @dropTask
  *workItemAssignUser(workitem) {
    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          workitem: workitem.id,
          assignedUsers: [this.shoebox.content.userId]
        }
      });
    } catch (error) {
      this.notifications.error(this.intl.t("workitemlist.saveError"));
    }
  }

  @action
  updateFilter(type, value) {
    set(this, `filters.${type}`, value);
    this.fetchWorkitems.perform();
  }
}
