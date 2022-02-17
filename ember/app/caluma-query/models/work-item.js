import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import completeWorkItemMutation from "citizen-portal/gql/mutations/complete-workitem";
import { queryManager } from "ember-apollo-client";
import WorkItemModel from "ember-caluma/caluma-query/models/work-item";
import { dropTask } from "ember-concurrency-decorators";

export default class CustomWorkItemModel extends WorkItemModel {
  @queryManager apollo;
  @service notification;

  @tracked rawStatus = this.raw.status;

  get isReady() {
    return this.rawStatus === "READY";
  }

  get status() {
    return this.intl.t(
      `caluma.caluma-query.work-item.status.${this.rawStatus}`
    );
  }

  @dropTask
  *completeWorkItem() {
    try {
      const response = yield this.apollo.mutate({
        mutation: completeWorkItemMutation,
        variables: {
          input: {
            id: this.id,
          },
        },
      });

      this.rawStatus = response.completeWorkItem.workItem.status;

      this.notification.success("Aufgabe wurde abgeschlossen");
      return true;
    } catch (error) {
      this.notification.danger("Aufgabe konnte nicht abgeschlossen werden");
    }
  }

  static fragment = `{
    createdAt
    createdByUser
    createdByGroup
    closedAt
    closedByUser
    closedByGroup
    status
    meta
    addressedGroups
    controllingGroups
    assignedUsers
    name
    deadline
    description
    case {
      id
      meta
    }
    task {
      slug
    }
  }`;
}
