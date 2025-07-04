import { service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "reactiveweb/function";

import mainConfig from "ember-ebau-core/config/main";
import createDocumentMutation from "ember-ebau-core/gql/mutations/create-document.graphql";
import linkDocumentMutation from "ember-ebau-core/gql/mutations/link-document.graphql";
import documentsQuery from "ember-ebau-core/gql/queries/legal-appeal/documents.graphql";
import workItemQuery from "ember-ebau-core/gql/queries/legal-appeal/work-item.graphql";

export default class LegalAppealTableComponent extends Component {
  @service ebauModules;
  @service notification;
  @service abilities;
  @service router;
  @service intl;

  @queryManager apollo;

  workItem = trackedFunction(this, async () => {
    try {
      const response = await this.apollo.query({
        query: workItemQuery,
        variables: {
          task: mainConfig.legalAppeal.task,
          instanceId: this.ebauModules.instanceId,
        },
      });

      return response.allWorkItems.edges[0].node;
    } catch {
      this.notification.danger(this.intl.t("legal-appeal.loading-error"));
    }
  });

  get rootDocumentId() {
    return this.workItem.value
      ? decodeId(this.workItem.value.document.id)
      : null;
  }

  legalAppeals = trackedFunction(this, async () => {
    if (!this.rootDocumentId) {
      return [];
    }

    try {
      const response = await this.apollo.query({
        query: documentsQuery,
        fetchPolicy: "network-only",
        variables: {
          orderQuestion: mainConfig.legalAppeal.orderQuestion,
          questions: [
            ...new Set(Object.values(mainConfig.legalAppeal.columns)),
          ],
          personQuestions: [
            mainConfig.answerSlugs.firstNameApplicant,
            mainConfig.answerSlugs.lastNameApplicant,
            mainConfig.answerSlugs.juristicNameApplicant,
            mainConfig.answerSlugs.isJuristicApplicant,
            mainConfig.answerSlugs.hasRepresentativeApplicant,
          ].filter(Boolean),
          filter: [
            { rootDocument: this.rootDocumentId },
            { form: mainConfig.legalAppeal.tableForm },
          ],
        },
      });

      return response.allDocuments.edges.map((edge) => edge.node);
    } catch {
      this.notification.danger(this.intl.t("legal-appeal.loading-error"));
    }
  });

  colspan = trackedFunction(this, async () => {
    const colspan = Object.keys(mainConfig.legalAppeal.columns).length;
    const canEdit = await this.abilities.can(
      "edit legal-appeal",
      this.workItem.value,
    );
    return canEdit ? colspan + 1 : colspan;
  });

  @dropTask
  *create(event) {
    event.preventDefault();

    try {
      const rawDocumentId = yield this.apollo.mutate(
        {
          mutation: createDocumentMutation,
          variables: { form: mainConfig.legalAppeal.tableForm },
        },
        "saveDocument.document.id",
      );

      const documentId = decodeId(rawDocumentId);

      const rowIds =
        this.legalAppeals.value.map((row) => decodeId(row.id)) ?? [];

      yield this.apollo.mutate({
        mutation: linkDocumentMutation,
        variables: {
          question: mainConfig.legalAppeal.tableQuestion,
          document: this.rootDocumentId,
          value: [...rowIds, documentId],
        },
      });

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute("legal-submission", "edit-appeal"),
        documentId,
      );
    } catch {
      this.notification.danger(this.intl.t("legal-appeal.create-error"));
    }
  }

  hasColumn = (name) =>
    Object.keys(mainConfig.legalAppeal.columns).includes(name);
}
