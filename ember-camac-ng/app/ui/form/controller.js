import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";

import getInstanceCaseQuery from "camac-ng/gql/queries/get-instance-case.graphql";

export default class FormController extends Controller {
  @service calumaStore;
  @service store;

  @queryManager apollo;

  queryParams = ["displayedForm"];

  @tracked displayedForm;

  @lastValue("getData") data;

  @dropTask()
  *getData() {
    const instance = yield this.store.findRecord("instance", this.model.id);
    const raw = yield this.apollo.query(
      {
        query: getInstanceCaseQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: this.model.id },
      },
      "allCases.edges.firstObject.node"
    );

    return { instance, case: raw, document: raw.document };
  }
}
