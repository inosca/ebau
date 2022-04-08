import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import calumaQuery from "@projectcaluma/ember-core/caluma-query";
import { allWorkItems } from "@projectcaluma/ember-core/caluma-query/queries";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";
import getProcessData from "ember-ebau-core/utils/work-item";

import completeWorkItem from "ebau/gql/mutations/complete-work-item.graphql";
import saveWorkItem from "ebau/gql/mutations/save-workitem.graphql";

export default class CasesDetailWorkItemsEditController extends Controller {
  @queryManager apollo;

  @service store;
  @service notification;
  @service intl;
  @service session;
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
      console.error(error);
      this.notification.danger(this.intl.t("workItems.fetchError"));
    }
  }

  @lastValue("fetchUserChoices") userChoices;
  @dropTask
  *fetchUserChoices() {
    try {
      return (yield this.store.query("public-user", {
        service: this.session.service.id,
        disabled: false,
      })).toArray();
    } catch (error) {
      this.notification.danger(this.intl.t("workItems.fetchError"));
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

      this.notification.success(this.intl.t("workItems.finishSuccess"));

      this.router.transitionTo("cases.detail.work-items.index");
    } catch (error) {
      this.notification.danger(this.intl.t("workItems.saveError"));
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

      this.notification.success(this.intl.t("workItems.saveSuccess"));

      this.router.transitionTo("cases.detail.work-items.index");
    } catch (error) {
      this.notification.danger(this.intl.t("workItems.saveError"));
    }
  }
}
