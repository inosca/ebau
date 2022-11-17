import { action } from "@ember/object";
import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import { trackedFunction } from "ember-resources/util/function";

import createDocumentMutation from "camac-ng/gql/mutations/create-document.graphql";
import linkDocumentMutation from "camac-ng/gql/mutations/link-document.graphql";
import documentsQuery from "camac-ng/gql/queries/legal-submission/documents.graphql";
import filterOptionsQuery from "camac-ng/gql/queries/legal-submission/filter-options.graphql";
import workItemQuery from "camac-ng/gql/queries/legal-submission/work-item.graphql";

export default class LegalSubmissionTableComponent extends Component {
  @service notification;
  @service abilities;
  @service router;
  @service intl;

  @queryManager apollo;

  get status() {
    return (
      this.filterOptions.value?.status.edges.map((edge) =>
        edge.node.options.edges.map((edge) => edge.node)
      )[0] ?? []
    );
  }

  get types() {
    return (
      this.filterOptions.value?.type.edges.map((edge) =>
        edge.node.options.edges.map((edge) => edge.node)
      )[0] ?? []
    );
  }

  get selectedTypes() {
    return this.types.filter((type) =>
      this.args.types.split(",").includes(type.slug)
    );
  }

  get selectedStatus() {
    return this.status.find((status) =>
      this.args.status.split(",").includes(status.slug)
    );
  }

  get colspan() {
    return this.abilities.can("edit legal-submission", this.workItem.value)
      ? 6
      : 5;
  }

  filterOptions = trackedFunction(this, async () => {
    return await this.apollo.watchQuery({ query: filterOptionsQuery });
  });

  workItem = trackedFunction(this, async () => {
    try {
      const response = await this.apollo.query({
        query: workItemQuery,
        variables: { instanceId: this.args.instanceId },
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
          filter: [
            { rootDocument: this.rootDocumentId },
            { form: "legal-submission-form" },
            this.args.status
              ? {
                  hasAnswer: [
                    {
                      question: "legal-submission-status",
                      value: this.args.status,
                      hierarchy: "DIRECT",
                    },
                  ],
                }
              : {},
            this.args.types
              ? {
                  hasAnswer: [
                    {
                      question: "legal-submission-type",
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
      this.notification.danger(this.intl.t("legalSubmission.loading-error"));
    }
  });

  @dropTask
  *create(event) {
    event.preventDefault();

    try {
      const rawDocumentId = yield this.apollo.mutate(
        {
          mutation: createDocumentMutation,
          variables: { form: "legal-submission-form" },
        },
        "saveDocument.document.id"
      );

      const documentId = decodeId(rawDocumentId);

      const rowIds =
        this.workItem.value.document.answers.edges[0]?.node.value.map((row) =>
          decodeId(row.id)
        ) ?? [];

      yield this.apollo.mutate({
        mutation: linkDocumentMutation,
        variables: {
          question: "legal-submission-table",
          document: this.rootDocumentId,
          value: [...rowIds, documentId],
        },
      });

      this.router.transitionTo("legal-submission.edit", documentId);
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
}
