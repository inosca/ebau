import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { dropTask, lastValue } from "ember-concurrency";

import getWorkItemOfTask from "camac-ng/gql/queries/get-work-item-of-task.graphql";

export default class TaskFormController extends Controller {
  @service apollo;
  @service shoebox;

  queryParams = ["displayedForm"];

  get moduleName() {
    return this.shoebox.content?.moduleName;
  }

  @lastValue("fetchWorkItem") workItem;
  @dropTask
  *fetchWorkItem() {
    const response = yield this.apollo.query({
      query: getWorkItemOfTask,
      fetchPolicy: "network-only",
      variables: { instanceId: this.model.instance_id, task: this.model.task },
    });

    return response.allWorkItems.edges[0]?.node;
  }
}
