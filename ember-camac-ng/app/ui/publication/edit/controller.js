import Controller, { inject as controller } from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { queryManager } from "ember-apollo-client";
import { dropTask, lastValue } from "ember-concurrency-decorators";

import saveWorkItemMutation from "camac-ng/gql/mutations/save-workitem.graphql";
import getPublication from "camac-ng/gql/queries/get-publication.graphql";
import confirm from "camac-ng/utils/confirm";

export default class PublicationEditController extends Controller {
  @queryManager apollo;

  @service notifications;
  @service intl;
  @service shoebox;

  @queryManager apollo;

  @controller("publication") publicationController;

  get filters() {
    return [
      { addressedGroups: [this.shoebox.content.serviceId] },
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

  @dropTask
  *cancelPublication(workItem) {
    try {
      yield this.apollo.mutate({
        mutation: saveWorkItemMutation,
        variables: {
          input: {
            workItem: workItem.id,
            meta: JSON.stringify({
              ...workItem.meta,
              "is-published": false,
            }),
          },
        },
      });
      window.location.reload();
    } catch (e) {
      console.error(e);
    }
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
