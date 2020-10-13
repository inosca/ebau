import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import getInstanceCaseQuery from "camac-ng/gql/queries/get-instance-case";

export default class FormController extends Controller {
  queryParams = ["displayedForm"];
  @tracked displayedForm;

  @service calumaStore;
  @queryManager apollo;

  @lastValue("getDocument") document;

  @dropTask()
  *getDocument() {
    const raw = yield this.apollo.query(
      {
        query: getInstanceCaseQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: this.model.id }
      },
      "allCases.edges.firstObject.node"
    );

    return raw.document;
  }
}
