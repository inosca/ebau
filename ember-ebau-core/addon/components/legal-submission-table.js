import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

import mainConfig from "ember-ebau-core/config/main";
import createDocumentMutation from "ember-ebau-core/gql/mutations/create-document.graphql";
import linkDocumentMutation from "ember-ebau-core/gql/mutations/link-document.graphql";
import documentsQuery from "ember-ebau-core/gql/queries/legal-submission/documents.graphql";
import filterOptionsQuery from "ember-ebau-core/gql/queries/legal-submission/filter-options.graphql";
import workItemQuery from "ember-ebau-core/gql/queries/legal-submission/work-item.graphql";

export default class LegalSubmissionTableComponent extends Component {
  @service ebauModules;
  @service notification;
  @service abilities;
  @service router;
  @service intl;

  @queryManager apollo;

  get status() {
    return (
      this.filterOptions.value?.status.edges.map((edge) =>
        edge.node.options.edges.map((edge) => edge.node),
      )[0] ?? []
    );
  }

  get types() {
    return (
      this.filterOptions.value?.type.edges.map((edge) =>
        edge.node.options.edges.map((edge) => edge.node),
      )[0] ?? []
    );
  }

  get selectedTypes() {
    return this.types.filter((type) =>
      this.args.types.split(",").includes(type.slug),
    );
  }

  get selectedStatus() {
    return this.status.find((status) =>
      this.args.status.split(",").includes(status.slug),
    );
  }

  get colspan() {
    const colspan = Object.keys(mainConfig.legalSubmission.columns).length;

    return this.abilities.can("edit legal-submission", this.workItem.value)
      ? colspan + 1
      : colspan;
  }

  filterOptions = trackedFunction(this, async () => {
    return await this.apollo.watchQuery({ query: filterOptionsQuery });
  });

  workItem = trackedFunction(this, async () => {
    try {
      const response = await this.apollo.query({
        query: workItemQuery,
        variables: {
          task: mainConfig.legalSubmission.task,
          instanceId: this.ebauModules.instanceId,
        },
      });

      return response.allWorkItems.edges[0].node;
    } catch (error) {
      this.notification.danger(this.intl.t("legal-submission.loading-error"));
    }
  });

  get rootDocumentId() {
    return this.workItem.value
      ? decodeId(this.workItem.value.document.id)
      : null;
  }

  legalSubmissions = trackedFunction(this, async () => {
    if (!this.rootDocumentId) {
      return [];
    }

    try {
      const response = await this.apollo.query({
        query: documentsQuery,
        fetchPolicy: "network-only",
        variables: {
          orderQuestion: mainConfig.legalSubmission.orderQuestion,
          questions: Object.values(mainConfig.legalSubmission.columns),
          personQuestions: [
            mainConfig.answerSlugs.firstNameApplicant,
            mainConfig.answerSlugs.lastNameApplicant,
            mainConfig.answerSlugs.juristicNameApplicant,
            mainConfig.answerSlugs.isJuristicApplicant,
          ],
          filter: [
            { rootDocument: this.rootDocumentId },
            { form: mainConfig.legalSubmission.tableForm },
            mainConfig.legalSubmission.filters?.status && this.args.status
              ? {
                  hasAnswer: [
                    {
                      question: mainConfig.legalSubmission.filters.status,
                      value: this.args.status,
                      hierarchy: "DIRECT",
                    },
                  ],
                }
              : {},
            mainConfig.legalSubmission.filters?.types && this.args.types
              ? {
                  hasAnswer: [
                    {
                      question: mainConfig.legalSubmission.filters.types,
                      value: this.args.types.split(","),
                      lookup: "INTERSECTS",
                      hierarchy: "DIRECT",
                    },
                  ],
                }
              : {},
          ],
        },
      });

      return response.allDocuments.edges.map((edge) => edge.node);
    } catch (error) {
      this.notification.danger(this.intl.t("legal-submission.loading-error"));
    }
  });

  @dropTask
  *create(event) {
    event.preventDefault();

    try {
      const rawDocumentId = yield this.apollo.mutate(
        {
          mutation: createDocumentMutation,
          variables: { form: mainConfig.legalSubmission.tableForm },
        },
        "saveDocument.document.id",
      );

      const documentId = decodeId(rawDocumentId);

      const rowIds =
        this.legalSubmissions.value.map((row) => decodeId(row.id)) ?? [];

      yield this.apollo.mutate({
        mutation: linkDocumentMutation,
        variables: {
          question: mainConfig.legalSubmission.tableQuestion,
          document: this.rootDocumentId,
          value: [...rowIds, documentId],
        },
      });

      this.router.transitionTo(
        this.ebauModules.resolveModuleRoute("legal-submission", "edit"),
        documentId,
      );
    } catch (error) {
      this.notification.danger(this.intl.t("legal-submission.create-error"));
    }
  }

  @action
  updateStatus(value) {
    this.args.onUpdateStatus(value?.slug ?? "");
  }

  @action
  updateTypes(value) {
    this.args.onUpdateTypes(value.map((v) => v.slug).join(","));
  }

  hasColumn = (name) =>
    Object.keys(mainConfig.legalSubmission.columns).includes(name);

  hasFilter = (name) =>
    Object.keys(mainConfig.legalSubmission.filters ?? {}).includes(name);
}
