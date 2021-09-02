import Controller, { inject as controller } from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import getPublication from "camac-ng/gql/queries/get-publication.graphql";
import confirm from "camac-ng/utils/confirm";

export default class PublicationEditController extends Controller {
  @service notifications;
  @service intl;

  @queryManager apollo;

  @controller("publication") publicationController;

  get filters() {
    return [
      { status: "READY" },
      {
        caseMetaValue: [
          {
            key: "camac-instance-id",
            value: this.publicationController.model,
          },
        ],
      },
    ];
  }

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

  @action
  async beforeComplete(validateFn) {
    return (
      (await validateFn()) &&
      (await confirm(this.intl.t("publication.confirm")))
    );
  }

  @action async afterComplete() {
    await this.publicationController.fetchPublications.perform();
    await this.fetchPublication.perform();
  }

  @action async afterCreate() {
    await this.publicationController.fetchPublications.perform();

    this.transitionToRoute("index");
  }
}
