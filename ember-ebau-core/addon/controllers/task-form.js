import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "reactiveweb/function";

import getWorkItemOfTask from "ember-ebau-core/gql/queries/get-work-item-of-task.graphql";

export default class TaskFormController extends Controller {
  @service ebauModules;

  @queryManager apollo;

  queryParams = ["displayedForm"];

  workItem = trackedFunction(this, async () => {
    const response = await this.apollo.query({
      query: getWorkItemOfTask,
      fetchPolicy: "network-only",
      variables: { instanceId: this.ebauModules.instanceId, task: this.model },
    });

    return response.allWorkItems.edges[0]?.node;
  });

  @action
  redirectToWorkItems() {
    if (
      // TODO: This is spaghetti. Refactor. Currently it is very easy to break a canton by adding or removing a task type here that another canton uses without knowing about it.
      [
        "decision",
        "formal-exam",
        "material-exam",
        "construction-acceptance",
        "geometer",
        "complete-instance",
        "complete-check",
        "release-for-bk",
      ].includes(this.model)
    ) {
      this.ebauModules.redirectToWorkItems();
    }
  }
}
