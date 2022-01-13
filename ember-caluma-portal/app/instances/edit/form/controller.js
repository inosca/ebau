import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { useTask } from "ember-resources";

import getInstanceCaseQuery from "caluma-portal/gql/queries/get-instance-case.graphql";

export default class InstancesEditFormController extends Controller {
  @service calumaStore;

  @queryManager apollo;

  @controller("instances.edit") editController;

  queryParams = ["displayedForm"];

  @tracked displayedForm = "";

  get instanceId() {
    return this.editController.model;
  }

  get instance() {
    return this.editController.instance;
  }

  document = useTask(this, this.fetchDocument, () => [
    this.model,
    this.instanceId,
  ]);

  @dropTask()
  *fetchDocument() {
    yield this.instance;

    const raw = yield this.apollo.query(
      {
        query: getInstanceCaseQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: this.instanceId },
      },
      "allCases.edges.firstObject.node"
    );

    if (this.instance.value.mainForm.slug === this.model) {
      return raw.document;
    }

    const workItemEdge = raw.workItems.edges.find(
      ({ node }) => node.document && node.document.form.slug === this.model
    );

    return workItemEdge?.node.document;
  }
}
