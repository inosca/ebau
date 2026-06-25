import Controller from "@ember/controller";
import { action } from "@ember/object";
import { service } from "@ember/service";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { confirm } from "ember-uikit";
import { trackedTask } from "reactiveweb/ember-concurrency";
import { trackedFunction } from "reactiveweb/function";
import { dedupeTracked } from "tracked-toolbox";

import mainConfig from "ember-ebau-core/config/main";
import saveWorkItemMutation from "ember-ebau-core/gql/mutations/save-workitem.graphql";
import getPublication from "ember-ebau-core/gql/queries/get-publication.graphql";
import getPublications from "ember-ebau-core/gql/queries/get-publications.graphql";

const getAnswerString = (edges, slug) =>
  edges?.find((answer) => answer.node.question.slug === slug)?.node.value;

export default class PublicationEditController extends Controller {
  @service notification;
  @service intl;
  @service ebauModules;
  @service router;
  @service fetch;
  @service dms;

  @queryManager apollo;

  @dedupeTracked documentId;

  placeholders = trackedFunction(this, async () => {
    const response = await this.fetch.fetch(
      `/api/v1/instances/${this.model.instanceId}/dms-placeholders`,
      {
        headers: { accept: "application/json" },
      },
    );

    return await response.json();
  });

  get confirmTextKey() {
    return `publication.submitConfirm.${this.model.type}`;
  }

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

  get #config() {
    return mainConfig.publication[this.model.type];
  }

  get createTask() {
    return this.#config.createTask;
  }

  get fillTask() {
    return this.#config.task;
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

      const notification = mainConfig.publication.cancelNotification;
      if (notification) {
        yield this.fetch.fetch(`/api/v1/notification-templates/sendmail`, {
          method: "POST",
          headers: {
            accept: "application/vnd.api+json",
            "content-type": "application/vnd.api+json",
          },
          body: JSON.stringify({
            data: {
              type: "notification-template-sendmails",
              attributes: {
                "template-slug": notification.templateSlug,
                "recipient-types": notification.recipientTypes,
              },
              relationships: {
                instance: {
                  data: { type: "instances", id: this.model.instanceId },
                },
              },
            },
          }),
        });
      }
    } catch {
      this.notification.danger(this.intl.t("publication.cancelError"));
    }
  }

  @dropTask
  *merge(saveToDocuments, event) {
    event.preventDefault();

    const edges =
      this.publication.value?.case?.family?.document?.answers?.edges || [];
    const oerebThemaValue = getAnswerString(edges, "oereb-thema");
    const publicationType =
      oerebThemaValue && mainConfig.oerebPublicationMapping[oerebThemaValue]
        ? mainConfig.oerebPublicationMapping[oerebThemaValue]
        : "baubewilligung";
    const templateSlug = mainConfig.publicationTemplateMapping[publicationType];

    yield this.dms.processMerge({
      placeholders: this.placeholders.value,
      templateSlug,
      filenameBase: templateSlug,
      instanceId: this.model.instanceId,
      saveToDocuments: saveToDocuments ?? true,
    });
  }

  @action
  async refreshNavigation(transitionToIndex = false) {
    const { task, dateRanges } = this.#config;

    await this.apollo.query({
      query: getPublications,
      fetchPolicy: "network-only",
      variables: {
        instanceId: this.ebauModules.instanceId,
        task,
        dateQuestions: dateRanges.flat(),
      },
    });

    if (transitionToIndex) {
      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute("publication", "index"),
      );
    }
  }

  @action
  async confirm(message, validateFn) {
    if (!(await confirm(message))) {
      return false;
    }

    if (!validateFn) {
      return true;
    }

    return await validateFn();
  }
}
