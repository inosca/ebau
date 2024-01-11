import Controller from "@ember/controller";
import { tracked } from "@glimmer/tracking";
import { queryManager } from "ember-apollo-client";
import { trackedFunction } from "ember-resources/util/function";

import getInstanceCaseQuery from "ebau/gql/queries/get-instance-case.graphql";

export default class CasesDetailFormController extends Controller {
  queryParams = ["displayedForm"];

  @tracked displayedForm = "";

  @queryManager apollo;

  document = trackedFunction(this, async () => {
    const raw = await this.apollo.query(
      {
        query: getInstanceCaseQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: this.model.id },
      },
      "allCases.edges",
    );

    return raw[0].node.document;
  });
}
