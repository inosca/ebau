import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency";

import getPublications from "camac-ng/gql/queries/get-publications.graphql";

export default class PublicationController extends Controller {
  @service notifications;
  @service intl;

  @queryManager apollo;

  @lastValue("fetchPublications") publications;
  @dropTask
  *fetchPublications() {
    try {
      const edges = yield this.apollo.query(
        {
          query: getPublications,
          fetchPolicy: "network-only",
          variables: { instanceId: this.model },
        },
        "allCases.edges.firstObject.node.workItems.edges"
      );

      return edges.map((edge) => edge.node);
    } catch (error) {
      this.notifications.error(this.intl.t("publication.loadingError"));
    }
  }
}
