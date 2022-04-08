import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { useTask } from "ember-resources";

import getInstanceCaseQuery from "ebau/gql/queries/get-instance-case.graphql";

export default class CasesDetailFormController extends Controller {
  @service calumaStore;

  @queryManager apollo;

  queryParams = ["displayedForm"];

  @tracked displayedForm = "";

  document = useTask(this, this.fetchDocument, () => [this.model]);

  @dropTask()
  *fetchDocument() {
    const raw = yield this.apollo.query(
      {
        query: getInstanceCaseQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: this.model },
      },
      "allCases.edges.firstObject.node"
    );

    return raw.document;
  }
}
