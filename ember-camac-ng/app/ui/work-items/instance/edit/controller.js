import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { useCalumaQuery } from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { query } from "ember-data-resources";
import { processNewWorkItems } from "ember-ebau-core/utils/work-item";
import { cached } from "tracked-toolbox";

import completeWorkItem from "camac-ng/gql/mutations/complete-work-item.graphql";
import saveWorkItem from "camac-ng/gql/mutations/save-workitem.graphql";

export default class WorkItemsInstanceEditController extends Controller {
  @queryManager apollo;

  @service store;
  @service notifications;
  @service intl;
  @service shoebox;
  @service router;

  workItemsQuery = useCalumaQuery(this, allWorkItems, () => ({
    options: {
      pageSize: 1,
      processNew: (workItems) => processNewWorkItems(this.store, workItems),
    },
    filter: [{ id: this.model }],
  }));

  @cached
  get workItem() {
    return this.workItemsQuery.value[0];
  }

  users = query(this, "public-user", () => ({
    service: this.shoebox.content.serviceId,
    disabled: false,
  }));

  @dropTask
  *finishWorkItem(event) {
    event.preventDefault();

    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: this.workItem.id,
            meta: JSON.stringify(this.workItem.meta),
          },
        },
      });

      yield this.apollo.mutate({
        mutation: completeWorkItem,
        variables: { id: this.workItem.id },
      });

      this.notifications.success(this.intl.t("workItems.finishSuccess"));

      this.router.transitionTo("work-items.instance.index");
    } catch (error) {
      this.notifications.error(this.intl.t("workItems.saveError"));
    }
  }

  @dropTask
  *saveWorkItem(event) {
    event.preventDefault();

    let assignedUsers;
    if (this.workItem.assignedUser) {
      assignedUsers = this.workItem.assignedUsers;
    }

    try {
      yield this.apollo.mutate({
        mutation: saveWorkItem,
        variables: {
          input: {
            workItem: this.workItem.id,
            description: this.workItem.description,
            deadline: this.workItem.deadline,
            assignedUsers,
            meta: JSON.stringify(this.workItem.meta),
          },
        },
      });

      this.notifications.success(this.intl.t("workItems.saveSuccess"));

      this.router.transitionTo("work-items.instance.index");
    } catch (error) {
      this.notifications.error(this.intl.t("workItems.saveError"));
    }
  }
}
