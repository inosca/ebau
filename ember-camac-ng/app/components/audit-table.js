import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency";
import createDocument from "ember-ebau-core/gql/mutations/create-document.graphql";
import linkDocument from "ember-ebau-core/gql/mutations/link-document.graphql";

import saveAnswerMutation from "camac-ng/gql/mutations/save-answer.graphql";
import getMainDocumentAnswerQuery from "camac-ng/gql/queries/get-document-answer.graphql";

export default class AuditTableComponent extends Component {
  @service notification;
  @service router;
  @service intl;

  @queryManager apollo;

  get forms() {
    return ["fp-form", "mp-form", "bab-form"];
  }

  @dropTask
  *create(form, event) {
    event.preventDefault();

    try {
      // create empty document
      const document = yield this.apollo.mutate(
        {
          mutation: createDocument,
          variables: { form },
        },
        "saveDocument.document",
      );
      const documentId = decodeId(document.id);

      if (form === "bab-form") {
        // get the value of the answer "nutzungsart" of the main document
        const cases = yield this.apollo.query(
          {
            query: getMainDocumentAnswerQuery,
            variables: {
              instanceId: this.args.workItem.caseData.instanceId,
              question: "nutzungsart",
            },
          },
          "allCases.edges",
        );
        const nutzungsartAnswer =
          cases[0].node.document.answers.edges[0]?.node.value;

        /**
         * Write an answer to the hidden question "bab-landwirtschaft-nutzung"
         * so the question "bab-bestaetigung-landwirtschaft" question is displayed
         * in the bab form.
         */
        if (nutzungsartAnswer?.includes("nutzungsart-landwirtschaft")) {
          yield this.apollo.mutate({
            mutation: saveAnswerMutation,
            variables: {
              document: documentId,
              question: "bab-landwirtschaft-nutzung",
              value: "bab-landwirtschaft-nutzung-ja",
            },
          });
        }
      }

      const value = new Set(this.args.documentData[form] || []);

      value.add(documentId);

      // link document to the right table
      yield this.apollo.mutate({
        mutation: linkDocument,
        variables: {
          question: form,
          document: this.args.documentData.id,
          value: [...value],
        },
      });

      yield this.args.onRefresh();

      yield this.router.transitionTo("audit.edit", documentId);
    } catch (error) {
      this.notification.danger(this.intl.t("audit.createError"));
    }
  }
}
