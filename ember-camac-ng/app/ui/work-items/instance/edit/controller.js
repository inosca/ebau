import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";

import completeWorkItem from "camac-ng/gql/mutations/complete-work-item.graphql";
import saveWorkItem from "camac-ng/gql/mutations/save-workitem.graphql";
import getProcessData from "camac-ng/utils/work-item";

export default class WorkItemsInstanceEditController extends Controller {
  @queryManager apollo;

  @service store;
  @service notifications;
  @service intl;
  @service shoebox;
  @service router;

  @calumaQuery({
    query: allWorkItems,
    options: "options",
  })
  workItemsQuery;

  get options() {
    return {
      pageSize: 1,
      processNew: (workItems) => this.processNew(workItems),
    };
  }

  async processNew(workItems) {
    const { usernames, instanceIds, serviceIds } = getProcessData(workItems);

    if (usernames.length) {
      await this.store.query("public-user", { username: usernames.join(",") });
    }

    if (instanceIds.length) {
      await this.store.query("instance", {
        instance_id: instanceIds.join(","),
        include: "form",
      });
    }

    if (serviceIds.length) {
      await this.store.query("service", { service_id: serviceIds.join(",") });
    }

    return workItems;
  }

  @lastValue("fetchWorkItems") workItem;
  @dropTask
  *fetchWorkItems() {
    try {
      yield this.workItemsQuery.fetch({ filter: [{ id: this.model }] });

      return this.workItemsQuery.value[0];
    } catch (error) {
      this.notifications.error(this.intl.t("workItems.fetchError"));
    }
  }

  @lastValue("fetchUserChoices") userChoices;
  @dropTask
  *fetchUserChoices() {
    try {
      return (yield this.store.query("public-user", {
        service: this.shoebox.content.serviceId,
        disabled: false,
      })).toArray();
    } catch (error) {
      this.notifications.error(this.intl.t("workItems.fetchError"));
    }
  }

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
            meta: JSON.stringify(this.workItem?.meta),
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
