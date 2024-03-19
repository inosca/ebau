import Controller from "@ember/controller";
import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { confirm } from "ember-uikit";
import { trackedTask } from "reactiveweb/ember-concurrency";
import { dedupeTracked } from "tracked-toolbox";

import mainConfig from "ember-ebau-core/config/main";
import saveWorkItemMutation from "ember-ebau-core/gql/mutations/save-workitem.graphql";
import getPublication from "ember-ebau-core/gql/queries/get-publication.graphql";
import getPublications from "ember-ebau-core/gql/queries/get-publications.graphql";

export default class PublicationEditController extends Controller {
  @service notification;
  @service intl;
  @service ebauModules;
  @service router;

  @queryManager apollo;

  @dedupeTracked documentId;

  get filters() {
    return [
      { addressedGroups: [String(this.ebauModules.serviceId)] },
      {
        caseMetaValue: [
          { key: "camac-instance-id", value: this.model.instanceId },
        ],
      },
    ];
  }

  publication = trackedTask(this, this.fetchPublication, () => [
    this.model.workItemId,
  ]);

  @dropTask
  *fetchPublication(id) {
    const response = yield this.apollo.watchQuery(
      {
        query: getPublication,
        variables: { id: btoa(`WorkItem:${id}`) },
      },
      "node",
    );

    // Set documentId manually so it's dedupe tracked. This is needed so the
    // form doesn't get rerendered when the ID is updated because of a mutation
    // but didn't change.
    this.documentId = decodeId(response.document.id);

    return response;
  }

  @dropTask
  *cancel() {
    try {
      if (
        !(yield confirm(
          this.intl.t(`publication.cancelConfirm.${this.model.type}`),
        ))
      ) {
        return;
      }

      yield this.apollo.mutate({
        mutation: saveWorkItemMutation,
        variables: {
          input: {
            workItem: this.publication.value.id,
            meta: JSON.stringify({
              ...this.publication.value.meta,
              "is-published": false,
            }),
          },
        },
      });
    } catch (e) {
      this.notification.danger(this.intl.t("publication.cancelError"));
    }
  }

  @action async refreshNavigation(transitionToIndex = false) {
    const { task, startQuestion, endQuestion } =
      mainConfig.publication[this.model.type];

    await this.apollo.query({
      query: getPublications,
      fetchPolicy: "network-only",
      variables: {
        instanceId: this.ebauModules.instanceId,
        task,
        startQuestion,
        endQuestion,
        fetchDates: Boolean(startQuestion && endQuestion),
      },
    });

    if (transitionToIndex) {
      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute("publication", "index"),
      );
    }
  }
}
