import Controller from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { trackedTask } from "ember-resources/util/ember-concurrency";

import getPublications from "ember-ebau-core/gql/queries/get-publications.graphql";

export default class PublicationController extends Controller {
  @service notification;
  @service intl;
  @service ebauModules;

  @queryManager apollo;

  publications = trackedTask(this, this.fetchPublications, () => [
    this.variables,
  ]);

  get variables() {
    return {
      instanceId: this.ebauModules.instanceId,
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
        "allWorkItems.edges",
      );
    } catch (error) {
      this.notification.danger(this.intl.t("publication.loadingError"));
    }
  }
}
