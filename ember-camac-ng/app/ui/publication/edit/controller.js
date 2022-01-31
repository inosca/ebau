import Controller, { inject as controller } from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";

import saveWorkItemMutation from "camac-ng/gql/mutations/save-workitem.graphql";
import getPublications from "camac-ng/gql/queries/get-publications.graphql";
import confirm from "camac-ng/utils/confirm";

export default class PublicationEditController extends Controller {
  @service notifications;
  @service intl;
  @service shoebox;
  @service router;

  @controller("publication") publicationController;

  @queryManager apollo;

  get filters() {
    return [
      { addressedGroups: [this.shoebox.content.serviceId] },
      {
        caseMetaValue: [
          { key: "camac-instance-id", value: this.model.instanceId },
        ],
      },
    ];
  }

  get publication() {
    return this.publicationController.publications.value?.find(
      (publication) => decodeId(publication.node.id) === this.model.workItemId
    )?.node;
  }

  @dropTask
  *cancel() {
    try {
      if (
        !(yield confirm(
          this.intl.t(`publication.cancelConfirm.${this.model.type}`)
        ))
      ) {
        return;
      }

      yield this.apollo.mutate({
        mutation: saveWorkItemMutation,
        variables: {
          input: {
            workItem: this.publication.id,
            meta: JSON.stringify({
              ...this.publication.meta,
              "is-published": false,
            }),
          },
        },
      });
    } catch (e) {
      this.notifications.error(this.intl.t("publication.cancelError"));
    }
  }

  @action async refreshNavigation(transitionToIndex = false) {
    await this.apollo.query({
      query: getPublications,
      fetchPolicy: "network-only",
      variables: this.publicationController.variables,
    });

    if (transitionToIndex) {
      this.router.transitionTo("publication.index");
    }
  }
}
