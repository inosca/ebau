import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
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
  redirectToCaseWorkItems() {
    if (this.workItem.value?.task.meta.redirectToWorkItemsAfterCompletion) {
      this.ebauModules.redirectToCaseWorkItems();
    }
  }
}
