import { inject as service } from "@ember/service";
import completeWorkItemMutation from "citizen-portal/gql/mutations/complete-workitem";
import { queryManager } from "ember-apollo-client";
import WorkItemModel from "ember-caluma/caluma-query/models/work-item";
import { dropTask } from "ember-concurrency-decorators";

export default class CustomWorkItemModel extends WorkItemModel {
  @queryManager apollo;
  @service notification;

  get isReady() {
    return this.raw.status === "READY";
  }

  @dropTask
  *completeWorkItem() {
    try {
      yield this.apollo.mutate({
        mutation: completeWorkItemMutation,
        variables: {
          input: {
            id: this.id,
          },
        },
      });

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
