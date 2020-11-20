import Controller, { inject as controller } from "@ember/controller";
import { reads } from "@ember/object/computed";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";
import QueryParams from "ember-parachute";

import getInstanceCaseQuery from "ember-caluma-portal/gql/queries/get-instance-case";

const queryParams = new QueryParams({
  displayedForm: {
    defaultValue: "",
    refresh: true,
  },
});

export default class InstancesEditFormController extends Controller.extend(
  queryParams.Mixin
) {
  @service calumaStore;
  @queryManager apollo;

  @controller("instances.edit") editController;
  @reads("editController.embedded") embedded;
  @reads("editController.model") instanceId;
  @reads("editController.instance") instance;
  @lastValue("getDocument") document;

  setup() {
    this.getDocument.perform();
  }

  reset() {
    this.resetQueryParams();
  }

  @dropTask()
  *getDocument() {
    yield this.editController.instanceTask.last;

    const raw = yield this.apollo.query(
      {
        query: getInstanceCaseQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: this.instanceId },
      },
      "allCases.edges.firstObject.node"
    );

    if (this.instance.mainForm.slug === this.model) {
      return raw.document;
    }

    const workItemEdge = raw.workItems.edges.find(
      ({ node }) => node.document && node.document.form.slug === this.model
    );

    return workItemEdge && workItemEdge.node.document;
  }
}
