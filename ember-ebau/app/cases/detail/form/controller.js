import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

import getInstanceCaseQuery from "ebau/gql/queries/get-instance-case.graphql";

export default class CasesDetailFormController extends Controller {
  @service calumaStore;

  @queryManager apollo;

  queryParams = ["displayedForm"];

  @tracked displayedForm = "";

  document = trackedTask(this, this.fetchDocument, () => [this.model.id]);

  @dropTask()
  *fetchDocument() {
    const raw = yield this.apollo.query(
      {
        query: getInstanceCaseQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: this.model.id },
      },
      "allCases.edges.firstObject.node",
    );

    return raw.document;
  }
}
