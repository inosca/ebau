import Controller, { inject as controller } from "@ember/controller";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import completeWorkItem from "camac-ng/gql/mutations/complete-work-item.graphql";
import getCreatePublication from "camac-ng/gql/queries/get-create-publication.graphql";
import getPublication from "camac-ng/gql/queries/get-publication.graphql";

export default class PublicationEditController extends Controller {
  @service notifications;
  @service intl;

  @queryManager apollo;

  @controller("publication") publicationController;

  @lastValue("fetchPublication") publication;
  @dropTask
  *fetchPublication() {
    try {
      return yield this.apollo.query(
        {
          query: getPublication,
          variables: { id: this.model },
        },
        "allWorkItems.edges.firstObject.node"
      );
    } catch (error) {
      this.notifications.error(this.intl.t("publication.loadingError"));
    }
  }

  @lastValue("fetchCreateWorkItem") createPublicationWorkItem;
  @dropTask
  *fetchCreateWorkItem() {
    try {
      return yield this.apollo.query(
        {
          query: getCreatePublication,
          variables: { instanceId: this.publicationController.model },
          fetchPolicy: "network-only",
        },
        "allCases.edges.firstObject.node.workItems.edges.firstObject.node"
      );
    } catch (error) {
      this.notifications.error(this.intl.t("publication.loadingError"));
    }
  }

  @dropTask
  *createPublication() {
    if (!this.createPublicationWorkItem) {
      return;
    }

    try {
      yield this.apollo.mutate({
        mutation: completeWorkItem,
        variables: { id: this.createPublicationWorkItem.id },
      });

      yield this.publicationController.fetchPublications.perform();

      this.transitionToRoute("publication.index");
    } catch (error) {
      this.notifications.error(this.intl.t("publication.createError"));
    }
  }
}
