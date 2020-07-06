import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import calumaQuery from "ember-caluma/caluma-query";
import { allWorkItems } from "ember-caluma/caluma-query/queries";
import { dropTask } from "ember-concurrency-decorators";

import saveWorkItem from "../../gql/mutations/save-workitem";

async function processAll(workitems) {
  let users = [];
  workitems.forEach(workitem => {
    users = [...new Set([...users, ...workitem.assignedUsers])];
  });
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

  get entries() {
    return (this.workItemsQuery.value || []).sortBy("deadline").reverse();
  }

  @dropTask
  *fetchWorkitems() {
    yield this.workItemsQuery.fetch({
      filter: this.filter,
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
}
