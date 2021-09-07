import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import getWorkItemOfTask from "camac-ng/gql/queries/get-work-item-of-task.graphql";

export default class TaskFormController extends Controller {
  @service apollo;
  @service shoebox;

  get moduleName() {
    return this.shoebox.content?.moduleName;
  }

  get context() {
    return { ...this.model, workItemId: this.workItem?.id };
  }

  @lastValue("fetchWorkItem") workItem;
  @dropTask
  *fetchWorkItem() {
    const response = yield this.apollo.query({
      query: getWorkItemOfTask,
      fetchPolicy: "network-only",
      variables: this.model,
    });

    return response.allWorkItems.edges[0]?.node;
  }
}
