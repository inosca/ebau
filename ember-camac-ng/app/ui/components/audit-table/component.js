import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency-decorators";

import createAuditDocument from "camac-ng/gql/mutations/create-audit-document.graphql";
import linkAuditDocument from "camac-ng/gql/mutations/link-audit-document.graphql";

export default class AuditTableComponent extends Component {
  @service notifications;
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
          mutation: createAuditDocument,
          variables: { form },
        },
        "saveDocument.document"
      );
      const documentId = decodeId(document.id);

      const value = new Set(this.args.documentData[form] || []);

      value.add(documentId);

      // link document to the right table
      yield this.apollo.mutate({
        mutation: linkAuditDocument,
        variables: {
          question: form,
          document: this.args.documentData.id,
          value: [...value],
        },
      });

      yield this.args.onRefresh();

      yield this.router.transitionTo("audit.edit", documentId);
    } catch (error) {
      this.notifications.error(this.intl.t("audit.createError"));
    }
  }
}
