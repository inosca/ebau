import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { useTask } from "ember-resources";

import getPublications from "camac-ng/gql/queries/get-publications.graphql";

export default class PublicationController extends Controller {
  @service notifications;
  @service intl;

  @queryManager apollo;

  publications = useTask(this, this.fetchPublications, () => [this.variables]);

  get variables() {
    return {
      instanceId: this.model.instanceId,
      ...(this.model.type === "neighbors"
        ? {
            task: "information-of-neighbors",
            startQuestion: "information-of-neighbors-start-date",
            endQuestion: "information-of-neighbors-end-date",
          }
        : {
            task: "fill-publication",
            startQuestion: "publikation-startdatum",
            endQuestion: "publikation-ablaufdatum",
          }),
    };
  }

  @dropTask
  *fetchPublications(variables) {
    try {
      return yield this.apollo.watchQuery(
        { query: getPublications, variables },
        "allWorkItems.edges"
      );
    } catch (error) {
      this.notifications.error(this.intl.t("publication.loadingError"));
    }
  }
}
