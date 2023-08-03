import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { findRecord } from "ember-data-resources";
import { trackedTask } from "ember-resources/util/ember-concurrency";

import getInstanceCaseQuery from "ebau/gql/queries/get-instance-case.graphql";

export default class CasesDetailFormController extends Controller {
  @service calumaStore;

  @queryManager apollo;

  queryParams = ["displayedForm"];

  @tracked displayedForm = "";

  instance = findRecord(this, "instance", () => this.model);
  document = trackedTask(this, this.fetchDocument, () => [this.model]);

  @dropTask()
  *fetchDocument() {
    const raw = yield this.apollo.query(
      {
        query: getInstanceCaseQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: this.model },
      },
      "allCases.edges.firstObject.node",
    );

    return raw.document;
  }
}
