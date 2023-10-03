import Route from "@ember/routing/route";
import { inject as service } from "@ember/service";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";

import getDistributionCaseQuery from "ebau/gql/queries/get-distribution-case.graphql";

export default class CasesDetailDistibutionIndexRoute extends Route {
  @service router;
  @queryManager apollo;

  model() {
    const instance = this.modelFor("cases.detail");
    return this.apollo.query(
      {
        query: getDistributionCaseQuery,
        fetchPolicy: "network-only",
        variables: { instanceId: instance.id },
      },
      "allCases.edges.firstObject.node.workItems.edges.firstObject.node.childCase.id",
    );
  }

  redirect(distributionId) {
    this.router.replaceWith(
      "cases.detail.distribution.distribution-engine",
      decodeId(distributionId),
    );
  }
}
