import { inject as service } from "@ember/service";
import Component from "@glimmer/component";
import { decodeId } from "@projectcaluma/ember-core/helpers/decode-id";
import { queryManager } from "ember-apollo-client";
import { dropTask } from "ember-concurrency-decorators";
import { saveAs } from "file-saver";

import { confirmTask } from "camac-ng/decorators";
import copyDocument from "camac-ng/gql/mutations/copy-document.graphql";
import deleteDocument from "camac-ng/gql/mutations/delete-document.graphql";
import linkAuditDocument from "camac-ng/gql/mutations/link-audit-document.graphql";

export default class AuditTableRowComponent extends Component {
  @service fetch;
  @service notifications;
  @service intl;
  @service router;

  @queryManager apollo;

  @dropTask
  *pdf() {
    try {
      const response = yield this.fetch.fetch(
        `/api/v1/instances/${this.args.audit.instanceId}/generate-pdf?document-id=${this.args.audit.id}`
      );
      if (!response.ok) {
        throw new Error(`${response.status}: ${response.statusText}`);
      }

      const filename = response.headers
        .get("content-disposition")
        .match(/filename="(.*)"/)[1];

      saveAs(yield response.blob(), filename);
    } catch (error) {
      this.notifications.error(this.intl.t("audit.createPdfError"));
    }
  }

  @dropTask
  @confirmTask("audit.deleteConfirm")
  *delete() {
    try {
      const value = new Set(this.args.documentData[this.args.audit.form] || []);

      value.delete(this.args.audit.id);

      // unlink audit
      yield this.apollo.mutate({
        mutation: linkAuditDocument,
        variables: {
          question: this.args.audit.form,
          document: this.args.documentData.id,
          value: [...value],
        },
      });

      // delete document
      yield this.apollo.mutate({
        mutation: deleteDocument,
        variables: { id: this.args.audit.id },
      });

      yield this.args.onRefresh();

      this.notifications.success(this.intl.t("audit.deleteSuccess"));
    } catch (error) {
      this.notifications.error(this.intl.t("audit.deleteError"));
    }
  }

  @dropTask
  @confirmTask("audit.copyConfirm")
  *copy() {
    try {
      // copy document
      const document = yield this.apollo.mutate(
        {
          mutation: copyDocument,
          variables: { source: this.args.audit.id },
        },
        "copyDocument.document"
      );

      const documentId = decodeId(document.id);
      const form = document.form.slug;

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
      this.notifications.error(this.intl.t("audit.copyError"));
    }
  }
}
