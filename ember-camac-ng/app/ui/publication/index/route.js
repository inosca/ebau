import Route from "@ember/routing/route";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";

import getLatestPublication from "camac-ng/gql/queries/get-latest-publication.graphql";

export default class PublicationIndexRoute extends Route {
  @queryManager apollo;

  async model() {
    const workItemId = await this.apollo.query(
      {
        fetchPolicy: "network-only",
        query: getLatestPublication,
        variables: { instanceId: this.modelFor("publication") },
      },
      "allCases.edges.firstObject.node.workItems.edges.firstObject.node.id"
    );

    return decodeId(workItemId);
  }

  redirect(model) {
    this.replaceWith("publication.edit", decodeId(model));
  }
}
